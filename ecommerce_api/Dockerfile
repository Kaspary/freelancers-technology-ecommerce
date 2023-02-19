FROM python:3.10

WORKDIR /usr/src/app

ARG DJANGO_ADMIN_USER
ARG DJANGO_ADMIN_PASSWORD

ENV DJANGO_SUPERUSER_USER=$DJANGO_ADMIN_USER
ENV DJANGO_SUPERUSER_PASSWORD=$DJANGO_ADMIN_PASSWORD

COPY ./ .

RUN python3 -m pip install --user --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

EXPOSE 8000

CMD ["bash", "entrypoint.sh"]