#!/usr/bin/env bash

# Print commands and their arguments as they are executed.
set -x

mypy app
black app --check
isort --check-only app
flake8
