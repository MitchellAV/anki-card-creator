import requests
import pandas as pd
import sys
import csv

sys.path.append('./types')

from jisho import JishoFiltered, JishoResponse
from tatoeba import TatoebaFiltered, TatoebaResponse

def create_jisho_url (search_term: str):
    JISHO_URL = f"https://jisho.org/api/v1/search/words?keyword={search_term}"
    return JISHO_URL


def create_tatoeba_url (search_term: str):
    # from=jpn&to=eng&
    TATOEBA_URL = f"https://tatoeba.org/en/api_v0/search?from=jpn&to=eng&query={search_term}"    
    return TATOEBA_URL

def format_jisho_results (results: JishoResponse):
    word_info = results['data'][0]

    word = word_info['slug']
    is_common = word_info['is_common']
    jlpt = word_info['jlpt']
    japanese = word_info['japanese'][0]
    english = word_info['senses'][0]
    tags = english['tags']
    is_kana = any(el in 'Usually written using kana alone' for el in tags)
    pos = '; '.join(english['parts_of_speech'])
    definition = '; '.join(english['english_definitions'][:3])
    reading = japanese['reading']
    kanji = japanese['word']


   

    filtered_data: JishoFiltered = {
        "word": word,
        "is_common":is_common,
        "jlpt":jlpt,
        "kanji": kanji,
        "reading": reading,
        # "japanese": japanese,
        # "english": english,
        "is_kana": is_kana,
        "pos": pos,
        "definition": definition
    }

    return filtered_data


def format_tatoeba_results (results:TatoebaResponse):
    
    sentence_info = results['results'][0]
    sentence = sentence_info['text']
    translation = ''
    try:
        translation_info = sentence_info['translations'][0][0]
        translation = translation_info['text']

    except:
        print('No english translation exists on tatoeba')
    

    filtered_data: TatoebaFiltered = {
        "sentence": sentence,
        "translation": translation
    }

    return filtered_data

def get_jisho_results (search_term: str):
    url = create_jisho_url(search_term)
    r = requests.get(url)
    data:JishoResponse = r.json()
    filtered_data = format_jisho_results(data)
    return filtered_data

def get_tatoeba_results (search_term: str):
    url = create_tatoeba_url(search_term)
    r = requests.get(url)
    data:TatoebaResponse = r.json()
    filtered_data: TatoebaFiltered = {'sentence':'','translation':''}
    if (len(data['results']) != 0):
        filtered_data = format_tatoeba_results(data)
    return filtered_data



search_term = "割増"

# print(get_jisho_results(search_term))
# print(get_tatoeba_results(search_term))

word_results = get_jisho_results(search_term)

sentence_results = get_tatoeba_results(word_results['kanji'])


columns = ['Vocabulary-Kanji',	'Vocabulary-Furigana',	'Vocabulary-Kana',	'Vocabulary-English',	'Vocabulary-Audio',	'Vocabulary-Pos',	'Caution',	'Expression',	'Reading',	'Sentence-Kana',	'Sentence-English']		

# row = [word_results['kanji'], '']

is_kana_char = '[カ] '
JLPT = ", ".join(word_results["jlpt"])
Vocabulary_Kanji = word_results["kanji"]
Vocabulary_Furigana= f'{word_results["kanji"]}[{word_results["reading"]}]'
Vocabulary_Kana=word_results["reading"]
Vocabulary_English=f'{is_kana_char if word_results["is_kana"] else ""}{word_results["definition"]}'
Vocabulary_Audio=	''
Vocabulary_Pos=	word_results["pos"]
Caution=''
Expression=sentence_results["sentence"]
Reading=	sentence_results["sentence"]
Sentence_Kana=''
Sentence_English=sentence_results["translation"]



# df = pd.DataFrame(columns=columns)
print(f'JLPT: {JLPT}')
print(f'Vocabulary-Kanji: {Vocabulary_Kanji}')
print(f'Vocabulary-Furigana: {Vocabulary_Furigana}')
print(f'Vocabulary-Kana: {Vocabulary_Kana}')
print(f'Vocabulary-English: {Vocabulary_English}')
print(f'Vocabulary-Pos: {Vocabulary_Pos}')
print(f'Expression: {Expression}')
print(f'Reading: {Reading}')
print(f'Sentence-English: {Sentence_English}')

row = [Vocabulary_Kanji,Vocabulary_Furigana,Vocabulary_Kana,Vocabulary_English,Vocabulary_Audio,Vocabulary_Pos,Caution,Expression,Reading,Sentence_Kana,Sentence_English]
with open('word.csv', 'w',encoding='utf-8') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(row)

