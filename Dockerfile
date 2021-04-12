# pull offical base image
FROM python:3.7-alpine

# Add scripts to the running path of the container. Access any scripts just from them
ENV PATH = "/scripts:${PATH}"

COPY 