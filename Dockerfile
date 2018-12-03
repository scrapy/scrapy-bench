FROM nginx
RUN apt-get update && apt-get install nginx wget -y
RUN bash -c 'rm -rf /data/ && \
    mkdir /data/ && \
    pushd /data/ && \
    wget --mirror --convert-links \
         --adjust-extension --page-requisites \
         --no-parent http://books.toscrape.com/ && \
    popd'

COPY nginx.conf /data/
CMD ["nginx", "-c", "/data/nginx.conf"]
