FROM python:3.7-alpine

RUN apk add --update --no-cache \
  build-base \
  postgresql-dev \
  py-pip

ENV INSTALL_DIR /app

WORKDIR $INSTALL_DIR

COPY . ./

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]