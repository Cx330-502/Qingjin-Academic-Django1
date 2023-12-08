FROM python:3.9.16-alpine

COPY Qingjin_Academic /Qingjin_Academic

WORKDIR /Qingjin_Academic

RUN pip install -r requirements.txt

EXPOSE 8000

ENV QINGJIN_ENV=prod

ENTRYPOINT ["ash", "run.sh"]
