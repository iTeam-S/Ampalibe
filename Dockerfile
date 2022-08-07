FROM python:3.10.4

ADD . /opt/

RUN cd /opt/ampalibe && python setup.py install && rm -r ampalibe.egg-info build dist

WORKDIR /usr/src/app

CMD if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt ; fi ; \
 ampalibe run 