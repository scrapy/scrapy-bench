FROM nginx
RUN apt-get update && apt-get install nginx \
                                      git \
                                      wget \
                                      python3-pip \
                                      python3 -y
RUN bash -c 'rm -rf /var/www/html/ && \
    mkdir -p /var/www/html/ && \
    pushd /var/www/html/ && \
    wget --mirror --convert-links \
         --adjust-extension --page-requisites \
         --no-parent http://books.toscrape.com/ && \
    popd && \
    mkdir /serve'

COPY docker/nginx.conf /serve/
RUN python3 -m pip install twisted git+https://github.com/Supervisor/supervisor.git@5112520
COPY docker/supervisord.conf /serve/
COPY server.py /serve/
ENTRYPOINT ["supervisord", "-c", "/serve/supervisord.conf", "--nodaemon"]
