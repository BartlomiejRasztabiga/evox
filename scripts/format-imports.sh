#!/usr/bin/env bash

# Exit immediately if command exits with a non-zero status.
set -e

# Print commands and their arguments as they are executed.
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports app
sh ./scripts/format.sh
