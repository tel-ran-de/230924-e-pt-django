#!/bin/sh

host="$1"
port="$2"

echo "Waiting for database at $host:$port..."

while ! nc -z "$host" "$port"; do
  sleep 1
done

echo "Database is up - continuing."
