#!/usr/bin/env bash

# Let the DB start
python ./app/pre_start.py

# Run migrations
alembic upgrade head
