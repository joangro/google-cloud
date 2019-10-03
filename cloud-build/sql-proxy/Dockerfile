FROM ubuntu

RUN apt-get update && apt-get install -y postgresql-client

ENTRYPOINT ["/bin/bash", "-c"]

CMD ["psql", "--version"]
