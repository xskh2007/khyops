#!/bin/bash
nohup /opt/khyops/venv/bin/python /opt/khyops/manage.py runserver 0.0.0.0:8000 >> /opt/khyops/khyops.log &
nohup /opt/khyops/venv/bin/python /opt/khyops/venv/bin/celery -A khyops worker -l DEBUG >> /opt/khyops/celery.log &