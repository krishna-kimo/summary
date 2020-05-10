### Dockerfile for Summarizer
FROM python:3.7-stretch

LABEL maintainer="Krishna Nallamilli<krishna@kimo.ai"
LABEL version="1.0"

WORKDIR /home/user

# Install required packages
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
#RUN pip install fastapi && pip install transformers && pip install torch==1.5.0 && \
#	pip install newspaper3k && pip install gunicorn && pip install uvicorn

### Need to move all the above to requirements.txt file

COPY . /home/user
### script to download models into the models directory
### Decide b/w run time or build time

## Ports
EXPOSE 8000

## cmd to run
CMD ["gunicorn", "fapi:app", "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "2", "--timeout", "0"]

