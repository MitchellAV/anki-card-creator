from typing import List
import requests
import pandas as pd
import sys
import csv

sys.path.append('./types')

from jisho import Japanese, JishoFiltered, JishoResponse, Sense
from tatoeba import TatoebaFiltered, TatoebaResponse

def create_jisho_url (search_term: str):
    JISHO_URL = f"https://jisho.org/api/v1/search/words?keyword={search_term}"
    return JISHO_URL


def create_tatoeba_url (search_term: str):
    # from=jpn&to=eng&
    TATOEBA_URL = f'https://tatoeba.org/en/api_v0/search?from=jpn&to=eng&sort=relevance&trans_link=direct&query=@text {search_term}'    
    return TATOEBA_URL

def format_jisho_results (search_term: str, results: JishoResponse):
    word_info = results['data'][0]

    word = word_info['slug']
    is_common = word_info['is_common']
    jlpt = word_info['jlpt']
    japanese = word_info['japanese']

    def get_correct_jp_index (search_term:str, list:List[Japanese]):
        for index, term in enumerate(list):
            kanji = ''
            try:
                kanji = term['word']
            except:
                kanji = term['reading']
            if kanji == search_term:
                return index
            else:
                pass
        return 0 

    jp_index = get_correct_jp_index(search_term, japanese)

    japanese = word_info['japanese'][jp_index]
    reading = japanese['reading']
    kanji = ''
    try:
        kanji = japanese['word']
    except:
        kanji = japanese['reading']

    english = word_info['senses']

    def get_correct_en_index (search_term: str, list: List[Sense]):
        for index, term in enumerate(list):
            info = term['info']

            for note in info:
                if f'. {search_term}' in note:
                    return index
            else:
                pass
        return 0 
    
    en_index = get_correct_en_index(search_term, english)
    english = word_info['senses'][en_index]
    tags = english['tags']
    info = '; '.join(english['info'])
    is_kana = any(el in 'Usually written using kana alone' for el in tags)
    pos = '; '.join(english['parts_of_speech'])
    definition = '; '.join(english['english_definitions'][:3])


   

    filtered_data: JishoFiltered = {
        "word": word,
        "is_common":is_common,
        "jlpt":jlpt,
        "kanji": kanji,
        "reading": reading,
        # "japanese": japanese,
        # "english": english,
        "info": info,
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
    filtered_data: JishoFiltered = {'definition':'',
    'is_common': True, 'is_kana':True,'jlpt':[],
    'kanji': '',"pos":'',"reading":'',"word":''}

    if len(data) != 0:
        filtered_data = format_jisho_results(search_term, data)
    return filtered_data

def get_tatoeba_results (search_term: str):
    url = create_tatoeba_url(search_term)
    r = requests.get(url)
    data:TatoebaResponse = r.json()
    filtered_data: TatoebaFiltered = {'sentence':'','translation':''}
    if (len(data['results']) != 0):
        filtered_data = format_tatoeba_results(data)
    return filtered_data


list_of_words: List[str] = []

with open('input.txt', encoding='utf-8') as file:
    for line in file:
        list_of_words.append(line.strip())



def create_anki_card (search_term: str):


    word_results = get_jisho_results(search_term)

    sentence_results = get_tatoeba_results(search_term)


    columns = ['Vocabulary-Kanji',	'Vocabulary-Furigana',	'Vocabulary-Kana',	'Vocabulary-English',	'Vocabulary-Audio',	'Vocabulary-Pos',	'Caution',	'Expression',	'Reading',	'Sentence-Kana',	'Sentence-English']		

# row = [word_results['kanji'], '']

    is_kana_char = '[カ] '

    jlpt = ", ".join(word_results["jlpt"])
    vocabulary_kanji = word_results["kanji"]
    vocabulary_Furigana = f'{word_results["kanji"]}[{word_results["reading"]}]'
    vocabulary_kana = word_results["reading"]
    vocabulary_english = f'{is_kana_char if word_results["is_kana"] else ""}{word_results["definition"]}'
    vocabulary_audio = ''
    vocabulary_pos =	word_results["pos"]
    caution = ''
    expression = sentence_results["sentence"]
    reading = sentence_results["sentence"]
    sentence_kana = ''
    sentence_english = sentence_results["translation"]



    print(f'JLPT: {jlpt}')
    print(f'Vocabulary-Kanji: {vocabulary_kanji}')
    print(f'Vocabulary-Furigana: {vocabulary_Furigana}')
    print(f'Vocabulary-Kana: {vocabulary_kana}')
    print(f'Vocabulary-English: {vocabulary_english}')
    print(f'Vocabulary-Pos: {vocabulary_pos}')
    print(f'Expression: {expression}')
    print(f'Reading: {reading}')
    print(f'Sentence-English: {sentence_english}')

    row = [vocabulary_kanji,vocabulary_Furigana,vocabulary_kana,vocabulary_english,vocabulary_audio,vocabulary_pos,caution,expression,reading,sentence_kana,sentence_english]

    return row

with open('output.csv', 'w', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    for word in list_of_words:
        row = create_anki_card(word)
        write.writerow(row)

