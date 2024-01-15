import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from collections import Counter

#Delete certain quotation marks from a dataframe
def replaceQuotationMarks(dataframe):

    print(dataframe)
    quotation_list = ["'", "’", "‘", "–", "``", "—", "''"]
    dataframe = dataframe.replace(quotation_list, "deleteThis")
    dataframe.drop(dataframe[dataframe.keyword == 'deleteThis'].index, inplace=True)
    print(dataframe)
    return dataframe

#Count the keywords in the list, convert the list to a counter series and convert the series into a pandas dataframe including keyword and count
def countKeywords(keyword_list):

    word_counts = Counter(keyword_list)
    word_counts_df = pd.DataFrame({'keyword':word_counts.keys(), 'count':word_counts.values()})
    sorted_word_counts = word_counts_df.sort_values(by='count', ascending=False)
    return sorted_word_counts


#Filter the list of titles into keywords and return them in a list
def filterKeywords(title_list):

    #Convert the list into a series to work in pandas
    series = pd.Series(title_list)
    #Create the set of words to filter out
    stop_words = set(stopwords.words('english') + list(string.punctuation) + list(string.digits) + ['...', "'s",])
    #Tokenize each word using nltk and then remove junk words and punctuation (I, can, so, ?, etc...)
    tokenized_series = series.apply(lambda x: [word.lower() for word in word_tokenize(x) if word.lower() not in stop_words])
    keyword_list = sum(tokenized_series, [])
    keyword_list = list(filter(bool, keyword_list))
    return keyword_list

#Calls the filter and count keyword functions and returns the resulting dataframe
def processKeywords(title_list):

    keyword_list = filterKeywords(title_list)
    keyword_dataframe = countKeywords(keyword_list)
    keyword_dataframe = replaceQuotationMarks(keyword_dataframe)
    return keyword_dataframe