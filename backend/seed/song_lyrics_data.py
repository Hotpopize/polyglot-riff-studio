from __future__ import annotations

from typing import Any

# =============================================================================
# SPLIT SONG LYRIC STANZAS (1 line per entry -> clean Git diffs & zero duplication)
# Derived strings (lyric_stanzas, full_lyrics) are materialized at runtime only.
# =============================================================================
SONG_SPLIT_LYRICS: dict[str, dict[str, Any]] = {
    "SONG_CZ_OVA_NOHAVICA": {
        "source_url": "https://www.karaoketexty.cz/texty-pisni/nohavica-jaromir/ostravo-19675",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Ostravo, Ostravo,",
                "město mezi městy, hořké moje štěstí,",
                "Ostravo, Ostravo,",
                "černá hvězdo nad hlavou.",
            ],
            [
                "Pánbůh rozdal jiným městům všecku krásu,",
                "parníky na řekách a dámy všité do atlasu,",
                "Ostravo, srdce rudé, zpečetěný osude.",
            ],
            [
                "Ostravo, Ostravo,",
                "kde jsem oči nechal, když jsem k tobě spěchal,",
                "Ostravo, Ostravo,",
                "černá hvězdo nad hlavou.",
            ],
            [
                "Ať mě moje nohy nesly, kam mě nesly,",
                "ptáci na obloze jenom jednu cestu kreslí —",
                "kaj ľudzie fchytaju šichtu a po robotě maju čistý fajront,",
                "bo ten motor musí fachat sám!",
            ],
        ],
    },
    "SONG_AT_VIE_FALCO": {
        "source_url": "https://falco.at/discography/vienna-calling/",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Hello, Vienna calling! Hello, oho, Vienna calling!",
                "Stella sitzt in Rio, Stella liegt in Tokyo,",
                "Männer fragen sie nach Feuer, nach dem andern sowieso.",
            ],
            [
                "Womit spielen kleine Mädchen heute, hier und dort und da,",
                "ob in Tucson, Arizona, Toronto, Canada.",
            ],
            [
                "Wien, nur Wien, du kennst mich up, kennst mich down, du kennst mich!",
                "Two, one, zero — der Alarm ist rot,",
                "Wien in Not, Vienna calling!",
            ],
            [
                "Vienna Calling, Oida! Kein Stress und kein G’schichtldrucken —",
                "der Wiener Schmäh rennt eh von allein,",
                "musst nur die Vorsicht an der Garderobe abgeben, schwer in Ordnung!",
            ],
        ],
    },
    "SONG_RU_ALA_ASTUDIO": {
        "source_url": "https://lyricsworld.ru/A-Studio/Dzhuliya-26451.html",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Девчонка из далёких дней,",
                "по школе бегал я за ней,",
                "домой провожал, записки тайком писал.",
            ],
            [
                "Мы незаметно подросли, и эти дни давно ушли,",
                "и я не скрывал, что лишь о тебе мечтал:",
                "Джули-Джулия, Джули-Джулия!",
            ],
            [
                "Не знаю я твой телефон, но разве мне поможет он —",
                "зачем напоминает грусть мне имя твоё,",
                "я буду опять его про себя повторять: Джули-Джулия!",
            ],
            [
                "Девочка моя Джулия, под тёплыми звёздами Алматы",
                "мы всё сделали по красоте, родной, базару нет —",
                "разговор по душам за широким дастарханом, прежде чем рвануть на Медеу!",
            ],
        ],
    },
    "SONG_EN_YYC_LOVERBOY": {
        "source_url": "https://www.stlyrics.com/lyrics/footloose/workingfortheweekend.htm",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Everyone's watching, to see what you will do,",
                "everyone's looking at you, oh!",
                "Everyone's wondering, will you come out tonight,",
                "everyone's trying to get it right!",
            ],
            [
                "Everybody's working for the weekend, everybody wants a new romance,",
                "everybody's goin' off the deep end, everybody needs a second chance!",
            ],
            [
                "You want a piece of my heart, you better start from the start,",
                "you wanna be in the show — come on baby, let's go!",
            ],
            [
                "Everybody's working for the weekend, bud!",
                "Stop being all hat and no cattle, don't leave that 69 Mustang collecting dust —",
                "kick the garage door open and just give ’er!",
            ],
        ],
    },
    "SONG_ES_SOT_CAMARON": {
        "source_url": "https://www.letras.com/camaron-de-la-isla/volando-voy/",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Volando voy, volando vengo,",
                "volando voy, volando vengo,",
                "por el camino yo me entretengo,",
                "por el camino yo me entretengo.",
            ],
            [
                "Enamorao de la vida, que a veces duele,",
                "si tengo frío busco candela.",
                "Señoras y señores, sepan ustedes",
                "que es la flor de la noche pa' quien la merece.",
            ],
            [
                "Y volando voy, volando vengo, por el camino yo me entretengo,",
                "porque a mí me va mucho la marcha tropical",
                "y los cariños en la frontera me dan.",
            ],
            [
                "Volando voy por Sotogrande sin postureo, tío:",
                "enamorao de la vida porque esto tiene duende",
                "y con las cartas sobre la mesa nunca vamos a mirar los toros desde la barrera.",
            ],
        ],
    },
    "SONG_WEEKND_OOTG": {
        "source_url": "https://www.letras.com/the-weeknd/one-of-the-girls-feat-jennie-lily-rose-depp/",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Lock me up and throw away the key",
                "He knows how to get the best out of me",
                "I'm no force for the world to see",
                "Trade my whole life just to be",
            ],
            [
                "Tell nobody I control you",
                "I broke you just to own you",
                "They can't tell that I love you",
                "'Cause you're loyal, baby",
                "I love when you're submissive",
                "You love it when I break skin",
                "You feel pain without flinchin'",
                "So say it",
            ],
            [
                "Give me tough love",
                "Leave me with nothin' when I come down",
                "My kind of love",
                "Push me and choke me till I pass out",
            ],
            [
                "We don't gotta be in love, no",
                "I don't gotta be the one, no",
                "I just wanna be one of your girls tonight",
                "We don't gotta be in love, no",
                "I don't gotta be the one, no",
                "I just wanna be one of your girls tonight, oh-oh-oh",
            ],
            [
                "Push me down, hold me down",
                "Spit in my mouth while you turn me out",
                "I wanna take your light inside",
                "Tear me down, snuff me out",
                "Hands on my neck while you push it up",
                "And I'm screamin' out",
            ],
            [
                "Give me tough love",
                "Leave me with nothin' when I come down",
                "My kind of love",
                "Force me and leave me with no breath",
            ],
            [
                "We don't gotta be in love, no",
                "I don't gotta be the one, no",
                "I just wanna be one of your girls tonight (tonight)",
                "We don't gotta be in love, no",
                "I don't gotta be the one, no (oh)",
                "I just wanna be one of your girls tonight, oh-oh-oh",
            ],
            [
                "Lock me up and throw away the key",
                "He knows how to get the best out of me",
                "I'm no force for the world to see",
                "Trade my whole life just to be",
                "Top of the world, but I'm still not free",
                "This is a secret that I keep",
                "Until it's gone, I can never find peace",
                "Waste my whole life just to be",
            ],
            [
                "We don't gotta be in love, no",
                "I don't gotta be the one, no",
                "I just wanna be one of your girls tonight (tonight)",
                "We don't gotta be in love, no",
                "I don't gotta be the one, no (oh)",
                "I just wanna be one of your girls tonight (oh), oh-oh-oh",
            ],
        ],
    },
}


def attach_split_lyrics(songs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Derive per-line, per-stanza, and full_lyrics strings in memory from split SONG_SPLIT_LYRICS."""
    for s in songs:
        meta = SONG_SPLIT_LYRICS.get(s["uid"])
        if not meta:
            continue
        stanzas_lines: list[list[str]] = meta["stanzas"]
        lyric_stanzas = ["\n".join(lines) for lines in stanzas_lines]
        lyric_lines = [
            {
                "stanza": idx + 1,
                "line": l_idx + 1,
                "text": line_text,
                "is_chorus": idx == len(stanzas_lines) - 1,
            }
            for idx, lines in enumerate(stanzas_lines)
            for l_idx, line_text in enumerate(lines)
        ]
        s["source_url"] = meta["source_url"]
        s["reach_channel"] = meta["reach_channel"]
        s["stanzas_lines"] = stanzas_lines
        s["lyric_lines"] = lyric_lines
        s["lyric_stanzas"] = lyric_stanzas
        s["full_lyrics"] = "\n\n".join(lyric_stanzas)
    return songs
