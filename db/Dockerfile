FROM postgres:14.10

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=pysoa
ENV POSTGRES_HOST_AUTH_METHOD=trust

COPY init.sql /docker-entrypoint-initdb.d/