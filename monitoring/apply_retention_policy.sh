#!/bin/bash

POLICY=${1}

echo curl -X POST "http://localhost:8086/cluster/database_configs/cloudify?u=root&p=root"­databinary @${POLICY}
