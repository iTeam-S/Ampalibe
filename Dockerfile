FROM python:3.8.10

WORKDIR /usr/src/app

ADD . /usr/src/app

RUN python setup.py install && rm -rf *


CMD if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt ; fi ; \
 ampalibe run 