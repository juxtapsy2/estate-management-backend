#!/bin/bash

set -o errexit

set -o pipefail

set -o nounset

python << END
import sys
import time
import psycopg2
suggest_uncoverable_after = 30
start = time.time()
while True:
    try:
        psycopg2.connect(
            dbname="${POSTGRE_DB}"
            user="${POSTGRE_USER}"
            password="${POSTGRE_PASSWORD}"
            host="${POSTGRE_HOST}"
            port="${POSTGRE_PORT}"
        )
        break
    except psycopg2.OperationalError as error:
        sys.stderr.write("Waiting for PostgreSQL to be available...\n")
        if time.time() - start > suggest_uncoverable_after:
            sys.stderr.write("This is taking longer than expected. The following exception
            may be indication of an unrecoverable error: '{}'\n".format(error))
            time.sleep(1)
END

>&2 echo "PostgresSQL is available"

exec "$@"