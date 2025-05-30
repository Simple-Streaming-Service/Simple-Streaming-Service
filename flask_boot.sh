#!/bin/bash
exec gunicorn -b localhost:5000 flask_wsgi:app