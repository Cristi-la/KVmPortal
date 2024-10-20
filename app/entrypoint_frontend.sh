#!/bin/bash

# If any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# Fail exit if one of your pipe commands fails
set -o pipefail
# Exits if any of your variables is not set
set -o nounset

# Wait for PostgreSQL to be ready
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

sleep 15

rm -rf node_modules package-lock.json
npm install

npm run openapi-ts
echo "Starting React Service!"

exec "$@"
