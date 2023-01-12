import requests
import pandas as pd

from jisho import JishoResponse
from tatoeba import TatoebaResponse

def create_jisho_url (search_term: str):
    JISHO_URL = f"https://jisho.org/api/v1/search/words?keyword={search_term}"
    return JISHO_URL


def create_tatoeba_url (search_term: str):
    TATOEBA_URL = f"https://tatoeba.org/en/api_v0/search?from=jpn&query={search_term}&to=eng"    
    return TATOEBA_URL

def format_jisho_results (results: JishoResponse):
    word_info = results['data'][0]

    word = word_info['slug']
    is_common = word_info['is_common']
    jlpt = word_info['jlpt']
    japanese = word_info['japanese']
    english = word_info['senses']


    filtered_data = {
        "word": word,
        "is_common":is_common,
        "jlpt":jlpt,
        "japanese": japanese,
        "english": english
    }

    return filtered_data


def format_tatoeba_results (results:TatoebaResponse):
    
    sentence_info = results['results'][0]
    sentence = sentence_info['text']
    translation_info = sentence_info['translations'][0][0]
    translation = translation_info['text']

    filtered_data = {
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
    filtered_data = format_tatoeba_results(data)
    return filtered_data



search_term = "仕事"

print(get_jisho_results(search_term))
print(get_tatoeba_results(search_term))

word_results = get_jisho_results(search_term)
sentence_results = get_tatoeba_results(search_term)


columns = ['Vocabulary-Kanji',	'Vocabulary-Furigana',	'Vocabulary-Kana',	'Vocabulary-English',	'Vocabulary-Audio',	'Vocabulary-Pos',	'Caution',	'Expression',	'Reading',	'Sentence-Kana',	'Sentence-English']		


df = pd.DataFrame(columns=columns)

print(df)
