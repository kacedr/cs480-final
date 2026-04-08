#!/bin/bash
dropdb --if-exists cs480final
createdb cs480final
psql -d cs480final -f db/schema.sql
psql -d cs480final -f db/seed.sql
echo "Database reset complete."
