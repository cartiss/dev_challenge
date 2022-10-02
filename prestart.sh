#! /usr/bin/env bash

sleep 10;
python trust_network/manage.py makemigrations

sleep 10;
python trust_network/manage.py migrate

sleep 10;
python trust_network/manage.py runserver 0.0.0.0:8000