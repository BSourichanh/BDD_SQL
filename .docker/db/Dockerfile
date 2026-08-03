FROM mysql:8.0
ENV MYSQL_ROOT_PASSWORD helloworld
COPY setup.sql /docker-entrypoint-initdb.d/
RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/
VOLUME .:/home/wwwroot
