#!/usr/bin/env bash

set -xe

if [[ -z "$PROJECT_PATH" ]]; then
    echo "Error: PROJECT_PATH is missed or empty"
    exit 1
fi

if [[ -z "$CI_COMPONENTS_PATH" ]]; then
    echo "Error: CI_COMPONENTS_PATH is missed or empty"
    exit 1
fi

output=$("$CI_COMPONENTS_PATH"/scripts/fmt/verify_license.py --path "$PROJECT_PATH" 2>&1 || exit 1)
if [ -n "$output" ]; then
  echo "Error: Some files are missing the Apache 2.0 license header:"
  echo "$output"
  exit 1
fi
