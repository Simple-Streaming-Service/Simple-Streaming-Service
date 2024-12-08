FROM python:slim
LABEL authors="Raynor"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY static static
COPY templates templates
COPY app/app.py boot.sh ./
RUN chmod a+x boot.sh

ENV FLASK_APP app.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]