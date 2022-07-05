#!/bin/sh
flask db migrate
flask db upgrade
flask run --host="${HOST}"
