#!/bin/bash
exec gunicorn -b localhost:5000 wsgi:app