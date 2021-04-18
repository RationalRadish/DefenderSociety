# base image from nginx inc. Use unprivileged version for security reasons.
FROM nginx:1.19

RUN rm /etc/nginx/conf.d/default.conf

# Copy over the files created to the sites-available folder.
COPY default.conf /etc/nginx/conf.d/default.conf
#COPY ./uwsgi_params /etc/nginx/sites-available/uwsgi_params

USER root

RUN mkdir -p /vol/static && mkdir -p /vol/media

# Create a user called nginx. Change ownership of the volume. Grant them full rights.
# RUN adduser nginx
#RUN chown -R nginx:nginx /vol
RUN  chmod  755 /vol/media
RUN chmod 755 /vol/static

# Swap to user to run the app
#USER nginx
