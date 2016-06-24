FROM python:2.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN pip install uwsgi

# ADD requirements.txt /code/
# RUN pip install -r requirements.txt
RUN pip install -e git+https://github.com/brianz/servant.git#egg=servant

COPY . /code/
RUN pip install -e .
