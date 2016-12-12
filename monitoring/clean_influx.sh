#!/bin/bash
systemctl stop cloudify-influxdb.service
rm -rf /opt/influxdb/shared/data/*
systemctl start cloudify-influxdb.service
#curl -X POST "http://localhost:8086/db?u=root&p=root" -d "{\"name\": \"cloudify\"}"
