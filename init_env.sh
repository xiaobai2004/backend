#!/usr/bin/env bash
app_dir=`dirname $0`
cd $app_dir

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
