FROM alpine:3.21.3

EXPOSE 6000 80

ARG DOMAIN_EMAIL
ARG DOMAIN_URL
ENV DOMAIN_EMAIL=$DOMAIN_EMAIL
ENV DOMAIN_URL=$DOMAIN_URL

WORKDIR /certbot
COPY . /certbot

RUN apk add certbot

CMD ["sh", "generate-certificate.sh"]