import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
from collections import Counter

def replaceQuotationMarks(text):
    return text.replace("'", "").replace("’", "")

#Count the keywords in a list and convert the series into a pandas dataframe including keyword and count
def countKeywords(keyword_list):
    word_counts = Counter(keyword_list)
    word_counts_df = pd.DataFrame.from_dict(word_counts, orient='index', columns=['count'])
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

# #testing the functions (uncomment for development purposes)
# list_test = ['Israeli tanks reported near Khan Younis as civilians urged to flee', 'Hamas planned rape as weapon of war - Israeli lawyer', 'Head of UN talks hits back in climate science row', "Ukraine war: Soldier tells BBC of river battle 'hell'", 'Eleven hikers killed as Indonesia volcano erupts', 'Florence Pugh hit by thrown object during film promo', "Mother of Paris suspect 'raised concern' before attack", 'Moment huge WW2 bomb detonates off coast of Denmark', 'Ryanair denies it is charging for e-boarding passes', 'Venezuelans back claim to Guyana-controlled region', "Attenborough ship encounters world's largest iceberg", 'Venezuelans back claim to Guyana-controlled region', "Attenborough ship encounters world's largest iceberg", 'Gold Coast scraps bid for 2026 Commonwealth Games', 'Spotify to axe 1,500 workers to cut costs', 'Five bodies found in crashed US aircraft near Japan', 'Injured and alone: The pain of Gaza’s orphans', 'Bowen: US sets clearer red lines for Israel as ceasefire ends', 'Why has the Gaza ceasefire come to an end?', "'A very desperate situation for the population of Gaza'", "'I’m not ready to lose hope': The hostages still in Gaza", 'Rizz named word of year. So what is it and who has it?', 'BBC World News TV', 'BBC World Service Radio', "Couple's property ordeal captivates Chinese internet", 'How do you transport two giant pandas?', 'Murders, hitmen and South Africa’s election', 'How weather apps are trying to be more accurate', "Meet the designer behind Beyoncé's neon green sari", 'Tanzania leader to leave COP to deal with flooding', 'Billie Eilish hits back at sexuality questions', 'Hong Kong activist Agnes Chow jumps bail', 'Watch: A dusty, foggy end for power station towers', "Raw sewage 'cover-up' at World Heritage Site", "Mandela's granddaughter slams 'climate apartheid'", 'Watch how heavy snowfall paralysed Europe', 'Native Americans are reclaiming energy', 'How Salesforce reached its net zero goals', 'How far would you walk for a cuppa?', '10 of the most iconic portraits from a lost US', 'Can we really fuel planes with fat and sugar?', "Why US 'YOLO' spending baffles economists", "A designer's guide to Vienna shopping", 'Sheff Utd set to sack manager Heckingbottom', 'Players may follow Farrell by taking break - Sinckler', 'Man City charged over players confronting referee', "Barbarians' Ratuniyarawa admits sex attacks in Cardiff bar", "'I've never seen a game with this many beautiful goals'", 'Dominant 49ers power to statement win over Eagles', 'Bouchier & Gibson awarded first central contracts']
# df = processKeywords(list_test)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.expand_frame_repr', False)
# print(df)