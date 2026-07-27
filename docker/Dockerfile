FROM python:3.12-slim

RUN pip install --no-cache-dir pillow numpy

RUN useradd -m agent
USER agent
WORKDIR /workspace
