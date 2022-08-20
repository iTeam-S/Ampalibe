#!/bin/bash

function simulate {
    echo $(curl -H "Content-Type: application/json" -X POST "http://127.0.0.1:4555/?testmode=1" -d "{\"object\": \"page\", \"entry\": [{\"messaging\": [ {\"sender\": {\"id\": \"test_user\"}, \"message\": {\"text\":$1} }]}]}")
}

####### PAYLOAD TEST #######
payload0=`simulate '"/set_my_name"'`
myname=$(simulate $payload0)
if [ $myname = '"Ampalibe"' ]
then
    echo "Message: OK Payload"
else
    echo KO
    exit 1
fi

####### ACTION TEST && Temporary data TEST #######
simulate '"/try_action"' > /dev/null
res=$(simulate '"Hello"')
if [ $res = '"Hello Ampalibe"' ]; then
    echo "Message: OK Action"
    echo "Message: OK Temporary data"
else
    echo KO
    exit 1
fi



