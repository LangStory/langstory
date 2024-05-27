FROM python:3.11
RUN apt install -y git && git config --global --add safe.directory /app && pip install mentat