FROM python:3.7-slim

RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY grrss.py /tmp/grrss

CMD ["python", "/tmp/grrss"]
