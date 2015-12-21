#!/usr/bin/env bash

flyway -url=jdbc:postgresql://$DB_PORT_5432_TCP_ADDR:5432/postgres -user=postgres migrate
