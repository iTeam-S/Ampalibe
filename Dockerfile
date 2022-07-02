FROM python:3.10.4

WORKDIR /usr/src/app

RUN pip install --no-cache-dir ampalibe==1.0.7 mysql-connector

CMD if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt ; fi ; \
 ampalibe run 