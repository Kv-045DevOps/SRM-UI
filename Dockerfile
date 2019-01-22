FROM python:3.6-alpine
MAINTAINER Maxim Zhovanik
WORKDIR /service/UI-SERV
COPY . /service/UI-SERV
RUN pip install -r requirements.txt
CMD ["python", "/service/UI-SERV/app/app.py"]
