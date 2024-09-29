import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import re
import glob
#os.system("taskset -p 0xff %d" % os.getpid())

#!pip3 install nltk spacy scikit-learn
#!python3 -m spacy download en_core_web_sm

import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import spacy


# TUNABLES
fields = [ 'title','url','anchor','content']
#fields = [ 'title','anchor']
input_corpus = 'All_Micro'
output_corpus = 'All_Micro'
n=2000 # numner of files to split corpus into
input_dir="input/"
output_dir="output/"
ext = ('.part')
utf8_command="/usr/bin/iconv -c -f utf-8 -t utf-8 "
move_command="/bin/mv "
regex_patterns = [ r'collectionall', r'querysearch',r'coursespostgraduate',r'coursesstaffaz',r'mapsresearch',r'expertiselibrary',r'bbiiooddiivveerrssiittyy',r'rreesseeaarrcchh',r'nneewwsslleetttteerr',r'cataloguelibrary',r'mapsresearch', r'cataloguetara',r'skip',r'eecm',r'cookies',r'main',r'menu',r'geocode',r'permalink' ]

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Download stopwords if not already present
nltk.download('stopwords')

# Function to extract keywords and n-grams
def extract_keywords_and_ngrams(text, ngram_range=(1, 3), top_n=20):
    # Tokenization and stopword removal using spaCy
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not token.is_stop and token.is_alpha]

    # Join the tokens back into a string for vectorization
    processed_text = ' '.join(tokens)

    # Use CountVectorizer to get n-grams
    vectorizer = CountVectorizer(ngram_range=ngram_range)
    X = vectorizer.fit_transform([processed_text])

    # Get the frequency of each n-gram
    ngram_counts = X.toarray().sum(axis=0)
    ngrams = vectorizer.get_feature_names_out()

    # Combine n-grams with their frequencies and sort them
    ngram_freq = sorted(zip(ngrams, ngram_counts), key=lambda x: x[1], reverse=True)

    # Get the top N keywords and n-grams
    top_ngrams = ngram_freq[:top_n]

    return top_ngrams

# Function to read the book text from a file
def read_book(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# 851305068 exceeds maximum of 1000000
#nlp.max_length = 851305069
nlp.max_length=8497018


import os

def split_file(file_path, n):
    # Ensure n is a positive integer
    if n <= 0:
        raise ValueError("Number of parts (n) must be a positive integer.")

    # Get the size of the file
    file_size = os.path.getsize(file_path)

    # Calculate the size of each part
    part_size = file_size // n
    remaining_size = file_size % n

    # Open the input file
    with open(file_path, 'rb') as input_file:
        for i in range(n):
            # Calculate the size for this part
            current_part_size = part_size + (1 if i < remaining_size else 0)

            # Read the part data
            part_data = input_file.read(current_part_size)

            # Write the part to a new file
            part_file_path = f'{file_path}_{i+1}.part'
            with open(part_file_path, 'wb') as part_file:
                part_file.write(part_data)

            #print(f'Created: {part_file_path} (Size: {current_part_size} bytes)')




from collections import defaultdict
def process_file(input_file, output_file):
    # Dictionary to accumulate frequencies
    frequency_dict = defaultdict(int)

    # Open the input file and process it
    with open(input_file, 'r') as f:
        for line in f:
            # Split the line into term and frequency
            term, frequency = line.strip().split(':')
            # Convert frequency to an integer and accumulate
            frequency_dict[term.strip()] += int(frequency.strip())

    # Write the results to the output file
    with open(output_file, 'w') as f:
        for term, total_frequency in frequency_dict.items():
            f.write(f"{term}: {total_frequency}\n")


def convert_utf8(utf8_command, move_command, input_file):
    execute = os.system(f"{utf8_command} {input_dir}{input_file} > {input_dir}{input_file}.tmp")
    execute = os.system(f"{move_command} {input_dir}{input_file}.tmp {input_dir}{input_file}")
    if execute == 0:
        pass
        #print("Successfully Converted to UTF8:  "+input_file)
    else:
        print("Conversion to UTF8 Failed: "+input_file)




def inline_replace_colon_with_tab(file_path):
    # Open the file for reading
    with open(file_path, 'r') as file:
        # Read the file
        filecontent = file.read()

    # Replace ": " with a tab
    modified_content = re.sub(r':\s', '\t', filecontent)

    # Write the modified filecontent back to the same file
    with open(output_file, 'w') as file:
        print("replacing colon with space")
        file.write(modified_content)




def inline_delete_lines_with_regex(file_path, regex_patterns):
    # Open the file and read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Compile regex patterns for efficiency
    compiled_patterns = [re.compile(pattern) for pattern in regex_patterns]

    # Filter out lines that contain any of the regex patterns
    filtered_lines = []
    for line in lines:
        if not any(pattern.search(line) for pattern in compiled_patterns):
            filtered_lines.append(line)

    # Write the filtered lines back to the same file
    print("Deleting lines with regular expressions like coursesstaffaz")
    with open(file_path, 'w') as file:
        file.writelines(filtered_lines)


def inline_sort_last_column(filename):
    print ('Sorting file' +filename+ ' by frequency of occurance')
    with open(filename, 'r') as file:
        lines = file.readlines()
    # Split the lines into columns and sort by the last column (numerically)
    sorted_lines = sorted(lines, key=lambda line: float(line.strip().split()[-1]),reverse=True)
    # Write the sorted lines back to the file
    with open(filename, 'w') as file:
        file.writelines(sorted_lines)



def delete_files_with_extension(directory, extension):
    # Construct the search pattern
    pattern = os.path.join(directory, f'*.{extension}')
    # Get all files that match the extension
    files = glob.glob(pattern)
    # Loop through the files and delete them
    for file in files:
        try:
            os.remove(file)
            print(f"{file} has been deleted successfully.")
        except Exception as e:
            print(f"Error occurred while deleting {file}: {e}")








# main
if __name__ == "__main__":
    for field in fields:
        input_file = ('input/'+input_corpus+'_'+field+'.txt')
        output_file_tmp = ('output/'+output_corpus+'_'+field+'.txt.tmp')
        output_file = ('output/'+output_corpus+'_'+field+'.txt')
        open(output_file, 'w').close()
        open(output_file_tmp, 'w').close()

        parts=str(n)  # Number of parts to split the file into
        print ('Splitting file into ' +parts+ ' parts')
        split_file(input_file, n)


        # iterating over all files
        for file in os.listdir(input_dir):
            if re.search(field, file):
                if file.endswith(ext):
                    #print(file)  # printing file name of desired extension
                    convert_utf8(utf8_command, move_command, file)
                    # Read the book
                    print ('Reading Book '+file+' :')
                    book_text = read_book(input_dir+file)

                    # Extract keywords and n-grams
                    print ("keywords and n-gram extraction")
                    try:
                        keywords_and_ngrams = extract_keywords_and_ngrams(book_text, ngram_range=(1, 3), top_n=2000)
                    except:
                        pass

                    # Print the results
                    with open(output_file_tmp, 'a') as f:
                        for ngram, freq in keywords_and_ngrams:
                            print(f"{ngram}: {freq}",file=f)

                    # accumulate frequency scores for split files
                    process_file(output_file_tmp, output_file)
            # format files
            inline_replace_colon_with_tab(output_file)
            inline_delete_lines_with_regex(output_file, regex_patterns)
            inline_sort_last_column(output_file)

    print ('Cleaning up temp files in ' +output_dir+' and in '+input_dir)
    delete_files_with_extension(input_dir, "part")
    delete_files_with_extension(output_dir, "tmp")
