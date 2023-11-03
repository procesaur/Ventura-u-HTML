from re import findall, sub
from json import dump
from unicodedata import normalize


with open("single.txt", "r", encoding="utf-8") as sf:
    single = sf.read()


def add_diactritic(string, diactritic):
    new = ""
    for x in string:
        new += x
        if x in "abcdefghijklmnopqrstuvwxyz":
            new += diactritic
    return new


def to_latin(str):
    for key, value in cyr2lat.items():
        str = str.replace(key, value)
    return str


tag_subs = {
    r'<(F[0-9]{1,3})(W[19])?(%[0-9]+)?(M\^)?(MV)?>': r'<\1><\4\5>',
    r'<(F[0-9]{1,3})(W[19])?(%[0-9]+)?([A-Z]+)?(%[0-9]+)?>': r'<\1><\4\5>',
    r'<(F[0-9]{4,8})(W[19])?(%[0-9]+)?([A-Z]+)?(\^)?(%[0-9]+)?>': r'<\4\5><\1>',
    r'<([A-Z]+)(%[0-9]+)?(J[0-9]{1,3})?>': r'<\1>',
    r'<(F[0-9]+)?(J[0-9]{1,3})?>': r'<\1>',
    r'<(W1)([A-Z])>': r'<\2>',
    r'<(W1)(%?-?[0-9]+)?>': '',
    r'<(%-?[0-9]+)>': '',
    # r'<F14><BI>([0-9a-z])': r'<v>\1</d>',
    r'<M\^>([0-9])': r'<sup>\1</sup>',
    r'<MV>([0-9])': r'<sub>\1</sub>',
    r'\n.+<R>\n': '',
    r'-?(<->)': '-',
    r'<[DLM]>': '<d>',
    r'<M?I>': '<i>',
    r'<M?B>': '<b>',
    r'<M?S>': '<s>',
    r'<BI>': '<v>',
    r'<F225>': r'<F14>',
}

format_paragraphs = {
    "@S-TEXT = ": "",
    "@N-TEXT = ": "",
    "@STIH = ": "",
    r'@VRH = \n\n@SLO = (.)': r'</div><div><h1>\1</h1>',
    r'\n([^\n])': r'\1',
    r'\n': r'</p>\n<p>',
    '  ': ' ',
    '</h1></p>': '</h1>',
    '<p></p>\n': ''
}

char_subs = {
    "<W1C0>^<DC255>": "◌̂",
    "<W1C0>,,<DC255>": "◌̏",
    "<W1C0>..<DC255>": "◌̈",
    "<W1C0>^^<DC255>": "◌̑",

    "<>": "",
    "|": "ђ",
    "`": "ж",
    "q": "љ",
    "w": "њ",
    "}": "ћ",
    "~": "ч",
    "x": "џ",
    "{": "ш",
    "\\": "Ђ",
    "@@": "Ж",
    "@": "Ж",
    "Q": "Љ",
    "W": "Њ",
    "]": "Ћ",
    "^": "Ч",
    "X": "Џ",
    "[": "Ш",

    "<171>": "~",
    "<198>": "|",
    "<147>": "ş",
    "<193>": "…",
    "<172>": "ı",
    "<192>": "„",
    "<181>": "“",
    "<129>": "ü",
    "<132>": "ä",
    "<148>": "ö",
    "<131>": "ь",
    "<188>": "Ⅹ",
    "<212>": "°",
    "<138>": "й",
    "<133>": "я",
    "<145>": "щ",
    "<196>": "—",
    "<128>": "Ⅰ",
    "<160>": "ы",
    "<135>": "Ⅴ",
    "<168>": "ß",
    "<142>": "Ä",
    "<139>": "ѣ",
    "<176>": "ъ",
    "<149>": "ĭ",
    "<153>": "Ö",
    "<137>": "ё",
    "<186>": "§",
    "<202>": "ѧ",
    "<144>": "ѫ",
}

Lat2Gr = {
    "<F128><130><F255>": "´",
    '<F128>A<F255>': 'Α',
    '<F128>a<F255>': 'α',
    '<F128>B<F255>': 'Β',
    '<F128>b<F255>': 'β',
    '<F128>G<F255>': 'Γ',
    '<F128>g<F255>': 'γ',
    '<F128>D<F255>': 'Δ',
    '<F128>d<F255>': 'δ',
    '<F128>E<F255>': 'Ε',
    '<F128>e<F255>': 'ε',
    '<F128>Z<F255>': 'Ζ',
    '<F128>z<F255>': 'ζ',
    '<F128>H<F255>': 'Η',
    '<F128>h<F255>': 'η',
    '<F128>U<F255>': 'Θ',
    '<F128>u<F255>': 'θ',
    '<F128>I<F255>': 'Ι',
    '<F128>i<F255>': 'ι',
    '<F128>K<F255>': 'Κ',
    '<F128>k<F255>': 'κ',
    '<F128>L<F255>': 'Λ',
    '<F128>l<F255>': 'λ',
    '<F128>M<F255>': 'Μ',
    '<F128>m<F255>': 'μ',
    '<F128>N<F255>': 'Ν',
    '<F128>n<F255>': 'ν',
    '<F128>J<F255>': 'Ξ',
    '<F128>j<F255>': 'ξ',
    '<F128>O<F255>': 'Ο',
    '<F128>o<F255>': 'ο',
    '<F128>P<F255>': 'Π',
    '<F128>p<F255>': 'π',
    '<F128>R<F255>': 'Ρ',
    '<F128>r<F255>': 'ρ',
    '<F128>S<F255>': 'Σ',
    '<F128>s<F255>': 'σ',
    '<F128>T<F255>': 'Τ',
    '<F128>t<F255>': 'τ',
    '<F128>Y<F255>': 'Υ',
    '<F128>y<F255>': 'υ',
    '<F128>F<F255>': 'Φ',
    '<F128>f<F255>': 'φ',
    '<F128>X<F255>': 'Χ',
    '<F128>x<F255>': 'χ',
    '<F128>C<F255>': 'Ψ',
    '<F128>c<F255>': 'ψ',
    '<F128>v<F255>': 'ω',
    '<F128>V<F255>': 'Ω',
}

cyr2lat = {
    "А": "A",
    "Б": "B",
    "В": "V",
    "Г": "G",
    "Д": "D",
    "Е": "E",
    "З": "Z",
    "И": "I",
    "Ј": "J",
    "К": "K",
    "Л": "L",
    "М": "M",
    "Н": "N",
    "О": "O",
    "П": "P",
    "Р": "R",
    "С": "S",
    "Т": "T",
    "У": "U",
    "Ф": "F",
    "Х": "H",
    "Ц": "C",
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "з": "z",
    "и": "i",
    "ј": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "c",
    "љ": "q",
    "њ": "w",
    "џ": "x",
    "Љ": "Q",
    "Њ": "W",
    "Џ": "X",
}

accent_subs = {
    r'<F31492>([^<]+)': u'\u0300',  # ̀
    r'<F40216>([^<]+)': u'\u0304',  # ̄
    r'<F47384>([^<]+)': u'\u0301',  # ́
    r'<F54573>([^<]+)': u'\u030f',  # ̏
    r'<F52989>([^<]+)': u'\u0311',  # ̑
    r'<F39997>([^<]+)': u'\u0301',  # ́
    r'<F53499>([^<]+)': u'\u0300',  # ̀
    r'<F52353>([^<]+)': u'\u0304',  # ̄
    r'<F56638>([^<]+)': u'\u0302',  # ̂
    r'<F40698>([^<]+)': u'\u0306',  # ̆
    r'<F57718>([^<]+)': u'\u030f',  # ̏
    r'<F33096>([^<]+)': u'\u0306',  # ̆
}

char_subs2 = {
    'A': 'А',
    'B': 'Б',
    'V': 'В',
    'G': 'Г',
    'D': 'Д',
    'E': 'Е',
    'Z': 'З',
    'I': 'И',
    'J': 'Ј',
    'K': 'К',
    'L': 'Л',
    'M': 'М',
    'N': 'Н',
    'O': 'О',
    'P': 'П',
    'R': 'Р',
    'S': 'С',
    'T': 'Т',
    'U': 'У',
    'F': 'Ф',
    'H': 'Х',
    'C': 'Ц',
    'a': 'а',
    'b': 'б',
    'v': 'в',
    'g': 'г',
    'd': 'д',
    'e': 'е',
    'z': 'з',
    'i': 'и',
    'j': 'ј',
    'k': 'к',
    'l': 'л',
    'm': 'м',
    'n': 'н',
    'o': 'о',
    'p': 'п',
    'r': 'р',
    's': 'с',
    't': 'т',
    'u': 'у',
    'f': 'ф',
    'h': 'х',
    'c': 'ц',
}

tag_subs2 = {
    r'(</?)п(>)': r'\1p\2',
    r'(</?)див(>)': r'\1div\2',
    r'(</?)б(>)': r'\1b\2',
    r'(</?)в(>)': r'\1v\2',
    r'(</?)с(>)': r'\1s\2',
    r'(</?)и(>)': r'\1i\2',
    r'(</?)х1(>)': r'\1h1\2',
    r'(</?)д(>)': r'\1d\2',
    r'(</?)суп(>)': r'\1sup\2',
    r'(</?)суб(>)': r'\1sub\2',
    '<Ф40172>': '<F40172>',
    '<Ф14>': '<F14>',
}

latin_sub = {
    r'<F40172>([^<]+)<F14>': '',
    r'<F40172>([^<]+)<d>': '',
}

close_tags = {
    '</p>': '<d></p>',
    r'<([bisv])>([^<]*)(<su[pb]>[^<]+</su[pb]>)*([^<]*)<([bisvd])>': r'<\1>\2\3\4</\1><\5>',
    r'<([bsiv])>([^<]*)(<su[pb]>[^<]+</su[pb]>)*([^<]*)<([bisvd])>': r'<\1>\2\3\4</\1><\5>',
    '<d>': '',
    r'<(/?)s>': r'<\1small>',
    '<v>': '<b><i>',
    '</v>': '</i></b>'
}

for key, value in tag_subs.items():
    single = sub(key, value, single)

for key, value in format_paragraphs.items():
    single = sub(key, value, single)

for key, value in char_subs.items():
    single = single.replace(key, value)

for key, value in Lat2Gr.items():
    single = sub(key, value, single)

for key, value in accent_subs.items():
    single = sub(key, lambda m: add_diactritic(m.group(1), value), single)

single = single.replace("<F255>", "")

for key, value in char_subs2.items():
    single = single.replace(key, value)

for key, value in tag_subs2.items():
    single = sub(key, value, single)

for key, value in latin_sub.items():
    single = sub(key, lambda m: to_latin(m.group(1)), single)

single = single.replace("<F40172>", "")
single = single.replace("<F14>", "")
single = single.replace("</div>", "", 1)
single = "<html><body>" + normalize('NFC', single) + "</p></div></body></html>"

for key, value in close_tags.items():
    single = sub(key, value, single)

tags = findall(r'<[^>]+>', single)

unique = set(tags)

tags = {i: tags.count(i) for i in unique}
tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)

tags2tags = {x[0]: x[0] for x in tags}

with open("tags2tags.json", "w", encoding="utf-8") as jf:
    dump(tags2tags, jf, indent=4)

with open("processed.html", "w", encoding="utf-8") as tf:
    tf.write(single)
