FROM registry.access.redhat.com/ubi8/python-39:latest

COPY requirements.txt ./requirements.txt
COPY data data/

RUN pip install -r requirements.txt

COPY wsgi.py ./wsgi.py
COPY spacy_model.py ./spacy_model.py
COPY spacy_entityruler.py ./spacy_entityruler.py

USER 1001
EXPOSE 8080

CMD ["python3", "wsgi.py", "8080"]