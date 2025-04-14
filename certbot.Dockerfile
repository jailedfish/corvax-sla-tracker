FROM alpine:3.21.3

EXPOSE 6000 80

ARG DOMAIN_EMAIL
ARG DOMAIN_URL
ENV DOMAIN_EMAIL=$DOMAIN_EMAIL
ENV DOMAIN_URL=$DOMAIN_URL

WORKDIR /certbot

RUN apk add certbot
RUN mkdir -p /etc/letsencrypt && wget -O /etc/letsencrypt/acme-dns-auth.py https://github.com/joohoi/acme-dns-certbot-joohoi/raw/master/acme-dns-auth.py && chmod +x /etc/letsencrypt/acme-dns-auth.py
COPY . /certbot
CMD ["sh", "generate-certificate.sh"]
