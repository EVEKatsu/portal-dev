#!/bin/sh

cd /app

pip install -r requirements.txt && \
python manager.py db upgrade && \
python scheduler_by_every_10_minutes.py

if [ $? ]; then
    python app.py
else
    echo "failed setup server environment"
    exit 1
fi