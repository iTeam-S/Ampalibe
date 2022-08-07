FROM python:3.10.4

WORKDIR /usr/src/app

ADD . /usr/src/app

RUN python setup.py install && rm -r ampalibe.egg-info build dist ampalibe


CMD if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt ; fi ; \
 ampalibe run 