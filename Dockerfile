FROM alpine:latest

RUN apk add --update --no-cache \
  build-base \
  postgresql-client \
  python \
  python-dev \
  py-pip

ENV INSTALL_DIR /app

WORKDIR $INSTALL_DIR

COPY . ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["run.py"]