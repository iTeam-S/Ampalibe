#!/bin/bash

function simulate {
    echo $(curl -H "Content-Type: application/json" -X POST "http://127.0.0.1:4555/?testmode=1" -d "{\"object\": \"page\", \"entry\": [{\"messaging\": [ {\"sender\": {\"id\": \"test_user\"}, \"message\": {\"text\":$1} }]}]}")
}

function no_simulate  {
        echo $(curl -H "Content-Type: application/json" -X POST "http://127.0.0.1:4555/" -d "{\"object\": \"page\", \"entry\": [{\"messaging\": [ {\"sender\": {\"id\": \"test_user\"}, \"message\": {\"text\":$1} }]}]}")

}

####### PAYLOAD TEST #######
payload0=`simulate '"/set_my_name"'`
myname=$(simulate $payload0)
if [ "$myname" = '"Ampalibe"' ]
then
    echo "Message: OK Payload"
else
    echo KO
    exit 1
fi

####### ACTION TEST && Temporary data TEST #######
simulate '"/try_action"' > /dev/null
res=$(simulate '"Hello"')
if [ "$res" = '"Hello Ampalibe"' ]; then
    echo "Message: OK Action"
    echo "Message: OK Temporary data"
else
    echo KO
    exit 1
fi

####### ACTION TEST && Payload data TEST #######
simulate '"/try_second_action"' > /dev/null
res=$(simulate '"Hello"')
if [ "$res" = '"Hello Ampalibe2"' ]; then
    echo "Message: OK Second Action"
    echo "Message: OK Payload data in action"
else
    echo KO
    exit 1
fi


### utils TEST: translate, simulate, download_file ####
res0=$(simulate '"/lang"')
no_simulate $res0 > /dev/null
sleep 2

res=$(simulate '"/lang/test"')
if [ "$res" = '"Hello World"' ]; then
    echo "Message: OK translate - simulate - download_file"
else
    echo KO
    exit 1
fi




