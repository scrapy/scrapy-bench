FROM nginx
RUN apt-get update && apt-get install nginx \
                                      git \
                                      wget \
                                      python3-pip \
                                      python3 -y
RUN bash -c 'rm -rf /data/ && \
    mkdir /data/ && \
    pushd /data/ && \
    wget --mirror --convert-links \
         --adjust-extension --page-requisites \
         --no-parent http://books.toscrape.com/ && \
    popd'

COPY docker/nginx.conf /data/
RUN python3 -m pip install git+https://github.com/Supervisor/supervisor.git@5112520
COPY docker/supervisord.conf /data
ENTRYPOINT ["supervisord", "-c", "/data/supervisord.conf", "--nodaemon"]
