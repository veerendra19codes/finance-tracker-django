#!/bin/bash
source /path/to/virtualenv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate



// "src": "build_files.sh",
// "use": "@vercel/static-build",
// "config": {
//     "distDir": "staticfiles_build"
// }