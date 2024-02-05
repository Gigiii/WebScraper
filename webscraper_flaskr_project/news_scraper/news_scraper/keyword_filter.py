import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from collections import Counter

# Delete certain quotation marks from a dataframe
def replaceQuotationMarks(dataframe):
    """
    Replaces specific quotation marks in the given dataframe with a placeholder.

    Args:
        dataframe (pandas.DataFrame): The input dataframe.

    Returns:
        pandas.DataFrame: The modified dataframe with quotation marks replaced.
    """
    print(dataframe)
    quotation_list = ["'", "’", "‘", "–", "``", "—", "''"]
    dataframe = dataframe.replace(quotation_list, "deleteThis")
    dataframe.drop(dataframe[dataframe.keyword == 'deleteThis'].index, inplace=True)
    print(dataframe)
    return dataframe

# Count the keywords in the list, convert the list to a counter series,
# and convert the series into a pandas dataframe including keyword and count
def countKeywords(keyword_list):
    """
    Counts the occurrences of keywords in the given list and creates a dataframe.

    Args:
        keyword_list (list): List of keywords.

    Returns:
        pandas.DataFrame: Dataframe with keyword and count columns.
    """
    word_counts = Counter(keyword_list)
    word_counts_df = pd.DataFrame({'keyword': word_counts.keys(), 'count': word_counts.values()})
    sorted_word_counts = word_counts_df.sort_values(by='count', ascending=False)
    return sorted_word_counts

# Filter the list of titles into keywords and return them in a list
def filterKeywords(title_list):
    """
    Filters out stopwords and punctuation from a list of titles.

    Args:
        title_list (list): List of titles.

    Returns:
        list: List of filtered keywords.
    """
    # Convert the list into a series to work in pandas
    series = pd.Series(title_list)
    # Create the set of words to filter out
    stop_words = set(stopwords.words('english') + list(string.punctuation) + list(string.digits) + ['...', "'s"])
    # Tokenize each word using nltk and then remove junk words and punctuation
    tokenized_series = series.apply(lambda x: [word.lower() for word in word_tokenize(x) if word.lower() not in stop_words])
    keyword_list = sum(tokenized_series, [])
    keyword_list = list(filter(bool, keyword_list))
    return keyword_list

# Calls the filter and count keyword functions and returns the resulting dataframe
def processKeywords(title_list):
    """
    Processes a list of titles to generate a dataframe with keyword counts.

    Args:
        title_list (list): List of titles.

    Returns:
        pandas.DataFrame: Dataframe with keyword counts.
    """
    keyword_list = filterKeywords(title_list)
    keyword_dataframe = countKeywords(keyword_list)
    keyword_dataframe = replaceQuotationMarks(keyword_dataframe)
    return keyword_dataframe