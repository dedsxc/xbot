FROM python:3.13.6-alpine3.21@sha256:f5f25747d6589917174824189a07ed31051ec6312a7e069a7c3498bbc935f0c3

ENV USER=user

WORKDIR /app
COPY . /app

# Install chromium
RUN apk update && apk add --no-cache tini chromium=136.0.7103.113-r0 chromium-chromedriver=136.0.7103.113-r0

# Install python package
RUN python3 -m pip install --no-cache-dir -r requirements.txt 

# Set permission
RUN adduser -D -H -u 1000 $USER && \
    chown -R $USER:$USER /app

USER $USER

ENTRYPOINT ["tini", "--", "python", "main.py"]
