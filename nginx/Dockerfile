# base image from nginx inc. Use unprivileged version for security reasons.
FROM nginxinc/nginx-unprivileged:1-alpine

# Copy over the files created to the sites-available folder.
COPY ./default.conf /etc/nginx/sites-available/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/sites-available/uwsgi_params

USER root

RUN mkdir -p /vol/static && mkdir -p /vol/media

# Create a user called nginx. Change ownership of the volume. Grant them full rights.
RUN adduser -D nginx && chown -R nginx:nginx /vol && chmod  755 /vol/media && chmod 755 /vol/static

# Swap to user to run the app
USER nginx