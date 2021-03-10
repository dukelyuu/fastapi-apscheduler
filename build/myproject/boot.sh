#!/bin/bash
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export LANGUAGE=C.UTF-8

# export FLASK_APP=manage.py
# while true; do
#     echo try deploy...
#     /venv/bin/flask deploy
#     if [[ "$?" == "0" ]]; then
#         break
#     fi
#     echo Deploy command failed, retrying in 5 secs...
#     sleep 5
# done
export FLASK_APP=app.py

# 源代码混淆
# echo encrypt python file...
# for cmd in clean compile remove copy cpython
# do
#     echo begin $cmd...
#     /venv/bin/python3 pyc_create.py $cmd ./ --ignore venv .git docs
# done

/venv/bin/flask run --host 0.0.0.0 --port 8080

# /venv/bin/gunicorn -c gunicorn.py app:app
