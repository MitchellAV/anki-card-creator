from typing import List
import requests
import sys
import csv
from wanakana import strip_okurigana, to_hiragana
from furigana import add_furigana

sys.path.append('./types')

from jisho import Japanese, JishoFiltered, JishoResponse, Sense
from tatoeba import TatoebaFiltered, TatoebaResponse

def create_jisho_url (search_term: str):
    JISHO_URL = f"https://jisho.org/api/v1/search/words?keyword={search_term}"
    return JISHO_URL


def create_tatoeba_url (search_term: str, kana: str, is_kana: bool):
    # from=jpn&to=eng&
    # stripped_word = strip_okurigana(search_term)
    text_query = f'="{search_term}"'
    # if is_kana:
    #     text_query = f'="{kana}"'
    # else:
    #     text_query = f'="{search_term}"'
    # print(search_term, kana)
    TATOEBA_URL = f'https://tatoeba.org/en/api_v0/search?from=jpn&to=eng&trans_link=direct&sort=relevance&query=@text {text_query} @transcription {kana}'    
    return TATOEBA_URL

def format_jisho_results (search_term: str, results: JishoResponse):

    word_index = 0
    for index, slug in enumerate(results['data']):
        if slug['slug'] == search_term:
            word_index = index
            break
    
    word_info = results['data'][word_index]
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

    if len(data) != 0 and len(data['data']) != 0:
        filtered_data = format_jisho_results(search_term, data)
    return filtered_data

def get_tatoeba_results (search_term: str, kana: str, is_kana: bool):
    url = create_tatoeba_url(search_term, kana, is_kana)
    r = requests.get(url)
    data:TatoebaResponse = r.json()
    filtered_data: TatoebaFiltered = {'sentence':'','translation':''}
    if (len(data['results']) != 0):
        filtered_data = format_tatoeba_results(data)
    return filtered_data





def create_anki_card (search_term: str):


    word_results = get_jisho_results(search_term)

    not_allowed_pos = ['ichidan', 'godan']
    kana = word_results['reading']
    is_kana = word_results['is_kana']
    if any(ele in (word_results['pos']).lower() for ele in not_allowed_pos):
        search_term = word_results['kanji'][:-1]
        kana = kana[:-1]
    sentence_results = get_tatoeba_results(search_term, kana, is_kana)



# row = [word_results['kanji'], '']

    is_kana_char = '[カ] '

    jlpt = ", ".join(word_results["jlpt"])
    vocabulary_kanji = word_results["kanji"]
    vocabulary_Furigana = f'{add_furigana(word_results["kanji"])}'
    vocabulary_kana = word_results["reading"]
    vocabulary_english = f'{is_kana_char if word_results["is_kana"] else ""}{word_results["definition"]}'
    vocabulary_audio = ''
    vocabulary_pos = word_results["pos"]
    caution = f'{word_results["info"]}'
    expression = sentence_results["sentence"]
    reading = add_furigana(sentence_results["sentence"])
    sentence_kana = ''
    sentence_english = sentence_results["translation"]



    print(f'JLPT: {jlpt}')
    print(f'Vocabulary-Kanji: {vocabulary_kanji}')
    print(f'Vocabulary-Furigana: {vocabulary_Furigana}')
    print(f'Vocabulary-Kana: {vocabulary_kana}')
    print(f'Vocabulary-English: {vocabulary_english}')
    print(f'Vocabulary-Pos: {vocabulary_pos}')
    print(f'Caution: {caution}')
    print(f'Expression: {expression}')
    print(f'Reading: {reading}')
    print(f'Sentence-English: {sentence_english}')

    row = [vocabulary_kanji,vocabulary_Furigana,vocabulary_kana,vocabulary_english,vocabulary_audio,vocabulary_pos,caution,expression,reading,sentence_kana,sentence_english]

    return row


list_of_words: List[str] = []
columns = ['Vocabulary-Kanji',	'Vocabulary-Furigana',	'Vocabulary-Kana',	'Vocabulary-English',	'Vocabulary-Audio',	'Vocabulary-Pos',	'Caution',	'Expression',	'Reading',	'Sentence-Kana',	'Sentence-English']		

with open('./input/input.txt', encoding='utf-8') as file:
    for line in file:
        list_of_words.append(line.strip())

# remove duplicates from input
list_of_words = [i for n, i in enumerate(list_of_words) if i not in list_of_words[:n]]


with open('./output/output.csv', 'w', encoding='utf-8', newline='') as f:
    write = csv.writer(f)
    write.writerow(columns)
    for word in list_of_words:
        row = create_anki_card(word)
        if row[0] == '':
            pass
        write.writerow(row)

