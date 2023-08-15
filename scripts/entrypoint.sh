#!/bin/bash
set -x

echo Starting ETL using parameters: "$@"
poetry run python -m etl "$@"
echo "ETL completed"

