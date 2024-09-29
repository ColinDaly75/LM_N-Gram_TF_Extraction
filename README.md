# LM_N-Gram_TF_Extraction
Using Language Modelling to Extracting Terms, Frequencies and NGrams from fields in a Solr Corpus

# Requirements
Access to a Solr Corpus


# run order
```
# ./1-download-corpus.sh
# ./2-extract-tf.py

```


# Output
The output is of the form:
```TERM  FREQUENCY```

or

```N-GRAM FREQUENCT```

For example, using a field from my own corpus, here the top 15 terms:
```
# head -15 ${CORPUS}_${FIELD}.txt
events  9354
pdf     7396
library 7214
research        5883
undergraduate   5069
news    4578
event   4241
events event    4172
articles        4011
committeepapers 3173
event events    2810
events event events     2794
people  2779
event events event      2763
tag     2735
manuscripts     2717
blog    2671
browse  2633
sort    2603
```
