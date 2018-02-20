#!/bin/bash

EXECUTIONID=${1}
USER=${2}
PASS=${3}
TENANT=${4}

curl http://localhost/executions/${EXECUTIONID} -X PATCH -H "Content-Type: application/json" -d '{"status": "cancelled"}'  -H "tenant:${TENANT}" --user "${USER}:${PASS}"


