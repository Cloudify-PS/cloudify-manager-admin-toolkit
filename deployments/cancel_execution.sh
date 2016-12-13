#!/bin/bash

EXECUTIONID=${1}

curl http://localhost/executions/${EXECUTIONID} -X PATCH -H "Content-Type: application/json" -d '{"status": "cancelled"}'

