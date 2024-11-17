FROM owasp/modsecurity-crs:4.8.0-nginx-202411071011
RUN mv /etc/modsecurity.d/owasp-crs/rules/* /tmp/*
COPY rules /etc/modsecurity.d/owasp-crs/rules/
COPY default.conf.template /etc/nginx/templates/conf.d/default.conf.template