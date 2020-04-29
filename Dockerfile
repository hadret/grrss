FROM python:3.7-slim

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY grrss.py /tmp/grrss

CMD python /tmp/grrss
