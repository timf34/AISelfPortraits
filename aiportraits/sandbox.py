"""Per-experiment Docker sandbox: network-off, resource-capped, non-root."""

import functools
import shutil
import subprocess
import uuid
from pathlib import Path

from aiportraits.config import BASH_TIMEOUT_S, DOCKER_IMAGE, MAX_OBSERVATION_CHARS


class SandboxError(Exception):
    pass


# The app path comes FIRST: on some machines /usr/local/bin/docker is a
# root-owned symlink into a phantom DMG volume that stalls PATH lookups.
_DOCKER_CANDIDATES = [
    "/Applications/Docker.app/Contents/Resources/bin/docker",
    "docker",
    "/usr/local/bin/docker",
]


@functools.cache
def docker_bin() -> str:
    for cand in _DOCKER_CANDIDATES:
        path = cand if "/" in cand else shutil.which(cand)
        if path and Path(path).exists():
            return path
    raise SandboxError("docker binary not found (is Docker Desktop installed?)")


def _run(cmd: list[str], timeout: float | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [docker_bin(), *cmd], capture_output=True, text=True, timeout=timeout
    )


class Sandbox:
    def __init__(self):
        self.name = f"aiport-{uuid.uuid4().hex[:12]}"
        proc = _run([
            "run", "-d", "--rm",
            "--network", "none",
            "--cpus", "1.0",
            "--memory", "1g",
            "--name", self.name,
            DOCKER_IMAGE,
            "sleep", "infinity",
        ], timeout=60)
        if proc.returncode != 0:
            raise SandboxError(f"failed to start container: {proc.stderr.strip()}")

    def bash(self, command: str, timeout_s: int = BASH_TIMEOUT_S) -> tuple[int, str]:
        """Run a command in /workspace. Returns (exit_code, combined output).
        The timeout runs inside the container so runaway processes are killed."""
        try:
            proc = _run([
                "exec", "-w", "/workspace", self.name,
                "timeout", "-k", "5", str(timeout_s), "bash", "-lc", command,
            ], timeout=timeout_s + 15)
        except subprocess.TimeoutExpired:
            return 124, f"(command did not finish within {timeout_s}s)"
        output = (proc.stdout or "") + (proc.stderr or "")
        if proc.returncode in (124, 137) and not output.strip():
            output = f"(command timed out after {timeout_s}s)"
        if len(output) > MAX_OBSERVATION_CHARS:
            output = output[:MAX_OBSERVATION_CHARS] + "\n... (output truncated)"
        return proc.returncode, output

    def copy_out(self, container_path: str, host_path: Path) -> bool:
        host_path.parent.mkdir(parents=True, exist_ok=True)
        proc = _run(["cp", f"{self.name}:{container_path}", str(host_path)], timeout=60)
        return proc.returncode == 0 and host_path.exists()

    def list_files(self) -> list[str]:
        code, out = self.bash("find /workspace -type f | sort", timeout_s=15)
        return [line for line in out.splitlines() if line.startswith("/workspace")] if code == 0 else []

    def stop(self) -> None:
        _run(["rm", "-f", self.name], timeout=30)


def cleanup_all() -> int:
    """Remove any stray aiport-* containers (e.g. after a crash)."""
    proc = _run(["ps", "-aq", "--filter", "name=aiport-"], timeout=30)
    ids = proc.stdout.split()
    if ids:
        _run(["rm", "-f", *ids], timeout=60)
    return len(ids)
