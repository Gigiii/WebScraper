import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from collections import Counter

#Delete the quotation marks in a text
def replaceQuotationMarks(text):
    return text.replace("'", "").replace("’", "").replace("‘", "").replace("–", "").replace("``", "")

#Count the keywords in a list and convert the series into a pandas dataframe including keyword and count
def countKeywords(keyword_list):
    word_counts = Counter(keyword_list)
    word_counts_df = pd.DataFrame({'keyword':word_counts.keys(), 'count':word_counts.values()})
    sorted_word_counts = word_counts_df.sort_values(by='count', ascending=False)
    return sorted_word_counts


#Filter the list of titles for keywords and return them in a list
def filterKeywords(title_list):
    #Convert the list into a series to work in pandas
    series = pd.Series(title_list)
    #Create the set of words to filter out
    stop_words = set(stopwords.words('english') + list(string.punctuation) + list(string.digits) + ['...', "'s",])
    #Tokenize each word using nltk and then remove junk words and punctuation (I, can, so, ?, etc...)
    tokenized_series = series.apply(lambda x: [word.lower() for word in word_tokenize(x) if word.lower() not in stop_words])
    keyword_list = sum(tokenized_series, [])
    keyword_list = list(map(replaceQuotationMarks, keyword_list))
    keyword_list = list(filter(bool, keyword_list))
    return keyword_list

#Calls the filter and count keyword functions and returns the resulting dataframe
def processKeywords(title_list):
    keyword_list = filterKeywords(title_list)
    keyword_dataframe = countKeywords(keyword_list)
    return keyword_dataframe