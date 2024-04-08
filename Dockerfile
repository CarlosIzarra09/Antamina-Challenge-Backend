FROM python:3.8.13-alpine3.15
WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

EXPOSE 5000
CMD ["python","-m","flask","run"]