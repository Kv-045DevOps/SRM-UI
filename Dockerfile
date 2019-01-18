FROM python:3.6-alpine
MAINTAINER Artem Kubrachenko
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["uiservice.py"]