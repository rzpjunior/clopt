FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src
COPY run.py run.py
COPY setup.py setup.py
COPY README.md README.md

RUN pip install -e .

CMD ["clopt"]
