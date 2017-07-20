#!/usr/bin/env bash

appdir=`dirname $0`
start_url=$1

count=0

while [ true ]; do

    if [ "" !=  "$start_url" ]; then
        echo "================================================================================"
        echo "start url found $start_url"
        echo "================================================================================"
        url=$start_url
        start_url=""
        ls '/var/tmp/sina_docx/*' | xargs rm -f

    else
        afile=`ls /var/tmp/sina_docx/* | grep 'prev' | grep -v 'grep'`
        if [ -n afile ]; then
            url=`cat $afile | tail -1`
        fi
        rm -f $afile

        if [ "" = "$url" ]; then
            echo "================================================================================"
            echo "Finished crawling"
            echo "================================================================================"
            exit 0
        else
            echo "================================================================================"
            echo "next url found: $url"
            echo "================================================================================"
        fi

    fi

    echo "[`date`] start to crawl '$url' .... " 
    python $appdir/sina.py  $url

    python $appdir/text2docx.py
    echo "[`date`] finished to crawl '$url' "
    url=""
    ls /var/tmp/sina_docx/* | grep -v prev | xargs rm -f

    count=$((count + 1))
    if [ $count -gt 10 ]; then
        exit 0
    fi

    sleep $((RANDOM % 5 + 5 ))

done
