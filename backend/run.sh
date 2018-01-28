#!/bin/sh
export PRODUCTION="TRUE"
cd /web/projects/scope-backend/scope/backend
/web/projects/scope-backend/scope/env/bin/gunicorn wsgi -b 127.0.0.1:$PORT -w=15
