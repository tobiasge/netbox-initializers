#!/bin/bash

# The docker compose command to use
doco="docker compose --project-name netbox_initializer_test"

INITIALIZERS_DIR="initializer-data"

test_setup() {
  echo "🏗 Setup up test environment"
  if [ -d "${INITIALIZERS_DIR}" ]; then
    rm -rf "${INITIALIZERS_DIR}"
  fi

  mkdir "${INITIALIZERS_DIR}"
  (
    cd ../src/netbox_initializers/initializers/yaml/ || exit
    for script in *.yml; do
      sed -E 's/^# //' "${script}" >"../../../../test/${INITIALIZERS_DIR}/${script}"
    done
  )
  $doco build --no-cache
}

test_cleanup() {
  echo "💣 Cleaning Up"
  $doco down -v

  if [ -d "${INITIALIZERS_DIR}" ]; then
    rm -rf "${INITIALIZERS_DIR}"
  fi
}

test_initializers() {
  echo "🏭 Testing Initializers"
  $doco run --rm netbox /opt/netbox/docker-entrypoint.sh ./manage.py load_initializer_data --path /etc/netbox/initializer-data
}

echo "🐳🐳🐳 Start testing"

# Make sure the cleanup script is executed
trap test_cleanup EXIT ERR
test_setup

test_initializers

echo "🐳🐳🐳 Done testing"
