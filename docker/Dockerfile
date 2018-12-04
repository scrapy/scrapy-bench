FROM nginx
RUN apt-get update && apt-get install nginx \
                                      git \
                                      wget \
                                      python-pip \
                                      python -y
RUN bash -c 'rm -rf /var/www/html/ && \
    mkdir -p /var/www/html/ && \
    pushd /var/www/html/ && \
    wget --mirror --convert-links \
         --adjust-extension --page-requisites \
         --no-parent http://books.toscrape.com/ && \
    popd && \
    mkdir /serve'

COPY docker/nginx.conf /serve/
RUN python -m pip install twisted supervisor
COPY docker/supervisord.conf /serve/
COPY server.py /serve
EXPOSE 8000
EXPOSE 8880
ENTRYPOINT ["supervisord", "-c", "/serve/supervisord.conf", "--nodaemon"]
