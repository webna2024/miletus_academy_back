FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /code
RUN apt-get update && apt-get install -y gcc python3-dev libpq-dev
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/


#FROM python:3.9

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

#WORKDIR /code

#COPY requirements.txt .
#RUN pip install -r requirements.txt

#COPY . .