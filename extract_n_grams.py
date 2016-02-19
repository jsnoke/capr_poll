import sys
sys.path.append('./text_utils/')
import os
from text_utils import n_grams
import io
from spacy.en import English
from nltk.corpus import stopwords
import re
import csv


def extract_capr_n_grams(n, outfile, infile, stopwords, col_idx):
    '''
    Args:
    -----
    n: n in n_grams
    outfile: path to write the output to
    infile: path to original data
    stopwords: A list of stopwords
    col_idx: The colum indeces of questions to be extracted (0 indexed)
    '''
    
    with io.open(infile_path, 'r', encoding='utf-8') as infile:
        
        rowreader = csv.reader(infile, delimiter=',', quotechar='"')
        
        # Prepare outfile 
        out = io.open(outfile, 'w+', encoding='utf-8')
        header = 'question,caseid,text\n'
        out.write(unicode(header))
        
        for i, cells in enumerate(rowreader):
                
            # Get colnames
            if i == 0:
                q_ids = [cells[i].strip('"') for i in col_idx]
                continue
                
            # Select relevant fields
            id_ = cells[0]
            text_fields = [unicode(cells[i]) for i in col_idx]
            
            # Process each text field
            for c_idx,text in enumerate(text_fields):
                
                # Remove non-alpha numeric characters and excess
                # space
                text = non_alpha.sub('', text)
                text = non_alpha.sub(' ', text)
                
                # Generate lemmatized n_grams
                ngrams = n_grams(text, parser=parser, n=n, stemmer=None, 
                                 stopwords=stopwords, lemmatize=True)
                
                
                # Generate line to write to outfile
                if ngrams is None:
                    out_text = ''
                else:
                    out_text = ' '.join(ngrams)
                out_line = '{},{},{}\n'.format(q_ids[c_idx],id_, out_text)
                # Write to connection
                out.write(unicode(out_line))
                
                
        # Close out connection    
        out.close()
            
        
# Initialize spacy english parser
parser = English()


# Set up parameters
infile_path = 'data/capr_data.csv'
outfile_dir = 'data/preproc_answers_no_manual_check/'

#sw = stopwords.words('english')
sw= None
excess_space = re.compile(r'\s+')
non_alpha = re.compile(r'[^A-Za-z0-9 ]')
# Columns to be extracted
col_idx = [4,6,8,10,13,15,17,19,23,25,27,28]

# n in grams
ns = [1,2,3,4,5]

for n in ns:
    
    print('Extracting {}_grams'.format(n))
    # Make file for parameter value
    if sw is None:
        fname = '{}_grams_text_answers.txt'.format(n)
    else:
        fname = '{}_grams_text_answers_no_stopwords.txt'.format(n)

    outfile_path = os.path.join(outfile_dir,fname)
    
    # Generate n_grams
    extract_capr_n_grams(n, outfile_path, infile_path, sw, col_idx)
