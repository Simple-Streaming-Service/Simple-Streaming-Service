FROM python:slim
LABEL authors="Raynor"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./app ./app
COPY boot.sh ./
COPY config.py ./

RUN chmod a+x boot.sh

ENV FLASK_APP app.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]