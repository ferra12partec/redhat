FROM registry.access.redhat.com/ubi8/python-39:latest

COPY requirements.txt ./requirements.txt
COPY data data/

RUN pip install -r requirements.txt

COPY app.py ./app.py
COPY spacy_model.py ./spacy_model.py
COPY spacy_entityruler.py ./spacy_entityruler.py

CMD ["python3", "app.py", "8080"]
