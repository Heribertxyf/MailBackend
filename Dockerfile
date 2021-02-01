FROM direpos.capitalonline.net/devops-django:base

MAINTAINER xuyangfei

ENV ENV_CONFIG=pro

RUN mkdir -p /data/ops_mail \
    && mkdir /data/ops_mail/logs \
    && touch /data/ops_mail/logs/ops_mail.log

ADD . /data/ops_mail/

RUN pip install -r /data/ops_mail/requirements.txt

WORKDIR /data/ops_mail/

CMD ["bash", "/data/ops_mail/run.sh"]
