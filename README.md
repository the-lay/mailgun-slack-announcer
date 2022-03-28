# Mailgun - Slack Announcer
[<img src="https://img.shields.io/badge/dockerhub-images-green.svg?logo=Docker">](TODO)
TODO GITHUB ACTIONS

Yet another incoming mailgun mail to slack utility.  
For ease of use, containerized [(Docker Hub)](TODO) and configured with environment variables.

Heavily inspired by [artnc/router.py](https://chaidarun.com/slack-emails).

## Quick start

1. Create an `.env` file based on `.env.sample` from the repository
2. Run the container and pass env file with...  
    ... Docker:
    ```bash
    docker run --env-file .env containername:latest
    ```

    ... Docker Compose: 
    ```docker
    version: "3.7"
    services:
        mailgun:
            image:
            restart: always
            env_file:
                - .env
            ports:
                - "8000:80"
    ```

In addition to env variables defined in `.env`, the docker image can take advantage of base image 
[tiangolo/meinheld-gunicorn-flask-docker](https://github.com/tiangolo/meinheld-gunicorn-flask-docker)
and use
[its environment variables](https://github.com/tiangolo/meinheld-gunicorn-flask-docker#environment-variables).
      
## Run locally

To run locally and publish to port 8000:
```bash
docker build -t mailgun-slack-announcer .
docker run -d --name mailgun -p 8000:80 mailgun-slack-announcer
```

## Message templating
To modify the templating, TODO.  
See all available message parameters that come from mailgun [on their docs](https://documentation.mailgun.com/en/latest/user_manual.html#parsed-messages-parameters).