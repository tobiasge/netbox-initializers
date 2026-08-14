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
  $doco run --rm netbox /opt/netbox/docker-entrypoint.sh ./manage.py check || exit 1
}

test_cleanup() {
  gh_echo "::group::Clean test environment"
  echo "💣 Cleaning Up"
  if [ "$KEEP_VOLUMES" == "true" ]; then
    $doco down
  else
    $doco down -v
  fi

  if [ -d "${INITIALIZERS_DIR}" ]; then
    rm -rf "${INITIALIZERS_DIR}"
  fi
  gh_echo "::endgroup::"
}

test_initializers() {
  echo "🏭 Testing Initializers"
  $doco run --rm netbox ./manage.py load_initializer_data --path /etc/netbox/initializer-data || exit 1
}

test_api_verification() {
  echo "🔍 Verifying data via NetBox API"

  # Start the NetBox web server so the REST API is available
  $doco up -d netbox || exit 1

  # Wait for the API to become available
  echo "⏳ Waiting for the NetBox API to be ready"
  for _ in $(seq 1 30); do
    if $doco exec -T netbox python3 -c \
      "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/')" \
      >/dev/null 2>&1; then
      echo "✅ NetBox API is ready"
      break
    fi
    sleep 5
  done

  # Copy the verification script into the running container and run it
  $doco cp ./verify_api.py netbox:/tmp/verify_api.py || exit 1
  $doco exec -T netbox python3 /tmp/verify_api.py || exit 1
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

gh_echo "::group::API verification"
test_api_verification
gh_echo "::endgroup::"

echo "🐳🐳🐳 Done testing"
