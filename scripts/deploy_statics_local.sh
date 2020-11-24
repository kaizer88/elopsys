#!/bin/bash


ROOT=`git rev-parse --show-toplevel`
cd ${ROOT}
SRC=${ROOT}
SITE_PATH=${SRC}/operations
VENV=${ROOT}/venv
GIT_HASH=`git log --format="%H" -n 1`

echo "collecting static files"
cd ${SITE_PATH}
python manage.py collectstatic --noinput --verbosity=0
python manage.py collectstatic_js_reverse
cp ${ROOT}/statics_collected/${GIT_HASH}/django_js_reverse/js/reverse.js ${SITE_PATH}/statics/js/dj-reverse.js
cd -

echo "Statics deploy complete"
