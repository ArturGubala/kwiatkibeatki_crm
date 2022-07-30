FROM python:3.9.13-alpine3.16
WORKDIR /kb_crm
COPY .requirements/crm-requirements.txt .
RUN pip install -r crm-requirements.txt
COPY app .
COPY entrypoint.sh entrypoint.sh
ENV FLASK_APP=.
ENV FLASK_ENV=development
RUN chmod u+x entrypoint.sh
ENTRYPOINT [ "entrypoint.sh" ]
