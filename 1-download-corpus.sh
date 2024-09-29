#!/bin/bash

#set -x


# script to download solr corpus (per field)
# takes about 1 min, depending on size of corpus and network speeed

FIELDS="title url anchor content"
SOLR_HOST="solrsearch.example.com"
MAX_ROWS=200000
CORPUS_NAME="All_Micro"
INPUT_DIR="input/"

for FIELD in $FIELDS
do
        if [ ! -f $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt ]
        then
        echo "Downloading $FIELD field of $CORPUS_NAME from $SOLR_HOST"
        #/usr/bin/curl -s "http://$SOLR_HOST:8983/solr/$CORPUS_NAME/select?fl=$FIELD&q=$FIELD:*&rows=$MAX_ROWS&wt=csv" > $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
        fi

        if [ $FIELD == "url" ]
        then
                sed -i -e 's|\/| |g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's|https||g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's|assets| |g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's|shelfmark| |g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's|download| |g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's|searchresults| |g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's|browse| |g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's|sort | |g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's|www.example.com||g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's|:||g' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e $'s/^      //g'  $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
                sed -i -e 's/\(.*\)/\L\1/' $INPUT_DIR/${CORPUS_NAME}_${FIELD}.txt
        fi
done
