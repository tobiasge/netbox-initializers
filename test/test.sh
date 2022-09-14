#!/bin/bash

# shellcheck disable=SC1091
source ./gh-functions.sh

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
  $doco build --no-cache || exit 1
}

test_cleanup() {
  gh_echo "::group::Clean test environment"
  echo "💣 Cleaning Up"
  $doco down -v

  if [ -d "${INITIALIZERS_DIR}" ]; then
    rm -rf "${INITIALIZERS_DIR}"
  fi
  gh_echo "::endgroup::"
}

test_initializers() {
  echo "🏭 Testing Initializers"
  $doco run --rm netbox /opt/netbox/docker-entrypoint.sh ./manage.py load_initializer_data --path /etc/netbox/initializer-data || exit 1
}

echo "🐳🐳🐳 Start testing"

# Make sure the cleanup script is executed
trap test_cleanup EXIT ERR

gh_echo "::group::Setup test environment"
test_setup
gh_echo "::endgroup::"

gh_echo "::group::Initializer tests"
test_initializers
gh_echo "::endgroup::"

echo "🐳🐳🐳 Done testing"
