#!/bin/bash

gunicorn --log-level debug --reload --bind 0.0.0.0:8080 --timeout=15 --worker-class=uvicorn.workers.UvicornWorker --keep-alive 60 --workers 4 apptodolist.web:app
