rm -rf /etc/letsencrypt/live/certfolder*

certbot certonly --standalone --email $DOMAIN_EMAIL -d $DOMAIN_URL --cert-name=certfolder --key-type rsa --agree-tos

cp /etc/letsencrypt/live/certfolder*/fullchain.pem /var/certs/cert.pen
cp /etc/letsencrypt/live/certfolder*/privkey.pem /var/certs/key.pem