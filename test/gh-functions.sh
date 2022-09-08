#!/bin/bash

###
# A regular echo, that only prints if ${GITHUB_ACTIONS} is defined.
###
gh_echo() {
  if [ -n "${GITHUB_ACTIONS}" ]; then
    echo "${@}"
  fi
}

###
# Prints the output to the file defined in ${GITHUB_ENV}.
# Only executes if ${GITHUB_ACTIONS} is defined.
# Example Usage: gh_env "FOO_VAR=bar_value"
###
gh_env() {
  if [ -n "${GITHUB_ACTIONS}" ]; then
    echo "${@}" >>"${GITHUB_ENV}"
  fi
}
