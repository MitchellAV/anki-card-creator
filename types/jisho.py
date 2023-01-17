from typing import Union, List, Any, Optional,TypedDict

class JishoFiltered(TypedDict):
    word: str
    is_common: bool
    jlpt: List[str]
    kanji: str
    reading: str
    is_kana: bool
    pos: str
    definition: str


class Attribution(TypedDict):
    jmdict: bool
    jmnedict: bool
    dbpedia: Union[bool, str]


class Japanese(TypedDict):
    word: str
    reading: str


class Link(TypedDict):
    text: str
    url: str


class Sense(TypedDict):
    english_definitions: List[str]
    parts_of_speech: List[str]
    links: List[Link]
    tags: List[str]
    restrictions: List[Any]
    see_also: List[str]
    antonyms: List[Any]
    source: List[Any]
    info: List[Any]
    sentences: Optional[List[Any]]


class Datum(TypedDict):
    slug: str
    is_common: bool
    tags: List[str]
    jlpt: List[str]
    japanese: List[Japanese]
    senses: List[Sense]
    attribution: Attribution


class Meta(TypedDict):
    status: int


class JishoResponse(TypedDict):
    meta: Meta
    data: List[Datum]
