FROM mysql:8.0

COPY containers/mysql/my.cnf /etc/mysql/conf.d/my.cnf
COPY containers/mysql/init.sql /docker-entrypoint-initdb.d

