#!/bin/bash


verif_content(){
    for file in core.py .env conf.py langs.json .gitignore requirements.txt models.py resources.py
    do 
        test -f $1/$file || { echo "$file not found" ; exit 1; }
    done
    
    for dir in public private 
    do 
        test -d $1/assets/$dir || { echo "assets/$dir not found" ; exit 1; }
    done

    test -d $1/templates || { echo "templates not found" ; exit 1; }
}

#### TEST AMPALIBE CREATE #######
ampalibe create test_proj > /dev/null
verif_content test_proj
rm -r test_proj

#### TEST AMPALIBE INIT #######
mkdir test_proj && cd test_proj 
ampalibe init > /dev/null
verif_content .

rm langs.json .env 
#### TEST AMPALIBE LANG #####
ampalibe lang > /dev/null
test -f langs.json || { echo "ampalibe lang not working" ; exit 1; }

#### TEST AMPALIBE ENV #####
ampalibe env > /dev/null
test -f .env || { echo "ampalibe env not working" ; exit 1; }

cd .. && rm -r test_proj

#### TEST AMPALIBE VERSION
ampalibe version > /dev/null || { echo "ampalibe version not working" ; exit 1; }