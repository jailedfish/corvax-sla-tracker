rm -rf /etc/letsencrypt/live/certfolder*

certbot certonly -v --manual --manual-auth-hook /etc/letsencrypt/acme-dns-auth.py --preferred-challenges dns --debug-challenges --email $DOMAIN_EMAIL -d $DOMAIN_URL --cert-name=certfolder --key-type rsa --agree-tos --http-01-port 81

cp /etc/letsencrypt/live/certfolder*/fullchain.pem /var/certs/cert.pem
cp /etc/letsencrypt/live/certfolder*/privkey.pem /var/certs/key.pem
