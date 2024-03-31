# Authors: Liam Arguedas <iliamftw2013@gmail.com>
# License: BSD 3 clause


def sense_es_la1() -> list[str]:
    return [
        "á",
        "Á",
        "é",
        "É",
        "í",
        "Í",
        "ó",
        "Ó",
        "ú",
        "Ú",
        "ñ",
        "Ñ",
    ]


def sense_pt_br() -> list[str]:
    return [
        "á",
        "Á",
        "é",
        "É",
        "í",
        "Í",
        "ó",
        "Ó",
        "ú",
        "Ú",
        "â",
        "Â",
        "ê",
        "Ê",
        "î",
        "Î",
        "ô",
        "Ô",
        "û",
        "Û",
        "ã",
        "Ã",
        "õ",
        "Õ",
        "ç",
        "Ç",
    ]


def sense_lan() -> tuple:
    return "^", "~"


def hotkey_lan() -> tuple:
    return "!", "+", "#"
