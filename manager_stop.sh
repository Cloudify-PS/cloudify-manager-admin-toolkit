#!/bin/bash
systemctl stop cloudify-webui.service
systemctl stop cloudify-restservice.service
systemctl stop nginx.service
systemctl stop cloudify-mgmtworker.service
systemctl stop cloudify-amqpinflux.service
systemctl stop cloudify-influxdb.service
systemctl stop cloudify-riemann.service
systemctl stop cloudify-rabbitmq.service

