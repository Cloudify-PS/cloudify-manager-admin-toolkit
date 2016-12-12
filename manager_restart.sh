#!/bin/bash

systemctl stop cloudify-webui.service
systemctl stop cloudify-restservice.service
systemctl stop nginx.service
systemctl stop cloudify-mgmtworker.service
systemctl stop cloudify-amqpinflux.service
systemctl stop cloudify-influxdb.service
systemctl stop cloudify-riemann.service
systemctl stop cloudify-rabbitmq.service

systemctl start cloudify-rabbitmq.service
systemctl start cloudify-riemann.service
systemctl start cloudify-influxdb.service
systemctl start cloudify-amqpinflux.service
systemctl start cloudify-mgmtworker.service
systemctl start nginx.service
systemctl start cloudify-restservice.service
systemctl start cloudify-webui.service
