from typing import List, Any, Optional, TypedDict
from enum import Enum
from datetime import datetime


class Sentences(TypedDict):
    finder: str
    page: int
    current: int
    count: int
    per_page: int
    start: int
    end: int
    prev_page: bool
    next_page: bool
    page_count: int
    sort: None
    direction: None
    limit: None
    sort_default: bool
    direction_default: bool
    scope: None
    complete_sort: List[Any]



class Paging(TypedDict):
    sentences: Sentences



class Dir(Enum):
    LTR = "ltr"


class ResultLang(Enum):
    JPN = "jpn"


class ResultLangName(Enum):
    JAPANESE = "Japanese"


class ResultLangTag(Enum):
    JA = "ja"


class License(Enum):
    CC_BY_20_FR = "CC BY 2.0 FR"


class Script(Enum):
    HRKT = "Hrkt"


class TypeEnum(Enum):
    ALTSCRIPT = "altscript"


class User(TypedDict):
    username: str

 


class Transcription(TypedDict):
    id: int
    sentence_id: int
    script: Script
    text: str
    user_id: Optional[int]
    needs_review: bool
    modified: datetime
    user: Optional[User]
    readonly: bool
    type: TypeEnum
    html: str
    markup: None
    info_message: str



class AttributionURL(Enum):
    EN_USER_PROFILE_CK = "/en/user/profile/CK"


class Author(Enum):
    CK = "CK"


class Audio(TypedDict):
    id: int
    author: Author
    attribution_url: AttributionURL
    license: None
    external: None
    sentence_id: Optional[int]
    user: Optional[User]




class TranslationLang(Enum):
    ENG = "eng"


class TranslationLangName(Enum):
    ENGLISH = "English"


class TranslationLangTag(Enum):
    EN = "en"


class Translation(TypedDict):
    id: int
    text: str
    lang: TranslationLang
    correctness: int
    script: None
    transcriptions: List[Any]
    audios: List[Audio]
    is_direct: Optional[bool]
    lang_name: TranslationLangName
    dir: Dir
    lang_tag: TranslationLangTag




class Result(TypedDict):
    id: int
    text: str
    lang: ResultLang
    correctness: int
    script: None
    license: License
    translations: List[List[Translation]]
    transcriptions: List[Transcription]
    audios: List[Any]
    user: User
    lang_name: ResultLangName
    dir: Dir
    lang_tag: ResultLangTag
    is_favorite: None
    is_owned_by_current_user: bool
    permissions: None
    max_visible_translations: int
    current_user_review: None



class TatoebaResponse(TypedDict):
    paging: Paging
    results: List[Result]
