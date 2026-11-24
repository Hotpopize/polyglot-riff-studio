from __future__ import annotations

from typing import Any

# =============================================================================
# SPLIT SONG LYRIC STANZAS (1 line per entry -> clean Git diffs & zero duplication)
# Derived strings (lyric_stanzas, full_lyrics) are materialized at runtime only.
# =============================================================================
SONG_SPLIT_LYRICS: dict[str, dict[str, Any]] = {
    "SONG_CZ_OVA_NOHAVICA": {
        "source_url": "https://www.letras.com/jaromir-nohavica/ostravo/",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Ostravo, Ostravo,",
                "město mezi městy,",
                "hořké moje štěstí,",
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
                "ptáci na obloze jenom jednu cestu kreslí,",
                "Ostravo, srdce rudé, zpečetěný osude.",
            ],
            [
                "Na první dobrou bez navoněné bídy, odložit smoking —",
                "kaj ľudzie fchytaju šichtu a po robotě maju čistý fajront,",
                "bo ten motor musí čistě fachat sám;",
                "řekni mi na rovinu, do čeho se pustíš s plnou parou!",
            ],
        ],
    },
    "SONG_AT_VIE_FALCO": {
        "source_url": "https://www.letras.com/falco/vienna-calling/",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Hello, Vienna calling,",
                "Hello, hello, Vienna calling,",
                "Hello, hello, Vienna calling,",
                "Hello, oho, Vienna calling.",
            ],
            [
                "Talking about Stella sitzt in Rio, Stella liegt in Tokyo,",
                "Männer fragen sie nach Feuer, nach dem andern sowieso.",
                "Sugar Chris, dich sehr vermisst — dein Bein und dein Gesicht,",
                "Du kannst auf mich verzichten, doch nur auf Luxus nicht.",
            ],
            [
                "Womit spielen kleine Mädchen heute, hier und dort und da,",
                "ob in Tucson, Arizona, Toronto, Canada.",
                "Wien, nur Wien, du kennst mich up, kennst mich down, du kennst mich!",
                "Wien, Wien, nur du allein — wohin sind deine Frauen?",
            ],
            [
                "Ohoho, operator (so alone am I),",
                "Ohoho, operator (need you to come tonight).",
                "Hello, oho, Vienna calling,",
                "Hello, oho, Vienna calling.",
            ],
            [
                "Two, one, zero — der Alarm ist rot,",
                "Wien in Not — cha, cha, cha,",
                "Vienna calling, Vienna calling!",
            ],
            [
                "Und plötzlich heißt Maria Marilyn und Eva heißt Yvonne,",
                "ein junger Bogart hängt ihr an den Lippen, Kleines, und sagt komm.",
                "Die Lockenpracht wird abgemacht, die Tänzer sind gestoppt,",
                "es ist 4 Uhr 45, nun wird Position geprobt.",
            ],
            [
                "Womit spielen kleine Mädchen heute, hier und dort und da,",
                "ob in Tucson, Arizona, Toronto, Canada.",
                "Wien, nur Wien, du kennst mich up, kennst mich down, du kennst mich!",
                "Wien, Wien, nur du allein — wohin sind deine Frauen?",
            ],
            [
                "Ohoho, operator (so alone am I),",
                "Ohoho, operator (need you to come tonight).",
                "Hello, oho, Vienna calling (na na na na),",
                "Hello, oho, Vienna calling.",
            ],
            [
                "Two, one, zero — der Alarm ist rot, Wien in Not — cha, cha, cha,",
                "Hello, Vienna calling (hello!), Wien in Not!",
                "Vienna calling, Vienna calling!",
            ],
            [
                "Vienna Calling, Oida! Das ist schwer in Ordnung —",
                "kein Theater, keine Pflanzerei und kein G’schichtldrucken, der Wiener Schmäh rennt eh halt von allein;",
                "musst nur die Vorsicht an der Garderobe abgeben,",
                "Hand aufs Herz: was ist der schönste Bledsinn, den wir als Nächstes anreißen?",
            ],
        ],
    },
    "SONG_RU_ALA_ASTUDIO": {
        "source_url": "https://www.musixmatch.com/lyrics/A-Studio/%D0%94%D0%B6%D1%83%D0%BB%D0%B8%D1%8F",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Девчонка из далёких дней,",
                "по школе бегал я за ней,",
                "домой провожал, записки тайком писал.",
            ],
            [
                "Мы незаметно подросли,",
                "и эти дни давно ушли,",
                "и я не скрывал, что лишь о тебе мечтал.",
            ],
            [
                "Но только всё пошло ко дну,",
                "и я не знаю почему —",
                "уехала ты в далёкую страну.",
            ],
            [
                "Тебя полюбят там опять,",
                "но будут по-другому звать,",
                "к чему вспоминать мне новое имя твоё?",
            ],
            [
                "Джули, Джулия!",
                "Джули, Джулия!",
                "Джули, Джулия!",
                "Джули! О-о-о!",
            ],
            [
                "Не знаю я твой телефон, но разве мне поможет он —",
                "не стану звонить, нам снова вдвоём не быть.",
                "Не знаю новый адрес твой, но нас не сблизит он с тобой —",
                "не стану писать, хоть много хочу сказать.",
            ],
            [
                "Развеялся былой обман, нас разделяет океан —",
                "прощай и забудь, назад не пройти тот путь.",
                "Зачем напоминает грусть мне имя твоё? Ну и пусть —",
                "я буду опять его про себя повторять. О-о-о-о-о-о!",
            ],
            [
                "Джули, Джулия!",
                "Джули, Джулия!",
                "Джули, Джулия!",
                "Джули! О-о-о!",
            ],
            [
                "Девочка моя Джулия, родной, под звёздами Алматы мы всё сделали по красоте,",
                "базару нет и без лишних понтов — разговор по душам за широким дастарханом;",
                "хватит держать горный беркут в золотой клетке —",
                "давай прямо сейчас рвануть наверх на Медеу без тормозов!",
            ],
        ],
    },
    "SONG_EN_YYC_LOVERBOY": {
        "source_url": "https://www.letras.com/loverboy/working-for-the-weekend/",
        "reach_channel": "agent-reach+jina",
        "stanzas": [
            [
                "Everyone's watching, to see what you will do,",
                "everyone's looking at you, oh!",
                "Everyone's wondering, will you come out tonight,",
                "everyone's trying to get it right, get it right!",
            ],
            [
                "Everybody's working for the weekend,",
                "everybody wants a little romance,",
                "everybody's goin' off the deep end,",
                "everybody needs a second chance, oh!",
            ],
            [
                "You want a piece of my heart,",
                "you better start from the start,",
                "you wanna be in the show —",
                "come on baby, let's go!",
            ],
            [
                "Everyone's looking to see if it was you,",
                "everyone wants you to come through,",
                "everyone's hoping it'll all work out,",
                "everyone's waiting, they're holding out!",
            ],
            [
                "Everybody's working for the weekend,",
                "everybody wants a little romance,",
                "everybody's goin' off the deep end,",
                "everybody needs a second chance, oh!",
            ],
            [
                "You want a piece of my heart, you better start from the start,",
                "you wanna be in the show — come on baby, let's go!",
                "You want a piece of my heart, you better start from the start,",
                "you wanna be in the show — come on baby, let's go!",
            ],
            [
                "Hold on a second, bud — everybody's working for the weekend, and this is the real deal:",
                "stop being all hat and no cattle, zero corporate polish, crank the amp to eleven;",
                "don't leave that 69 Mustang collecting dust in the garage all summer —",
                "kick the garage doors open tonight and just give ’er!",
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
                "Enamorao de la vida, aunque a veces duela,",
                "si tengo frío busco candela.",
                "Volá, volando voy!",
            ],
            [
                "Señoras y señores, sepan ustedes",
                "que es la flor de la noche pa' quien la merece.",
                "Volá, volando voy!",
            ],
            [
                "Enamorao de la vida, aunque a veces duela,",
                "yo no sé quien soy, ni lo pretendiera.",
                "Volá, volando voy!",
            ],
            [
                "Porque a mí me va mucho la marcha tropical,",
                "y los cariños en la frontera me van.",
            ],
            [
                "Volando voy, volando vengo,",
                "por el camino yo me entretengo,",
                "volá, volando voy!",
            ],
            [
                "Oye, tío, volando voy por Sotogrande porque esto tiene duende,",
                "sin postureo, con las cartas sobre la mesa y hay que tener buena muñeca;",
                "nunca vamos a mirar los toros desde la barrera —",
                "mójate un poco conmigo: ¿cuál es la jugada que te pide el cuerpo?",
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
