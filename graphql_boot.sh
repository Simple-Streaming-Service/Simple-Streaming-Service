#!/bin/bash
exec hypercorn -b localhost:5001 graphql_asgi:app