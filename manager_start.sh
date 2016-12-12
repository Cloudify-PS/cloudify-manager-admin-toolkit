#!/bin/bash
systemctl start cloudify-rabbitmq.service
systemctl start cloudify-riemann.service
systemctl start cloudify-influxdb.service
systemctl start cloudify-amqpinflux.service
systemctl start cloudify-mgmtworker.service
systemctl start nginx.service
systemctl start cloudify-restservice.service
systemctl start cloudify-webui.service

