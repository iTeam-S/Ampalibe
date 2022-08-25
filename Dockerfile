FROM python:3.8.10

WORKDIR /usr/src/app

ADD . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt && python setup.py install --force && rm -rf *

CMD if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt ; fi ; \
 ampalibe run 