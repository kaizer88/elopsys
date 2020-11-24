#!/bin/bash


ROOT=`git rev-parse --show-toplevel`
cd ${ROOT}
SRC=${ROOT}
SITE_PATH=${SRC}/operations
VENV=${ROOT}/venv

echo "checking for virtualenv"
if [ ! -d ${VENV} ]; then
    cd ${ROOT}
    virtualenv --no-site-packages venv
fi

echo "activate virtualenv"
cd ${VENV}
. ./bin/activate
if [ $? != 0 ]; then
    echo "failed to activate virtualenv at ${VENV}: ABORTING"
    exit 1
fi
cd -

echo "installing requirements"
cd ${ROOT}
if [ ! -f "requirements.txt" ]; then
    echo "No requirement.txt file, incomplete repo"
    exit 1
fi
pip install -r requirements.txt
if [ $? != 0 ]; then
    echo "pip install failed: ABORTING"
    exit 1
fi
cd -

cd ${SITE_PATH}/operations
if [ ! -f "local_settings.py" ]; then
    echo "creating default local_settings.py"
    touch local_settings.py
    echo "Please edit ${SITE_PATH}/operations/local_settings.py and set your database configuration based on ${SITE_PATH}/operations/settings.py. Then re-run this script"
    exit 1
fi
cd -

echo "fixing permissions"
cd ${ROOT}
if [ ! -d logs ]; then
    mkdir logs
fi

# echo "updating database"
# cd ${SITE_PATH}
# python manage.py syncdb
# if [ $? != 0 ]; then
#     echo "syncdb failed: ABORTING"
#     #exit 1
# fi
cd -


cd ${SITE_PATH}
python manage.py migrate #--delete-ghost-migrations
if [ $? != 0 ]; then
    echo "db migrate failed: ABORTING"
    exit 1
fi

echo "Checking if a super user already exists"
cd ${SITE_PATH}
NUM_SUPERUSERS=`echo "Select count(*) from policies_user where is_superuser=1" | python manage.py dbshell | tail -n 1`
if [ ${NUM_SUPERUSERS} == 0 ]; then
    python manage.py createsuperuser
else
    echo "super user already exists"
fi

echo "Creating media folder"
cd ${ROOT}
if [ ! -d "media" ]; then
    mkdir "media"
    sudo chown -R www-data media
fi

echo "Creating statics folder"
cd ${ROOT}
if [ ! -d "statics_collected" ]; then
    mkdir "statics_collected"
    sudo chown -R www-data statics_collected
fi

echo "collecting static files"
cd ${SITE_PATH}
python manage.py collectstatic --noinput --verbosity=0
python manage.py collectstatic_js_reverse
cd -

echo "Deploy local complete"

