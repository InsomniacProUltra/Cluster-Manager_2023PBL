# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app

COPY miniproject_host.py /app/miniproject_host.py

COPY miniproject2_client.py /app/miniproject2_client.py
COPY random_numbers.npy /app/random_numbers.npy

COPY miniproject3_client.py /app/miniproject3_client.py
COPY x4linear_regression.npy /app/x4linear_regression.npy
COPY y4linear_regression.npy /app/y4linear_regression.npy

RUN echo "hello world" > /app/greeting

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["sh"]
