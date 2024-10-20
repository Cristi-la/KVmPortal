# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

# Wait for PostgreSQL to be ready
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.5
done

echo "PostgreSQL started. Starting Service!"

exec "$@"
