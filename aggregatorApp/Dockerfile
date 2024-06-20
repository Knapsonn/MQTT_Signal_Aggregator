FROM python:3

WORKDIR /app/

RUN pip install 'paho-mqtt<2.0.0' psycopg2 

COPY . /app/

CMD ["python3","signal_aggregator.py","4","20"]

