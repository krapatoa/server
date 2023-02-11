#!/bin/bash
set -x
gunicorn -w 4 --bind 0.0.0.0:5000 --preload -c hooks.py wsgi:app
