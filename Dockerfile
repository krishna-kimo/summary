### Dockerfile for Summarizer
FROM python:3.7-stretch

LABEL maintainer="Krishna Nallamilli<krishna@kimo.ai"
LABEL version="1.0"

WORKDIR /home/user

# Install required packages
RUN pip install fastapi
RUN pip install transformers
RUN pip install tensorflow==2.1.0
RUN pip install torch==1.5.0
RUN pip install newspaper3k
RUN pip install gunicorn
RUN pip install uvicorn
### Need to move all the above to requirements.txt file

COPY . /home/user
### script to download models into the models directory
### Decide b/w run time or build time

## Ports
EXPOSE 8000

## cmd to run
CMD ["gunicorn", "fapi:app", "-b", "0.0.0.0", "-k", "uvicorn.workers.UvicornWorker", "--workers", "2", "--timeout", "0"]

