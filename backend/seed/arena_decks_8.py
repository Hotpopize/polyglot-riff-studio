"""Unified 8 Social Arenas metadata, full 5-persona 4-C card decks, and sequential FSRS edges."""
from __future__ import annotations

ARENAS = [
    {
        "id": "terrace",
        "icon": "🥃",
        "label": "Late-Night Terrace & Deep Chemistry",
        "short_label": "Late-Night Terrace",
        "arena_group": "Zero-Corporate Lounge",
        "description": "Warm chest-voice intimacy, unscripted candor & rooftop/terrace rapport."
    },
    {
        "id": "spark",
        "icon": "⚡",
        "label": "First-Impression Spark",
        "short_label": "First-Impression Spark",
        "arena_group": "Zero-Corporate Lounge",
        "description": "Instant magnetic opener—cutting through polite small talk in the first 20 seconds."
    },
    {
        "id": "adventure",
        "icon": "🔥",
        "label": "Melting Hesitation into Adventure",
        "short_label": "Melting Hesitation",
        "arena_group": "Zero-Corporate Lounge",
        "description": "Playfully flipping \"maybe later / playing it safe\" into spontaneous co-conspiracy."
    },
    {
        "id": "runway",
        "icon": "🧥",
        "label": "Fashion Runway & Zákulisí",
        "short_label": "Runway & Zákulisí",
        "arena_group": "Haute Salon Trio",
        "description": "Front-row couture polish vs. honest backstage tailoring where seams actually hold."
    },
    {
        "id": "hochkultur",
        "icon": "🏛️",
        "label": "Staatsoper & Hochkultur",
        "short_label": "Staatsoper & Hochkultur",
        "arena_group": "Haute Salon Trio",
        "description": "Loge & vernissage poise—dropping stiff tuxedo formality into peer-to-peer candor."
    },
    {
        "id": "polo",
        "icon": "🐎",
        "label": "Sotogrande & Polo Club Paddock",
        "short_label": "Polo Club Paddock",
        "arena_group": "Haute Salon Trio",
        "description": "High-handicap paddock calm—bridging equestrian finesse with raw engine horsepower."
    },
    {
        "id": "wien",
        "icon": "🕵️",
        "label": "Station Wien Café (Corner Intercept)",
        "short_label": "Station Wien Café",
        "arena_group": "Station Wien",
        "description": "Velvet Central-European Kaffeehaus tradecraft, quiet sovereignty & corner-table trust."
    },
    {
        "id": "b2b",
        "icon": "⚙️",
        "label": "B2B Boardroom → Trench",
        "short_label": "B2B Boardroom → Trench",
        "arena_group": "Executive → Trench",
        "description": "Controlled Vykání → Tykání register drop from C-suite glass room to engineering floor."
    }
]

ARENA_8_CARDS = [
    {
        "uid": "CZ_OVA_SPARK_COMP",
        "register_id": "CZ_OVA",
        "stage": "COMPLIMENT",
        "arena": "spark",
        "title": "First-Impression Spark ? CZ_OVA COMPLIMENT",
        "text_html": "Čau, v téhle místnosti plné frází jde z tebe <span class=\"slang-token\" data-term=\"na první dobrou\">na první dobrou</span> úplně jiná jiskra – žádná <span class=\"slang-token\" data-term=\"navoněná bída\">navoněná bída</span>, ale čistá energie.",
        "phonetics": "[CHA-oo, v TEH-hle MEEST-nos-ti PL-neh FRAA-zee yde z TE-be na PRV-nee DOB-row OO-pl-nye YI-naa YISK-ra]",
        "english_gloss": "Hey, in this room full of clichés you radiate a completely different spark on the very first take—zero perfumed flash, pure energy.",
        "delivery_cue": "DE/RU Bridge: DE: Phrase (fráze), Energie • RU: комната (místnost), искра (jiskra), чистая энергия (čistá energie)",
        "idiom_terms": [
            "na první dobrou",
            "navoněná bída"
        ]
    },
    {
        "uid": "CZ_OVA_SPARK_CHAM",
        "register_id": "CZ_OVA",
        "stage": "CHAMELEON",
        "arena": "spark",
        "title": "First-Impression Spark ? CZ_OVA CHAMELEON",
        "text_html": "Hned vím, <span class=\"slang-token\" data-term=\"kaj\">kaj</span> patříš – žádné škrobené divadlo, prostě lidi, kterým to v hlavě okamžitě <span class=\"slang-token\" data-term=\"fachat\">fachá</span> na stejné vlně.",
        "phonetics": "[Hned veem, KAY PAT-reesh — ZHAAD-neh SHKRO-be-neh DI-vad-lo... FA-khaa na STEY-neh VL-nye]",
        "english_gloss": "I can tell right away where you belong—no starched theater, just people whose minds click on the exact same wavelength.",
        "delivery_cue": "DE/RU Bridge: DE: Fach (fachá = clicks/works) • RU: куда (kaj), в голове (v hlavě), на одной волне (na stejné vlně)",
        "idiom_terms": [
            "kaj",
            "fachat"
        ]
    },
    {
        "uid": "CZ_OVA_SPARK_COUNT",
        "register_id": "CZ_OVA",
        "stage": "COUNTERACT",
        "arena": "spark",
        "title": "First-Impression Spark ? CZ_OVA COUNTERACT",
        "text_html": "Stát tu u baru a bavit se o počasí by byla <span class=\"slang-token\" data-term=\"šichta\">šichta</span> za trest – dejme zdvořilostem <span class=\"slang-token\" data-term=\"fajront\">fajront</span>, <span class=\"slang-token\" data-term=\"bo\">bo</span> večer teprve začíná.",
        "phonetics": "[Staat tu u BA-ru a BA-vit se o PO-cha-see bi BI-la SHIKH-ta za trest — DEY-me ZDVO-zhi-los-tem FAY-ront, bo VE-cher TEP-r-ve ZA-chee-naa]",
        "english_gloss": "Standing by the bar talking about the weather would be a punishment shift—let’s give polite small talk quitting time, because the night is just starting.",
        "delivery_cue": "DE/RU Bridge: DE: Schicht (šichta), Feierabend (fajront) • RU: у бара (u baru), о погоде (o počasí), вечер начинается (večer začíná)",
        "idiom_terms": [
            "šichta",
            "fajront",
            "bo"
        ]
    },
    {
        "uid": "CZ_OVA_SPARK_CUR",
        "register_id": "CZ_OVA",
        "stage": "CURIOSITY",
        "arena": "spark",
        "title": "First-Impression Spark ? CZ_OVA CURIOSITY",
        "text_html": "Řekni mi bez filtru – jaký čerstvý nápad tě sem dneska večer doopravdy přitáhl?",
        "phonetics": "[REK-ni mi bez FILT-ru — YA-kee CHERST-vee NAA-pad tye sem DNES-ka VE-cher DO-op-rav-di PRI-taa-hl?]",
        "english_gloss": "Tell me unfiltered—what fresh idea actually pulled you in here tonight?",
        "delivery_cue": "DE/RU Bridge: DE: frisch (čerstvý ≠ RU черствый!), Einfall (nápad ≠ RU нападки!) • RU: без фильтра (bez filtru), сегодня вечером (dneska večer)",
        "idiom_terms": []
    },
    {
        "uid": "AT_VIE_SPARK_COMP",
        "register_id": "AT_VIE",
        "stage": "COMPLIMENT",
        "arena": "spark",
        "title": "First-Impression Spark ? AT_VIE COMPLIMENT",
        "text_html": "Servus, eines fällt sofort auf: Während der halbe Raum posiert, hast du eine Ausstrahlung, die echt <span class=\"slang-token\" data-term=\"schwer in Ordnung\">schwer in Ordnung</span> ist.",
        "phonetics": "",
        "english_gloss": "Hello there, one thing stands out immediately: while half the room poses, you carry a presence that is genuinely solid.",
        "delivery_cue": "",
        "idiom_terms": [
            "schwer in Ordnung"
        ]
    },
    {
        "uid": "AT_VIE_SPARK_CHAM",
        "register_id": "AT_VIE",
        "stage": "CHAMELEON",
        "arena": "spark",
        "title": "First-Impression Spark ? AT_VIE CHAMELEON",
        "text_html": "Kein Smalltalk, kein steifes <span class=\"slang-token\" data-term=\"G’schichtldrucken\">G’schichtldrucken</span> – man merkt in zehn Sekunden, dass wir denselben Schmäh haben.",
        "phonetics": "",
        "english_gloss": "Zero small talk, zero tall tales—you can tell in ten seconds we share the same dry wit.",
        "delivery_cue": "",
        "idiom_terms": [
            "G’schichtldrucken"
        ]
    },
    {
        "uid": "AT_VIE_SPARK_COUNT",
        "register_id": "AT_VIE",
        "stage": "COUNTERACT",
        "arena": "spark",
        "title": "First-Impression Spark ? AT_VIE COUNTERACT",
        "text_html": "Geh bitte, das höfliche Kennenlern-Protokoll können wir direkt <span class=\"slang-token\" data-term=\"an der Garderobe abgeben\">an der Garderobe abgeben</span>.",
        "phonetics": "",
        "english_gloss": "Come on now, let’s hand the polite introductory protocol straight to the coat check.",
        "delivery_cue": "",
        "idiom_terms": [
            "an der Garderobe abgeben"
        ]
    },
    {
        "uid": "AT_VIE_SPARK_CUR",
        "register_id": "AT_VIE",
        "stage": "CURIOSITY",
        "arena": "spark",
        "title": "First-Impression Spark ? AT_VIE CURIOSITY",
        "text_html": "Verrat mir eines: Was ist die spannendste Geschichte in diesem Raum, die außer dir noch keiner bemerkt hat?",
        "phonetics": "",
        "english_gloss": "Tell me one thing: what is the best story in this room that nobody besides you has spotted yet?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "RU_ALA_SPARK_COMP",
        "register_id": "RU_ALA",
        "stage": "COMPLIMENT",
        "arena": "spark",
        "title": "First-Impression Spark ? RU_ALA COMPLIMENT",
        "text_html": "Слушай, с первой секунды видно живой огонёк: весь образ и подача — прямо <span class=\"slang-token\" data-term=\"сделали по красоте\">сделали по красоте</span>.",
        "phonetics": "",
        "english_gloss": "Listen, from the very first second you see a real spark: your whole vibe is pure craft and beauty.",
        "delivery_cue": "",
        "idiom_terms": [
            "сделали по красоте"
        ]
    },
    {
        "uid": "RU_ALA_SPARK_CHAM",
        "register_id": "RU_ALA",
        "stage": "CHAMELEON",
        "arena": "spark",
        "title": "First-Impression Spark ? RU_ALA CHAMELEON",
        "text_html": "<span class=\"slang-token\" data-term=\"базару нет\">Базару нет</span>, сразу легко говорить <span class=\"slang-token\" data-term=\"без лишних понтов\">без лишних понтов</span> — будто знакомы уже сто лет.",
        "phonetics": "",
        "english_gloss": "No question, it’s effortless talking with zero hollow posturing—as if we’ve known each other for ages.",
        "delivery_cue": "",
        "idiom_terms": [
            "базару нет",
            "без лишних понтов"
        ]
    },
    {
        "uid": "RU_ALA_SPARK_COUNT",
        "register_id": "RU_ALA",
        "stage": "COUNTERACT",
        "arena": "spark",
        "title": "First-Impression Spark ? RU_ALA COUNTERACT",
        "text_html": "Но тратить такой вечер на дежурные фразы — это держать <span class=\"slang-token\" data-term=\"горный беркут в золотой клетке\">горный беркут в золотой клетке</span>.",
        "phonetics": "",
        "english_gloss": "Spending an evening like this on canned small talk is keeping a mountain golden eagle in a gilded cage.",
        "delivery_cue": "",
        "idiom_terms": [
            "горный беркут в золотой клетке"
        ]
    },
    {
        "uid": "RU_ALA_SPARK_CUR",
        "register_id": "RU_ALA",
        "stage": "CURIOSITY",
        "arena": "spark",
        "title": "First-Impression Spark ? RU_ALA CURIOSITY",
        "text_html": "Скажи честно: ради какого самого яркого момента ты вообще решил заглянуть сюда сегодня?",
        "phonetics": "",
        "english_gloss": "Tell me honestly: what’s the boldest moment you actually came looking for tonight?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_SPARK_COMP",
        "register_id": "EN_YYC",
        "stage": "COMPLIMENT",
        "arena": "spark",
        "title": "First-Impression Spark ? EN_YYC COMPLIMENT",
        "text_html": "Alright, time-out, bud—thirty seconds in and you’ve got more genuine spark than a whole room of folks who are <span class=\"slang-token\" data-term=\"all hat and no cattle\">all hat and no cattle</span>.",
        "phonetics": "",
        "english_gloss": "Instant warm Foothills opener contrasting real presence against superficial networking.",
        "delivery_cue": "",
        "idiom_terms": [
            "all hat and no cattle"
        ]
    },
    {
        "uid": "EN_YYC_SPARK_CHAM",
        "register_id": "EN_YYC",
        "stage": "CHAMELEON",
        "arena": "spark",
        "title": "First-Impression Spark ? EN_YYC CHAMELEON",
        "text_html": "Zero elevator pitch, zero rehearsed script—just quick wit and straight talk right out of the gate.",
        "phonetics": "",
        "english_gloss": "Direct alignment dropping corporate networking armor immediately.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_SPARK_COUNT",
        "register_id": "EN_YYC",
        "stage": "COUNTERACT",
        "arena": "spark",
        "title": "First-Impression Spark ? EN_YYC COUNTERACT",
        "text_html": "Sticking to polite weather chat right now would be like leaving a <span class=\"slang-token\" data-term=\"69 Mustang collecting dust\">69 Mustang collecting dust</span> in the driveway.",
        "phonetics": "",
        "english_gloss": "Playful pushback steering away from safe small talk.",
        "delivery_cue": "",
        "idiom_terms": [
            "69 Mustang collecting dust"
        ]
    },
    {
        "uid": "EN_YYC_SPARK_CUR",
        "register_id": "EN_YYC",
        "stage": "CURIOSITY",
        "arena": "spark",
        "title": "First-Impression Spark ? EN_YYC CURIOSITY",
        "text_html": "Skip the LinkedIn bio for me—what’s got you genuinely fired up this week?",
        "phonetics": "",
        "english_gloss": "Clean open-loop curiosity question inviting genuine passion.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_SPARK_COMP",
        "register_id": "ES_SOT",
        "stage": "COMPLIMENT",
        "arena": "spark",
        "title": "First-Impression Spark ? ES_SOT COMPLIMENT",
        "text_html": "Espera un segundo: nada más entrar se nota quién ilumina la sala y quién solo hace bulto—lo tuyo <span class=\"slang-token\" data-term=\"tiene duende\">tiene duende</span>.",
        "phonetics": "",
        "english_gloss": "Hold on a second: the moment you walk in you can tell who lights up the room—your vibe has real duende.",
        "delivery_cue": "",
        "idiom_terms": [
            "tiene duende"
        ]
    },
    {
        "uid": "ES_SOT_SPARK_CHAM",
        "register_id": "ES_SOT",
        "stage": "CHAMELEON",
        "arena": "spark",
        "title": "First-Impression Spark ? ES_SOT CHAMELEON",
        "text_html": "Qué gusto cruzar mirada con alguien cero impostado; conectamos al vuelo sin necesidad de presentaciones eternas.",
        "phonetics": "",
        "english_gloss": "What a pleasure meeting someone with zero pretense; instant wavelength without endless introductions.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_SPARK_COUNT",
        "register_id": "ES_SOT",
        "stage": "COUNTERACT",
        "arena": "spark",
        "title": "First-Impression Spark ? ES_SOT COUNTERACT",
        "text_html": "¡Ni de coña nos quedamos hablando del tiempo! Eso sería <span class=\"slang-token\" data-term=\"mirar los toros desde la barrera\">mirar los toros desde la barrera</span> en la mejor noche.",
        "phonetics": "",
        "english_gloss": "No way we stay talking about the weather! That would be watching the bulls from behind the barrier on the best night.",
        "delivery_cue": "",
        "idiom_terms": [
            "mirar los toros desde la barrera"
        ]
    },
    {
        "uid": "ES_SOT_SPARK_CUR",
        "register_id": "ES_SOT",
        "stage": "CURIOSITY",
        "arena": "spark",
        "title": "First-Impression Spark ? ES_SOT CURIOSITY",
        "text_html": "Dime la verdad: ¿qué plan inesperado haría que esta noche valga por diez?",
        "phonetics": "",
        "english_gloss": "Tell me the truth: what unexpected plan would make tonight worth ten?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "CZ_OVA_ADVENTURE_COMP",
        "register_id": "CZ_OVA",
        "stage": "COMPLIMENT",
        "arena": "adventure",
        "title": "Melting Hesitation ? CZ_OVA COMPLIMENT",
        "text_html": "Koukám na tebe a je jasné, že nejsi typ na nudný průměr – v tobě to umí pořádně <span class=\"slang-token\" data-term=\"fachat\">fachat</span>, když jde o velkou věc.",
        "phonetics": "[KOW-kaam na TE-be a ye YAS-neh, zhe NEY-si tip na NUD-nee PROO-myer — v TO-bye to U-mee PO-raad-nye FA-khat]",
        "english_gloss": "Looking at you, it’s clear you’re not built for boring averages—you fire on all cylinders when something big is on the line.",
        "delivery_cue": "DE/RU Bridge: DE: klar (jasné), Typ, Fach (fachat) • RU: скучный (nudný), большая вещь (velká věc)",
        "idiom_terms": [
            "fachat"
        ]
    },
    {
        "uid": "CZ_OVA_ADVENTURE_CHAM",
        "register_id": "CZ_OVA",
        "stage": "CHAMELEON",
        "arena": "adventure",
        "title": "Melting Hesitation ? CZ_OVA CHAMELEON",
        "text_html": "Přesně vím, <span class=\"slang-token\" data-term=\"kaj\">kaj</span> tě to táhne: nejlepší věci vznikají ve chvíli, kdy člověk zahodí zbytečný manuál.",
        "phonetics": "[PRES-nye veem, KAY tye to TAAH-ne: NEY-lep-shee VYE-tsi VZNI-ka-yee ve KHVEE-li, kdi CHLO-vyek ZA-ho-dee ZBI-tech-nee MA-nu-aal]",
        "english_gloss": "I know exactly where it pulls you: the best things happen the moment you toss out the unnecessary manual.",
        "delivery_cue": "DE/RU Bridge: DE: präzise (přesně ≠ RU пресный!), Manual • RU: куда тянет (kaj táhne), человек (člověk)",
        "idiom_terms": [
            "kaj"
        ]
    },
    {
        "uid": "CZ_OVA_ADVENTURE_COUNT",
        "register_id": "CZ_OVA",
        "stage": "COUNTERACT",
        "arena": "adventure",
        "title": "Melting Hesitation ? CZ_OVA COUNTERACT",
        "text_html": "Říkat „možná příště“ je jen další šedivá <span class=\"slang-token\" data-term=\"šichta\">šichta</span> v kalendáři – dej váhání <span class=\"slang-token\" data-term=\"fajront\">fajront</span>, <span class=\"slang-token\" data-term=\"bo\">bo</span> taková vlna nečeká.",
        "phonetics": "[REE-kat MOZH-naa PREESH-tye ye yen DAL-shee SHE-di-vaa SHIKH-ta v KA-len-daa-rhi — dey VAA-haa-nyee FAY-ront, bo TA-ko-vaa VL-na NE-che-kaa]",
        "english_gloss": "Saying \"maybe next time\" is just another grey shift on the calendar—give hesitation quitting time, because a wave like this doesn’t wait.",
        "delivery_cue": "DE/RU Bridge: DE: Schicht (šichta), Feierabend (fajront), Kalender • RU: может быть (možná), волна не ждёт (vlna nečeká)",
        "idiom_terms": [
            "šichta",
            "fajront",
            "bo"
        ]
    },
    {
        "uid": "CZ_OVA_ADVENTURE_CUR",
        "register_id": "CZ_OVA",
        "stage": "CURIOSITY",
        "arena": "adventure",
        "title": "Melting Hesitation ? CZ_OVA CURIOSITY",
        "text_html": "Tak pojď na první dobrou – kdybychom teď vyrazili mimo mapu na dvacet minut, kam zabočíme?",
        "phonetics": "[Tak poyd na PRV-nee DOB-row — KDI-bi-khom ted VI-ra-zi-li MI-mo MA-pu na DVA-tset MI-nut, kam ZA-bo-chee-me?]",
        "english_gloss": "So come on, first take—if we stepped off the map for twenty minutes right now, where are we turning?",
        "delivery_cue": "DE/RU Bridge: RU: пойдём (pojď), мимо карты (mimo mapu), двадцать минут (dvacet minut), куда свернём (kam zabočíme)",
        "idiom_terms": []
    },
    {
        "uid": "AT_VIE_ADVENTURE_COMP",
        "register_id": "AT_VIE",
        "stage": "COMPLIMENT",
        "arena": "adventure",
        "title": "Melting Hesitation ? AT_VIE COMPLIMENT",
        "text_html": "Du hast diesen Blick drauf, Oida – ruhig nach außen, aber innerlich bereit für ein Abenteuer, das <span class=\"slang-token\" data-term=\"schwer in Ordnung\">schwer in Ordnung</span> ist.",
        "phonetics": "",
        "english_gloss": "You’ve got that look—calm on the outside, but inwardly ready for a seriously great adventure.",
        "delivery_cue": "",
        "idiom_terms": [
            "schwer in Ordnung"
        ]
    },
    {
        "uid": "AT_VIE_ADVENTURE_CHAM",
        "register_id": "AT_VIE",
        "stage": "CHAMELEON",
        "arena": "adventure",
        "title": "Melting Hesitation ? AT_VIE CHAMELEON",
        "text_html": "Mir geht’s ja genauso: Die besten Nächte in Wien stehen in keinem Kalender und brauchen kein <span class=\"slang-token\" data-term=\"G’schichtldrucken\">G’schichtldrucken</span>.",
        "phonetics": "",
        "english_gloss": "I’m the exact same way: the best nights in Vienna aren’t in any calendar and need zero excuses.",
        "delivery_cue": "",
        "idiom_terms": [
            "G’schichtldrucken"
        ]
    },
    {
        "uid": "AT_VIE_ADVENTURE_COUNT",
        "register_id": "AT_VIE",
        "stage": "COUNTERACT",
        "arena": "adventure",
        "title": "Melting Hesitation ? AT_VIE COUNTERACT",
        "text_html": "„Vielleicht nächstes Mal“? Geh bitte, diese brave Vernunft geben wir jetzt für eine Stunde <span class=\"slang-token\" data-term=\"an der Garderobe abgeben\">an der Garderobe ab</span>.",
        "phonetics": "",
        "english_gloss": "\"Maybe next time\"? Come on, let’s hand that well-behaved caution to the coat check for an hour.",
        "delivery_cue": "",
        "idiom_terms": [
            "an der Garderobe abgeben"
        ]
    },
    {
        "uid": "AT_VIE_ADVENTURE_CUR",
        "register_id": "AT_VIE",
        "stage": "CURIOSITY",
        "arena": "adventure",
        "title": "Melting Hesitation ? AT_VIE CURIOSITY",
        "text_html": "Komm, zwanzig Minuten Umweg auf meine Kappe: Wohin entführen wir diesen Abend jetzt spontan?",
        "phonetics": "",
        "english_gloss": "Come on, twenty-minute detour on my tab: where are we spontaneously taking this evening right now?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "RU_ALA_ADVENTURE_COMP",
        "register_id": "RU_ALA",
        "stage": "COMPLIMENT",
        "arena": "adventure",
        "title": "Melting Hesitation ? RU_ALA COMPLIMENT",
        "text_html": "По глазам вижу, родной: в тебе живёт дух первооткрывателя, который всё делает с размахом и <span class=\"slang-token\" data-term=\"сделали по красоте\">по красоте</span>.",
        "phonetics": "",
        "english_gloss": "I can see it in your eyes, brother: you have an explorer’s spirit that does everything with scale and beauty.",
        "delivery_cue": "",
        "idiom_terms": [
            "сделали по красоте"
        ]
    },
    {
        "uid": "RU_ALA_ADVENTURE_CHAM",
        "register_id": "RU_ALA",
        "stage": "CHAMELEON",
        "arena": "adventure",
        "title": "Melting Hesitation ? RU_ALA CHAMELEON",
        "text_html": "<span class=\"slang-token\" data-term=\"базару нет\">Базару нет</span>, самые легендарные истории всегда начинаются со слов «а поехали прямо сейчас».",
        "phonetics": "",
        "english_gloss": "No question, the most legendary stories always start with \"let’s roll right now.\"",
        "delivery_cue": "",
        "idiom_terms": [
            "базару нет"
        ]
    },
    {
        "uid": "RU_ALA_ADVENTURE_COUNT",
        "register_id": "RU_ALA",
        "stage": "COUNTERACT",
        "arena": "adventure",
        "title": "Melting Hesitation ? RU_ALA COUNTERACT",
        "text_html": "Откладывать на потом — это снова запереть <span class=\"slang-token\" data-term=\"горный беркут в золотой клетке\">горный беркут в золотой клетке</span>, когда горы уже зовут.",
        "phonetics": "",
        "english_gloss": "Putting it off for later is locking a mountain eagle back in a golden cage when the mountains are already calling.",
        "delivery_cue": "",
        "idiom_terms": [
            "горный беркут в золотой клетке"
        ]
    },
    {
        "uid": "RU_ALA_ADVENTURE_CUR",
        "register_id": "RU_ALA",
        "stage": "CURIOSITY",
        "arena": "adventure",
        "title": "Melting Hesitation ? RU_ALA CURIOSITY",
        "text_html": "Давай без долгих сборов: если срываемся с места через пять минут — куда берём курс?",
        "phonetics": "",
        "english_gloss": "Zero long packing: if we take off in five minutes, where are we setting course?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_ADVENTURE_COMP",
        "register_id": "EN_YYC",
        "stage": "COMPLIMENT",
        "arena": "adventure",
        "title": "Melting Hesitation ? EN_YYC COMPLIMENT",
        "text_html": "You’ve got way too much maverick in you, bud, to pretend you came out tonight for a predictable script—nothing <span class=\"slang-token\" data-term=\"all hat and no cattle\">all hat and no cattle</span> about your vibe.",
        "phonetics": "",
        "english_gloss": "Warm challenge celebrating the counterpart’s adventurous streak.",
        "delivery_cue": "",
        "idiom_terms": [
            "all hat and no cattle"
        ]
    },
    {
        "uid": "EN_YYC_ADVENTURE_CHAM",
        "register_id": "EN_YYC",
        "stage": "CHAMELEON",
        "arena": "adventure",
        "title": "Melting Hesitation ? EN_YYC CHAMELEON",
        "text_html": "Best nights from Calgary to Europe always start the exact second you throw the itinerary in the glovebox.",
        "phonetics": "",
        "english_gloss": "Co-conspirator alignment around spontaneous detours.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_ADVENTURE_COUNT",
        "register_id": "EN_YYC",
        "stage": "COUNTERACT",
        "arena": "adventure",
        "title": "Melting Hesitation ? EN_YYC COUNTERACT",
        "text_html": "Saying \"let’s rain-check\" right now is keeping a <span class=\"slang-token\" data-term=\"69 Mustang collecting dust\">69 Mustang collecting dust</span> while the highway’s wide open.",
        "phonetics": "",
        "english_gloss": "Playful pattern interrupt melting hesitation.",
        "delivery_cue": "",
        "idiom_terms": [
            "69 Mustang collecting dust"
        ]
    },
    {
        "uid": "EN_YYC_ADVENTURE_CUR",
        "register_id": "EN_YYC",
        "stage": "CURIOSITY",
        "arena": "adventure",
        "title": "Melting Hesitation ? EN_YYC CURIOSITY",
        "text_html": "Thirty-minute audible, zero overthinking—if we duck out that side door right now, what’s chapter one?",
        "phonetics": "",
        "english_gloss": "Spontaneous low-pressure adventure invitation.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_ADVENTURE_COMP",
        "register_id": "ES_SOT",
        "stage": "COMPLIMENT",
        "arena": "adventure",
        "title": "Melting Hesitation ? ES_SOT COMPLIMENT",
        "text_html": "Se te ve en la mirada esa chispa indomable que <span class=\"slang-token\" data-term=\"tiene duende\">tiene duende</span>; tú no has nacido para planes tibios.",
        "phonetics": "",
        "english_gloss": "You can see that untamed spark with duende in your eyes; you weren’t born for lukewarm plans.",
        "delivery_cue": "",
        "idiom_terms": [
            "tiene duende"
        ]
    },
    {
        "uid": "ES_SOT_ADVENTURE_CHAM",
        "register_id": "ES_SOT",
        "stage": "CHAMELEON",
        "arena": "adventure",
        "title": "Melting Hesitation ? ES_SOT CHAMELEON",
        "text_html": "Somos iguales en eso: lo inolvidable empieza justo cuando cierras el reloj y te dejas llevar por el momento.",
        "phonetics": "",
        "english_gloss": "We’re alike in that: the unforgettable starts right when you stop checking the clock.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_ADVENTURE_COUNT",
        "register_id": "ES_SOT",
        "stage": "COUNTERACT",
        "arena": "adventure",
        "title": "Melting Hesitation ? ES_SOT COUNTERACT",
        "text_html": "¿Dejarlo para otro día? ¡Qué va! Eso es quedarse <span class=\"slang-token\" data-term=\"mirar los toros desde la barrera\">mirando los toros desde la barrera</span> cuando suena la música.",
        "phonetics": "",
        "english_gloss": "Leave it for another day? No chance! That’s watching the bulls from behind the barrier right as the music plays.",
        "delivery_cue": "",
        "idiom_terms": [
            "mirar los toros desde la barrera"
        ]
    },
    {
        "uid": "ES_SOT_ADVENTURE_CUR",
        "register_id": "ES_SOT",
        "stage": "CURIOSITY",
        "arena": "adventure",
        "title": "Melting Hesitation ? ES_SOT CURIOSITY",
        "text_html": "Venga, mójate conmigo veinte minutos: si nos escapamos del guion ahora mismo, ¿adónde tiramos?",
        "phonetics": "",
        "english_gloss": "Come on, jump in with me for twenty minutes: if we escape the script right now, where do we head?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "CZ_OVA_RUNWAY_COMP",
        "register_id": "CZ_OVA",
        "stage": "COMPLIMENT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? CZ_OVA COMPLIMENT",
        "text_html": "V zákulisí je hned vidět, kdo dělá jen <span class=\"slang-token\" data-term=\"navoněná bída\">navoněnou bídu</span> a komu to pod rukama čistě <span class=\"slang-token\" data-term=\"fachat\">fachá</span> – ten váš střih drží <span class=\"slang-token\" data-term=\"na první dobrou\">na první dobrou</span>.",
        "phonetics": "[V ZAA-ku-li-see ye hned VI-dyet... a KO-mu to pod RU-ka-ma CHIS-tye FA-khaa — ten vaash STRIH DR-zhee na PRV-nee DOB-row]",
        "english_gloss": "Backstage you see right away who makes perfumed flash and whose craft actually runs—your cut holds on the very first take.",
        "delivery_cue": "DE/RU Bridge: RU: за кулисами (v zákulisí), под руками (pod rukama) • DE: Fach/fachen (fachá = works), Schnitt (střih)",
        "idiom_terms": [
            "navoněná bída",
            "fachat",
            "na první dobrou"
        ]
    },
    {
        "uid": "CZ_OVA_RUNWAY_CHAM",
        "register_id": "CZ_OVA",
        "stage": "CHAMELEON",
        "arena": "runway",
        "title": "Runway & Zákulisí ? CZ_OVA CHAMELEON",
        "text_html": "V první řadě u mola všichni pózují, ale my dva víme, <span class=\"slang-token\" data-term=\"kaj\">kaj</span> se láme chleba – dole u švů a konstrukce.",
        "phonetics": "[V PRV-nee RHA-dye u MO-la VSHIKH-ni POO-zu-yee, a-le mi dva VEE-me, KAY se LAA-me KHLE-ba — DO-le u SHVOO a KON-struk-tse]",
        "english_gloss": "In the front row by the runway everyone poses, but the two of us know where it really counts—down in the seams and structure.",
        "delivery_cue": "DE/RU Bridge: DE: Konstruktion, Pose (pózují) • RU: в первом ряду (v první řadě), мы два знаем (my dva víme), хлеб (chleba), швы (švy)",
        "idiom_terms": [
            "kaj"
        ]
    },
    {
        "uid": "CZ_OVA_RUNWAY_COUNT",
        "register_id": "CZ_OVA",
        "stage": "COUNTERACT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? CZ_OVA COUNTERACT",
        "text_html": "Ale žehlit to v zákulisí ručně do noci je <span class=\"slang-token\" data-term=\"šichta\">šichta</span> pro blázny – pusťme ten hlavní kus na světlo, ať má ateliér čistý <span class=\"slang-token\" data-term=\"fajront\">fajront</span>, <span class=\"slang-token\" data-term=\"bo\">bo</span> látka nepustí.",
        "phonetics": "[A-le ZHEH-lit to v ZAA-ku-li-see RUCH-nye do NO-tsi ye SHIKH-ta pro BLAAZ-ni... CHIS-tee FAY-ront, bo LAAT-ka NE-pus-tee]",
        "english_gloss": "Steaming it manually backstage till midnight is a crazy shift—let’s send the flagship piece out under the lights so the atelier gets a clean Feierabend, because the fabric holds.",
        "delivery_cue": "DE/RU Bridge: DE: Schicht (šichta), Feierabend (fajront), Atelier • RU: ручно до ночи (ručně do noci), на свет (na světlo)",
        "idiom_terms": [
            "šichta",
            "fajront",
            "bo"
        ]
    },
    {
        "uid": "CZ_OVA_RUNWAY_CUR",
        "register_id": "CZ_OVA",
        "stage": "CURIOSITY",
        "arena": "runway",
        "title": "Runway & Zákulisí ? CZ_OVA CURIOSITY",
        "text_html": "Mezi námi u věšáků – který odvážný kus schováváte v ateliéru a ještě jste ho nepustili na molo?",
        "phonetics": "[ME-zi NAA-mi u VYE-shaa-koo — KTE-ree OD-vaazh-nee kus SKHO-vaa-vaa-te v A-te-li-eh-ru a YESH-tye yste ho NE-pus-ti-li na MO-lo?]",
        "english_gloss": "Between us by the garment racks—what bold piece are you hiding in the atelier that hasn’t hit the runway yet?",
        "delivery_cue": "DE/RU Bridge: DE: Atelier • RU: между нами (mezi námi), отважный кусок (odvážný kus), прячете (schováváte)",
        "idiom_terms": []
    },
    {
        "uid": "AT_VIE_RUNWAY_COMP",
        "register_id": "AT_VIE",
        "stage": "COMPLIMENT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? AT_VIE COMPLIMENT",
        "text_html": "Backstage merkt man sofort: Kein lautes Theater, sondern echtes Handwerk – euer Schnitt ist <span class=\"slang-token\" data-term=\"schwer in Ordnung\">schwer in Ordnung</span>.",
        "phonetics": "",
        "english_gloss": "Backstage you notice immediately: zero loud theater, just real craft—your cut is seriously solid.",
        "delivery_cue": "",
        "idiom_terms": [
            "schwer in Ordnung"
        ]
    },
    {
        "uid": "AT_VIE_RUNWAY_CHAM",
        "register_id": "AT_VIE",
        "stage": "CHAMELEON",
        "arena": "runway",
        "title": "Runway & Zákulisí ? AT_VIE CHAMELEON",
        "text_html": "Vorne blitzen die Kameras, aber wir schauen auf die Naht – ganz ohne PR-<span class=\"slang-token\" data-term=\"G’schichtldrucken\">G’schichtldrucken</span>.",
        "phonetics": "",
        "english_gloss": "Up front the cameras flash, while we inspect the seam—zero PR tall tales.",
        "delivery_cue": "",
        "idiom_terms": [
            "G’schichtldrucken"
        ]
    },
    {
        "uid": "AT_VIE_RUNWAY_COUNT",
        "register_id": "AT_VIE",
        "stage": "COUNTERACT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? AT_VIE COUNTERACT",
        "text_html": "Die falsche Bescheidenheit vor dem Finale solltet ihr samt Sedcard <span class=\"slang-token\" data-term=\"an der Garderobe abgeben\">an der Garderobe abgeben</span>.",
        "phonetics": "",
        "english_gloss": "You ought to check that false modesty right at the coat check before the finale.",
        "delivery_cue": "",
        "idiom_terms": [
            "an der Garderobe abgeben"
        ]
    },
    {
        "uid": "AT_VIE_RUNWAY_CUR",
        "register_id": "AT_VIE",
        "stage": "CURIOSITY",
        "arena": "runway",
        "title": "Runway & Zákulisí ? AT_VIE CURIOSITY",
        "text_html": "Unter uns im Atelier: Welches geheime Meisterstück schicken wir als Nächstes unangekündigt ins Scheinwerferlicht?",
        "phonetics": "",
        "english_gloss": "Between us in the atelier: what secret masterpiece are we sending unannounced into the spotlight next?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "RU_ALA_RUNWAY_COMP",
        "register_id": "RU_ALA",
        "stage": "COMPLIMENT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? RU_ALA COMPLIMENT",
        "text_html": "За кулисами сразу видно руку мастера, родной: каждый шов с изнанки — прямо <span class=\"slang-token\" data-term=\"сделали по красоте\">сделали по красоте</span>.",
        "phonetics": "",
        "english_gloss": "Backstage you spot the master’s hand right away, brother: every inner seam is built with real beauty.",
        "delivery_cue": "",
        "idiom_terms": [
            "сделали по красоте"
        ]
    },
    {
        "uid": "RU_ALA_RUNWAY_CHAM",
        "register_id": "RU_ALA",
        "stage": "CHAMELEON",
        "arena": "runway",
        "title": "Runway & Zákulisí ? RU_ALA CHAMELEON",
        "text_html": "<span class=\"slang-token\" data-term=\"базару нет\">Базару нет</span>, подиум любит вспышки, а мы с тобой ценим честный крой <span class=\"slang-token\" data-term=\"без лишних понтов\">без лишних понтов</span>.",
        "phonetics": "",
        "english_gloss": "No question, the runway loves flashbulbs, while we value an honest cut with zero hollow flexing.",
        "delivery_cue": "",
        "idiom_terms": [
            "базару нет",
            "без лишних понтов"
        ]
    },
    {
        "uid": "RU_ALA_RUNWAY_COUNT",
        "register_id": "RU_ALA",
        "stage": "COUNTERACT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? RU_ALA COUNTERACT",
        "text_html": "Прятать лучшую коллекцию в чехлах — это как <span class=\"slang-token\" data-term=\"горный беркут в золотой клетке\">горный беркут в золотой клетке</span> посреди недели моды.",
        "phonetics": "",
        "english_gloss": "Hiding your best collection inside garment bags is like a mountain eagle in a golden cage mid-fashion-week.",
        "delivery_cue": "",
        "idiom_terms": [
            "горный беркут в золотой клетке"
        ]
    },
    {
        "uid": "RU_ALA_RUNWAY_CUR",
        "register_id": "RU_ALA",
        "stage": "CURIOSITY",
        "arena": "runway",
        "title": "Runway & Zákulisí ? RU_ALA CURIOSITY",
        "text_html": "Скажи по секрету за кулисами: какой главный выход перевернёт весь зал сегодня вечером?",
        "phonetics": "",
        "english_gloss": "Tell me backstage: what flagship walk is going to turn the whole hall upside down tonight?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_RUNWAY_COMP",
        "register_id": "EN_YYC",
        "stage": "COMPLIMENT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? EN_YYC COMPLIMENT",
        "text_html": "In a fashion tent where half the front row is <span class=\"slang-token\" data-term=\"all hat and no cattle\">all hat and no cattle</span>, bud, your tailoring actually carries real horsepower.",
        "phonetics": "",
        "english_gloss": "Backstage Foothills praise separating real structural craft from front-row hype.",
        "delivery_cue": "",
        "idiom_terms": [
            "all hat and no cattle"
        ]
    },
    {
        "uid": "EN_YYC_RUNWAY_CHAM",
        "register_id": "EN_YYC",
        "stage": "CHAMELEON",
        "arena": "runway",
        "title": "Runway & Zákulisí ? EN_YYC CHAMELEON",
        "text_html": "Love the backstage vibe here—steamers running, zero ego, everyone focused on how the fabric actually moves.",
        "phonetics": "",
        "english_gloss": "Maker-to-maker backstage rapport.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_RUNWAY_COUNT",
        "register_id": "EN_YYC",
        "stage": "COUNTERACT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? EN_YYC COUNTERACT",
        "text_html": "Keeping your boldest silhouette on the rack right now is like a <span class=\"slang-token\" data-term=\"69 Mustang collecting dust\">69 Mustang collecting dust</span> behind the curtain.",
        "phonetics": "",
        "english_gloss": "Playful challenge pushing the signature piece onto the runway.",
        "delivery_cue": "",
        "idiom_terms": [
            "69 Mustang collecting dust"
        ]
    },
    {
        "uid": "EN_YYC_RUNWAY_CUR",
        "register_id": "EN_YYC",
        "stage": "CURIOSITY",
        "arena": "runway",
        "title": "Runway & Zákulisí ? EN_YYC CURIOSITY",
        "text_html": "Before the house lights drop—what’s the wildcard piece you’re dying to send down that catwalk first?",
        "phonetics": "",
        "english_gloss": "Backstage open-loop hook right before curtain.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_RUNWAY_COMP",
        "register_id": "ES_SOT",
        "stage": "COMPLIMENT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? ES_SOT COMPLIMENT",
        "text_html": "Cuando se apagan los focos de la pasarela, lo único que manda es el corte—y el vuestro <span class=\"slang-token\" data-term=\"tiene duende\">tiene duende</span> en cada costura.",
        "phonetics": "",
        "english_gloss": "When the runway lights go dark, only the cut rules—and yours has duende in every seam.",
        "delivery_cue": "",
        "idiom_terms": [
            "tiene duende"
        ]
    },
    {
        "uid": "ES_SOT_RUNWAY_CHAM",
        "register_id": "ES_SOT",
        "stage": "CHAMELEON",
        "arena": "runway",
        "title": "Runway & Zákulisí ? ES_SOT CHAMELEON",
        "text_html": "Aquí en el backstage se respira oficio de verdad, con esa <span class=\"slang-token\" data-term=\"tener buena muñeca\">buena muñeca</span> que no necesita aplauso fácil.",
        "phonetics": "",
        "english_gloss": "Backstage you breathe real craft, with that effortless wrist finesse that needs zero easy applause.",
        "delivery_cue": "",
        "idiom_terms": [
            "tener buena muñeca"
        ]
    },
    {
        "uid": "ES_SOT_RUNWAY_COUNT",
        "register_id": "ES_SOT",
        "stage": "COUNTERACT",
        "arena": "runway",
        "title": "Runway & Zákulisí ? ES_SOT COUNTERACT",
        "text_html": "Guardar el diseño estrella en el camerino es <span class=\"slang-token\" data-term=\"mirar los toros desde la barrera\">mirar los toros desde la barrera</span> en plena noche de estreno.",
        "phonetics": "",
        "english_gloss": "Keeping the star design in the dressing room is watching the bulls from behind the barrier on opening night.",
        "delivery_cue": "",
        "idiom_terms": [
            "mirar los toros desde la barrera"
        ]
    },
    {
        "uid": "ES_SOT_RUNWAY_CUR",
        "register_id": "ES_SOT",
        "stage": "CURIOSITY",
        "arena": "runway",
        "title": "Runway & Zákulisí ? ES_SOT CURIOSITY",
        "text_html": "Entre bastidores, dime: ¿qué prenda rompe-esquemas sacamos ahora mismo para cerrar el desfile?",
        "phonetics": "",
        "english_gloss": "Behind the scenes, tell me: what rule-breaking piece do we send out right now to close the show?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "CZ_OVA_HOCHKULTUR_COMP",
        "register_id": "CZ_OVA",
        "stage": "COMPLIMENT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? CZ_OVA COMPLIMENT",
        "text_html": "Mezi tolika fraky v lóži je radost potkat někoho, komu za tou noblesou doopravdy <span class=\"slang-token\" data-term=\"fachat\">fachá</span> hlava i poctivý grunt.",
        "phonetics": "[ME-zi TO-li-ka FRA-ki v LOO-zhi ye RA-dost POT-kat NYE-ko-ho... FA-khaa HLA-va i PO-tsi-vee grunt]",
        "english_gloss": "Among so many tailcoats in the opera box, it’s a joy meeting someone whose mind and solid foundation genuinely run underneath the elegance.",
        "delivery_cue": "DE/RU Bridge: DE: Frack (frak), Loge (lóže), Grund (grunt = foundation), Fach (fachá) • RU: радость встретить (radost potkat), голова (hlava)",
        "idiom_terms": [
            "fachat"
        ]
    },
    {
        "uid": "CZ_OVA_HOCHKULTUR_CHAM",
        "register_id": "CZ_OVA",
        "stage": "CHAMELEON",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? CZ_OVA CHAMELEON",
        "text_html": "Když o přestávce <span class=\"slang-token\" data-term=\"odložit smoking\">odložíme smoking</span>, hned vidím, <span class=\"slang-token\" data-term=\"kaj\">kaj</span> míříš – žádné prázdné árie, ale čistá souhra.",
        "phonetics": "[Kdish o PRES-taav-tse OD-lo-zhee-me SMO-king, hned VI-deem, KAY MEE-reesh — ZHAAD-neh PRAAZD-neh AA-ri-ye]",
        "english_gloss": "When we figuratively take off the tuxedo at intermission, I see right where you’re aiming—no hollow arias, just clean ensemble play.",
        "delivery_cue": "DE/RU Bridge: DE: Smoking (tuxedo), Arie (árie) • RU: отложим смокинг (odložíme smoking), куда метишь (kaj míříš), чистая сыгранность (čistá souhra)",
        "idiom_terms": [
            "odložit smoking",
            "kaj"
        ]
    },
    {
        "uid": "CZ_OVA_HOCHKULTUR_COUNT",
        "register_id": "CZ_OVA",
        "stage": "COUNTERACT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? CZ_OVA COUNTERACT",
        "text_html": "Dirigovat každý detail ručně je ale umělecká <span class=\"slang-token\" data-term=\"šichta\">šichta</span> – dej té salónní opatrnosti <span class=\"slang-token\" data-term=\"fajront\">fajront</span>, <span class=\"slang-token\" data-term=\"bo\">bo</span> orchestr už zná partituru.",
        "phonetics": "[DI-ri-go-vat KAZH-dee DE-tayl RUCH-nye ye A-le U-mye-lets-kaa SHIKH-ta — dey teh SA-loon-nyee O-pat-r-nos-ti FAY-ront, bo OR-khest-r uzh znaa PAR-ti-tu-ru]",
        "english_gloss": "Conducting every detail manually is an artistic grind—give that salon caution quitting time, because the orchestra already knows the score.",
        "delivery_cue": "DE/RU Bridge: DE: dirigieren, Schicht (šichta), Feierabend (fajront), Orchester, Partitur • RU: каждый деталь ручно (každý detail ručně)",
        "idiom_terms": [
            "šichta",
            "fajront",
            "bo"
        ]
    },
    {
        "uid": "CZ_OVA_HOCHKULTUR_CUR",
        "register_id": "CZ_OVA",
        "stage": "CURIOSITY",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? CZ_OVA CURIOSITY",
        "text_html": "Řekni mi u sklenky v salónku – jaké velké druhé dějství rozehrajeme, jakmile zhasne lustr?",
        "phonetics": "[REK-ni mi u SKLEN-ki v SA-loon-ku — YA-keh VEL-keh DRU-heh DYEY-stvee RO-ze-hra-ye-me, YAK-mi-le ZHAS-ne LUST-r?]",
        "english_gloss": "Tell me over a glass in the salon—what grand second act are we launching the moment the chandelier dims?",
        "delivery_cue": "DE/RU Bridge: DE: Salon, Lüster (lustr) • RU: у стакана/бокала (u sklenky), второе действие (druhé dějství), погаснет люстра (zhasne lustr)",
        "idiom_terms": []
    },
    {
        "uid": "AT_VIE_HOCHKULTUR_COMP",
        "register_id": "AT_VIE",
        "stage": "COMPLIMENT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? AT_VIE COMPLIMENT",
        "text_html": "In der Staatsoper-Loge trifft man viele Blender, Oida, aber deine Linie hat Stil und ist <span class=\"slang-token\" data-term=\"schwer in Ordnung\">schwer in Ordnung</span>.",
        "phonetics": "",
        "english_gloss": "In the Staatsoper box you meet plenty of bluffers, man, yet your vision has real style and substance.",
        "delivery_cue": "",
        "idiom_terms": [
            "schwer in Ordnung"
        ]
    },
    {
        "uid": "AT_VIE_HOCHKULTUR_CHAM",
        "register_id": "AT_VIE",
        "stage": "CHAMELEON",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? AT_VIE CHAMELEON",
        "text_html": "Zwischen zwei Akten beim Sekt merkt man sofort: Wir brauchen keine <span class=\"slang-token\" data-term=\"Pflanzerei\">Pflanzerei</span> und kein <span class=\"slang-token\" data-term=\"G’schichtldrucken\">G’schichtldrucken</span>.",
        "phonetics": "",
        "english_gloss": "Between two acts over sparkling wine you notice right away: we need zero gallery bluffing and zero tall tales.",
        "delivery_cue": "",
        "idiom_terms": [
            "Pflanzerei",
            "G’schichtldrucken"
        ]
    },
    {
        "uid": "AT_VIE_HOCHKULTUR_COUNT",
        "register_id": "AT_VIE",
        "stage": "COUNTERACT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? AT_VIE COUNTERACT",
        "text_html": "Die heilige Ehrfurcht vor dem alten Protokoll sollten wir vor dem dritten Gong <span class=\"slang-token\" data-term=\"an der Garderobe abgeben\">an der Garderobe abgeben</span>.",
        "phonetics": "",
        "english_gloss": "Let’s check that sacred reverence for old protocol at the coat check before the third intermission gong.",
        "delivery_cue": "",
        "idiom_terms": [
            "an der Garderobe abgeben"
        ]
    },
    {
        "uid": "AT_VIE_HOCHKULTUR_CUR",
        "register_id": "AT_VIE",
        "stage": "CURIOSITY",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? AT_VIE CURIOSITY",
        "text_html": "Unter uns in der Loge: Welchen mutigen Hauptakt heben wir nach der Pause direkt auf die große Bühne?",
        "phonetics": "",
        "english_gloss": "Between us in the box: what bold main act are we lifting straight onto the grand stage after intermission?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "RU_ALA_HOCHKULTUR_COMP",
        "register_id": "RU_ALA",
        "stage": "COMPLIMENT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? RU_ALA COMPLIMENT",
        "text_html": "Под этими люстрами много громких слов, брат, но за твоей идеей чувствуется порода — <span class=\"slang-token\" data-term=\"сделали по красоте\">сделали по красоте</span>.",
        "phonetics": "",
        "english_gloss": "Under these chandeliers there are plenty of loud words, brother, yet behind your idea you feel real pedigree and craft.",
        "delivery_cue": "",
        "idiom_terms": [
            "сделали по красоте"
        ]
    },
    {
        "uid": "RU_ALA_HOCHKULTUR_CHAM",
        "register_id": "RU_ALA",
        "stage": "CHAMELEON",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? RU_ALA CHAMELEON",
        "text_html": "<span class=\"slang-token\" data-term=\"базару нет\">Базару нет</span>, высокое искусство мы любим, но ценим разговор <span class=\"slang-token\" data-term=\"без лишних понтов\">без лишних понтов</span> в антракте.",
        "phonetics": "",
        "english_gloss": "No question, we appreciate high art while valuing a conversation with zero hollow posturing at intermission.",
        "delivery_cue": "",
        "idiom_terms": [
            "базару нет",
            "без лишних понтов"
        ]
    },
    {
        "uid": "RU_ALA_HOCHKULTUR_COUNT",
        "register_id": "RU_ALA",
        "stage": "COUNTERACT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? RU_ALA COUNTERACT",
        "text_html": "Держать такой замысел в камерном формате — это <span class=\"slang-token\" data-term=\"горный беркут в золотой клетке\">горный беркут в золотой клетке</span> под бархатным занавесом.",
        "phonetics": "",
        "english_gloss": "Keeping a vision of that scale in a tiny chamber format is a mountain eagle in a gilded cage behind velvet curtains.",
        "delivery_cue": "",
        "idiom_terms": [
            "горный беркут в золотой клетке"
        ]
    },
    {
        "uid": "RU_ALA_HOCHKULTUR_CUR",
        "register_id": "RU_ALA",
        "stage": "CURIOSITY",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? RU_ALA CURIOSITY",
        "text_html": "Скажи мне в антракте: какую самую смелую премьеру мы выведем на главную сцену этой весной?",
        "phonetics": "",
        "english_gloss": "Tell me at intermission: what boldest premiere are we bringing onto the main stage next?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_HOCHKULTUR_COMP",
        "register_id": "EN_YYC",
        "stage": "COMPLIMENT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? EN_YYC COMPLIMENT",
        "text_html": "Even under crystal chandeliers, bud, it takes five seconds to spot someone with real substance in a gallery full of <span class=\"slang-token\" data-term=\"all hat and no cattle\">all hat and no cattle</span>.",
        "phonetics": "",
        "english_gloss": "Disarming Calgary candor cutting warmly through velvet-rope formality.",
        "delivery_cue": "",
        "idiom_terms": [
            "all hat and no cattle"
        ]
    },
    {
        "uid": "EN_YYC_HOCHKULTUR_CHAM",
        "register_id": "EN_YYC",
        "stage": "CHAMELEON",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? EN_YYC CHAMELEON",
        "text_html": "Appreciate the black-tie craft, love the straight-shooting conversation at the champagne bar even more.",
        "phonetics": "",
        "english_gloss": "Peer alignment blending salon poise with Foothills directness.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_HOCHKULTUR_COUNT",
        "register_id": "EN_YYC",
        "stage": "COUNTERACT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? EN_YYC COUNTERACT",
        "text_html": "Keeping your flagship move behind velvet ropes is like parking a <span class=\"slang-token\" data-term=\"69 Mustang collecting dust\">69 Mustang collecting dust</span> in a museum.",
        "phonetics": "",
        "english_gloss": "Playful challenge bringing museum-locked ideas into live motion.",
        "delivery_cue": "",
        "idiom_terms": [
            "69 Mustang collecting dust"
        ]
    },
    {
        "uid": "EN_YYC_HOCHKULTUR_CUR",
        "register_id": "EN_YYC",
        "stage": "CURIOSITY",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? EN_YYC CURIOSITY",
        "text_html": "Before the third chime calls us back—what’s the headline act we’re greenlighting once the tuxedos come off?",
        "phonetics": "",
        "english_gloss": "Intermission open-loop hook.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_HOCHKULTUR_COMP",
        "register_id": "ES_SOT",
        "stage": "COMPLIMENT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? ES_SOT COMPLIMENT",
        "text_html": "Entre tanta etiqueta de gala, encontrar una mente con criterio propio y obra que <span class=\"slang-token\" data-term=\"tiene duende\">tiene duende</span> es oro puro.",
        "phonetics": "",
        "english_gloss": "Amid so much gala etiquette, meeting an independent mind whose work truly has duende is pure gold.",
        "delivery_cue": "",
        "idiom_terms": [
            "tiene duende"
        ]
    },
    {
        "uid": "ES_SOT_HOCHKULTUR_CHAM",
        "register_id": "ES_SOT",
        "stage": "CHAMELEON",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? ES_SOT CHAMELEON",
        "text_html": "Nos entendemos con media mirada en el foyer: elegancia toda, pero <span class=\"slang-token\" data-term=\"tener buena muñeca\">buena muñeca</span> y verdad por delante.",
        "phonetics": "",
        "english_gloss": "Half a glance in the foyer and we get each other: full elegance, with real finesse and truth up front.",
        "delivery_cue": "",
        "idiom_terms": [
            "tener buena muñeca"
        ]
    },
    {
        "uid": "ES_SOT_HOCHKULTUR_COUNT",
        "register_id": "ES_SOT",
        "stage": "COUNTERACT",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? ES_SOT COUNTERACT",
        "text_html": "Quedarse solo en el brindis de salón sería <span class=\"slang-token\" data-term=\"mirar los toros desde la barrera\">mirar los toros desde la barrera</span> teniendo el escenario listo.",
        "phonetics": "",
        "english_gloss": "Staying just at the salon toast would be watching the bulls from behind the barrier when the stage is ready.",
        "delivery_cue": "",
        "idiom_terms": [
            "mirar los toros desde la barrera"
        ]
    },
    {
        "uid": "ES_SOT_HOCHKULTUR_CUR",
        "register_id": "ES_SOT",
        "stage": "CURIOSITY",
        "arena": "hochkultur",
        "title": "Staatsoper & Hochkultur ? ES_SOT CURIOSITY",
        "text_html": "Dime aquí en el palco: ¿qué gran obra estrenamos juntos cuando se abra el telón de verdad?",
        "phonetics": "",
        "english_gloss": "Tell me right here in the box: what grand work do we premiere together when the real curtain rises?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "CZ_OVA_POLO_COMP",
        "register_id": "CZ_OVA",
        "stage": "COMPLIMENT",
        "arena": "polo",
        "title": "Polo Club Paddock ? CZ_OVA COMPLIMENT",
        "text_html": "U hrazení v paddocku je hned vidět, <span class=\"slang-token\" data-term=\"kaj\">kaj</span> je skutečná síla v tahu – máte to osedlané tak čistě, že to na pažitu <span class=\"slang-token\" data-term=\"fachat\">fachá</span> jako hodinky.",
        "phonetics": "[U HRA-ze-nyee v PA-do-ku ye hned VI-dyet, KAY ye SKU-tech-naa SEE-la v TA-hu... FA-khaa YA-ko HO-din-ki]",
        "english_gloss": "By the paddock rail you see right away where the real pulling power is—you’ve saddled this so cleanly it runs on the turf like clockwork.",
        "delivery_cue": "DE/RU Bridge: DE: Paddock, Zugkraft (síla v tahu), Fach (fachá) • RU: сила (síla), как часики (jako hodinky — ≠ hodina = 1 hour!)",
        "idiom_terms": [
            "kaj",
            "fachat"
        ]
    },
    {
        "uid": "CZ_OVA_POLO_CHAM",
        "register_id": "CZ_OVA",
        "stage": "CHAMELEON",
        "arena": "polo",
        "title": "Polo Club Paddock ? CZ_OVA CHAMELEON",
        "text_html": "Bílé kalhoty a šampaňské jsou fajn kulisa, ale my koukáme pod sedlo – na poctivý trénink a klidnou ruku.",
        "phonetics": "[BEE-leh KAL-ho-ti a SHAM-pan-skeh ysow fayn KU-li-sa, a-le mi KOW-kaa-me pod SED-lo — na PO-tsi-vee TREH-nink]",
        "english_gloss": "White breeches and champagne are nice scenery, yet we look under the saddle—at honest training and a steady hand.",
        "delivery_cue": "DE/RU Bridge: DE: Champagner, fein (fajn), Kulisse, Sattel (sedlo), Training • RU: белые (bílé), под седло (pod sedlo), спокойная рука (klidná ruka)",
        "idiom_terms": []
    },
    {
        "uid": "CZ_OVA_POLO_COUNT",
        "register_id": "CZ_OVA",
        "stage": "COUNTERACT",
        "arena": "polo",
        "title": "Polo Club Paddock ? CZ_OVA COUNTERACT",
        "text_html": "Zašlapávat drny ručně mezi chukkery je zbytečná <span class=\"slang-token\" data-term=\"šichta\">šichta</span> – dejte brzdám <span class=\"slang-token\" data-term=\"fajront\">fajront</span>, <span class=\"slang-token\" data-term=\"bo\">bo</span> ten plnokrevník chce plný cval.",
        "phonetics": "[ZA-shla-paa-vat DR-ni RUCH-nye ME-zi CHA-ke-ri ye ZBI-tech-naa SHIKH-ta — DEY-te BRZ-daam FAY-ront, bo ten PL-no-krev-nyeek khtse PL-nee tsval]",
        "english_gloss": "Stomping divots manually between chukkers is an unnecessary grind—give the brakes quitting time, because that thoroughbred wants full gallop.",
        "delivery_cue": "DE/RU Bridge: DE: Schicht (šichta), Feierabend (fajront), Vollblut (plnokrevník) • RU: ручно (ručně), тормозам (brzdám), полный галоп (plný cval)",
        "idiom_terms": [
            "šichta",
            "fajront",
            "bo"
        ]
    },
    {
        "uid": "CZ_OVA_POLO_CUR",
        "register_id": "CZ_OVA",
        "stage": "CURIOSITY",
        "arena": "polo",
        "title": "Polo Club Paddock ? CZ_OVA CURIOSITY",
        "text_html": "Řekni mi u zábradlí – až teď rozhodčí zapíská další chukker, do jakého tahu půjdeme s plnou parou?",
        "phonetics": "[REK-ni mi u ZAA-brad-lee — azh ted ROZ-hod-chee ZA-pees-kaa DAL-shee CHA-ker, do YA-keh-ho TA-hu POOY-de-me s PL-now PA-row?]",
        "english_gloss": "Tell me by the rail—when the umpire whistles the next chukker, what breakaway play are we riding into at full steam?",
        "delivery_cue": "DE/RU Bridge: DE: Volldampf (s plnou parou) • RU: скажи мне (řekni mi), запищит/просвистит (zapíská), с полным паром (s plnou parou)",
        "idiom_terms": []
    },
    {
        "uid": "AT_VIE_POLO_COMP",
        "register_id": "AT_VIE",
        "stage": "COMPLIMENT",
        "arena": "polo",
        "title": "Polo Club Paddock ? AT_VIE COMPLIMENT",
        "text_html": "Am Polo-Rasen sieht man zwischen zwei Chukkern sofort, wer Ruhe im Sattel hat – euer Tempo ist <span class=\"slang-token\" data-term=\"schwer in Ordnung\">schwer in Ordnung</span>.",
        "phonetics": "",
        "english_gloss": "On the polo lawn between chukkers you see right away who has calm in the saddle—your pace is genuinely solid.",
        "delivery_cue": "",
        "idiom_terms": [
            "schwer in Ordnung"
        ]
    },
    {
        "uid": "AT_VIE_POLO_CHAM",
        "register_id": "AT_VIE",
        "stage": "CHAMELEON",
        "arena": "polo",
        "title": "Polo Club Paddock ? AT_VIE CHAMELEON",
        "text_html": "Keine schicke <span class=\"slang-token\" data-term=\"Pflanzerei\">Pflanzerei</span> am Champagnerzelt, kein <span class=\"slang-token\" data-term=\"G’schichtldrucken\">G’schichtldrucken</span> – nur echtes Timing.",
        "phonetics": "",
        "english_gloss": "Zero fancy bluffing at the champagne tent, zero tall tales—pure timing.",
        "delivery_cue": "",
        "idiom_terms": [
            "Pflanzerei",
            "G’schichtldrucken"
        ]
    },
    {
        "uid": "AT_VIE_POLO_COUNT",
        "register_id": "AT_VIE",
        "stage": "COUNTERACT",
        "arena": "polo",
        "title": "Polo Club Paddock ? AT_VIE COUNTERACT",
        "text_html": "Die angezogene Handbremse im letzten Chukker geben wir jetzt aber schleunigst <span class=\"slang-token\" data-term=\"an der Garderobe abgeben\">an der Garderobe ab</span>.",
        "phonetics": "",
        "english_gloss": "Let’s hand that pulled handbrake to the coat check before the final chukker.",
        "delivery_cue": "",
        "idiom_terms": [
            "an der Garderobe abgeben"
        ]
    },
    {
        "uid": "AT_VIE_POLO_CUR",
        "register_id": "AT_VIE",
        "stage": "CURIOSITY",
        "arena": "polo",
        "title": "Polo Club Paddock ? AT_VIE CURIOSITY",
        "text_html": "Sag ehrlich an der Bande: Welchen weiten Schlag wagen wir sofort beim nächsten Anritt?",
        "phonetics": "",
        "english_gloss": "Tell me straight by the boards: what long downfield shot are we taking on the very next ride-off?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "RU_ALA_POLO_COMP",
        "register_id": "RU_ALA",
        "stage": "COMPLIMENT",
        "arena": "polo",
        "title": "Polo Club Paddock ? RU_ALA COMPLIMENT",
        "text_html": "У кромки поля сразу видна порода и хватка, брат: как вы держите темп в седле — <span class=\"slang-token\" data-term=\"сделали по красоте\">сделали по красоте</span>.",
        "phonetics": "",
        "english_gloss": "At the edge of the field you immediately see pedigree and grip, brother: your pace in the saddle is pure craft.",
        "delivery_cue": "",
        "idiom_terms": [
            "сделали по красоте"
        ]
    },
    {
        "uid": "RU_ALA_POLO_CHAM",
        "register_id": "RU_ALA",
        "stage": "CHAMELEON",
        "arena": "polo",
        "title": "Polo Club Paddock ? RU_ALA CHAMELEON",
        "text_html": "<span class=\"slang-token\" data-term=\"базару нет\">Базару нет</span>, в наших краях коней чувствуют сердцем — всё честно и <span class=\"slang-token\" data-term=\"без лишних понтов\">без лишних понтов</span>.",
        "phonetics": "",
        "english_gloss": "No question, where we come from you feel horses with your heart—honest and with zero hollow flexing.",
        "delivery_cue": "",
        "idiom_terms": [
            "базару нет",
            "без лишних понтов"
        ]
    },
    {
        "uid": "RU_ALA_POLO_COUNT",
        "register_id": "RU_ALA",
        "stage": "COUNTERACT",
        "arena": "polo",
        "title": "Polo Club Paddock ? RU_ALA COUNTERACT",
        "text_html": "Придерживать такого скакуна у бортика — всё равно что держать <span class=\"slang-token\" data-term=\"горный беркут в золотой клетке\">горный беркут в золотой клетке</span>.",
        "phonetics": "",
        "english_gloss": "Holding a thoroughbred like that back by the boards is like keeping a mountain golden eagle in a gilded cage.",
        "delivery_cue": "",
        "idiom_terms": [
            "горный беркут в золотой клетке"
        ]
    },
    {
        "uid": "RU_ALA_POLO_CUR",
        "register_id": "RU_ALA",
        "stage": "CURIOSITY",
        "arena": "polo",
        "title": "Polo Club Paddock ? RU_ALA CURIOSITY",
        "text_html": "Скажи между чаккерами: если сейчас отпустить поводья на полную — какую цель берём сходу?",
        "phonetics": "",
        "english_gloss": "Tell me between chukkers: if we drop the reins into full gallop right now, what target do we take first?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_POLO_COMP",
        "register_id": "EN_YYC",
        "stage": "COMPLIMENT",
        "arena": "polo",
        "title": "Polo Club Paddock ? EN_YYC COMPLIMENT",
        "text_html": "Out here by the paddock rail, bud, it’s clear in two seconds who actually rides—zero <span class=\"slang-token\" data-term=\"all hat and no cattle\">all hat and no cattle</span> in your saddle.",
        "phonetics": "",
        "english_gloss": "Paddock-side respect connecting Alberta horsemanship with high-goal polo.",
        "delivery_cue": "",
        "idiom_terms": [
            "all hat and no cattle"
        ]
    },
    {
        "uid": "EN_YYC_POLO_CHAM",
        "register_id": "EN_YYC",
        "stage": "CHAMELEON",
        "arena": "polo",
        "title": "Polo Club Paddock ? EN_YYC CHAMELEON",
        "text_html": "Different hemisphere, same rule from Spruce Meadows to Sotogrande: trust the horse, keep clean hands, let the pace breathe.",
        "phonetics": "",
        "english_gloss": "Equestrian peer bond across Calgary and Sotogrande.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_POLO_COUNT",
        "register_id": "EN_YYC",
        "stage": "COUNTERACT",
        "arena": "polo",
        "title": "Polo Club Paddock ? EN_YYC COUNTERACT",
        "text_html": "Holding that horsepower back in the fourth chukker is like leaving a <span class=\"slang-token\" data-term=\"69 Mustang collecting dust\">69 Mustang collecting dust</span> in the barn.",
        "phonetics": "",
        "english_gloss": "Playful challenge unlocking full-field pace.",
        "delivery_cue": "",
        "idiom_terms": [
            "69 Mustang collecting dust"
        ]
    },
    {
        "uid": "EN_YYC_POLO_CUR",
        "register_id": "EN_YYC",
        "stage": "CURIOSITY",
        "arena": "polo",
        "title": "Polo Club Paddock ? EN_YYC CURIOSITY",
        "text_html": "Bell’s about to ring for the final chukker—where are we sending the long ball right off the throw-in?",
        "phonetics": "",
        "english_gloss": "High-momentum paddock open loop.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_POLO_COMP",
        "register_id": "ES_SOT",
        "stage": "COMPLIMENT",
        "arena": "polo",
        "title": "Polo Club Paddock ? ES_SOT COMPLIMENT",
        "text_html": "En Santa María se ve al vuelo quién <span class=\"slang-token\" data-term=\"tener buena muñeca\">tiene buena muñeca</span> y temple—vuestro juego <span class=\"slang-token\" data-term=\"tiene duende\">tiene duende</span> en la cancha.",
        "phonetics": "",
        "english_gloss": "At Santa María you spot right away who has effortless wrist touch and poise—your game has real duende on the field.",
        "delivery_cue": "",
        "idiom_terms": [
            "tener buena muñeca",
            "tiene duende"
        ]
    },
    {
        "uid": "ES_SOT_POLO_CHAM",
        "register_id": "ES_SOT",
        "stage": "CHAMELEON",
        "arena": "polo",
        "title": "Polo Club Paddock ? ES_SOT CHAMELEON",
        "text_html": "Brisa de levante, caballos finos y cero postureo en las tablas; hablamos exactamente el mismo idioma.",
        "phonetics": "",
        "english_gloss": "Levante breeze, fine horses, and zero posturing by the boards; we speak the exact same language.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_POLO_COUNT",
        "register_id": "ES_SOT",
        "stage": "COUNTERACT",
        "arena": "polo",
        "title": "Polo Club Paddock ? ES_SOT COUNTERACT",
        "text_html": "Con esa cuadra, reservarse ahora es <span class=\"slang-token\" data-term=\"mirar los toros desde la barrera\">mirar los toros desde la barrera</span> en el último chukker.",
        "phonetics": "",
        "english_gloss": "With a string of horses like that, holding back now is watching the bulls from behind the barrier in the final chukker.",
        "delivery_cue": "",
        "idiom_terms": [
            "mirar los toros desde la barrera"
        ]
    },
    {
        "uid": "ES_SOT_POLO_CUR",
        "register_id": "ES_SOT",
        "stage": "CURIOSITY",
        "arena": "polo",
        "title": "Polo Club Paddock ? ES_SOT CURIOSITY",
        "text_html": "Dime antes de subir al caballo: ¿qué jugada maestra lanzamos nada más sonar la campana?",
        "phonetics": "",
        "english_gloss": "Tell me before mounting up: what master play do we launch the second the bell rings?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "CZ_OVA_WIEN_COMP",
        "register_id": "CZ_OVA",
        "stage": "COMPLIMENT",
        "arena": "wien",
        "title": "Station Wien Café ? CZ_OVA COMPLIMENT",
        "text_html": "Tady v rohovém boxu nad melange je klid – líbí se mi, jak máte celou věc v hlavě srovnanou <span class=\"slang-token\" data-term=\"na první dobrou\">na první dobrou</span> a bez šumu.",
        "phonetics": "[TA-di v RO-ho-vehm BO-xu nad ME-lanzh ye klid — LEE-bee se mi, yak MAA-te TSE-low vyets v HLA-vye SROV-na-now na PRV-nee DOB-row]",
        "english_gloss": "Here in the corner booth over a Melange it’s calm—I admire how cleanly and noiselessly you’ve got the whole picture lined up.",
        "delivery_cue": "DE/RU Bridge: DE: Melange, Box • RU: покой (klid), в голове (v hlavě), без шума (bez šumu)",
        "idiom_terms": [
            "na první dobrou"
        ]
    },
    {
        "uid": "CZ_OVA_WIEN_CHAM",
        "register_id": "CZ_OVA",
        "stage": "CHAMELEON",
        "arena": "wien",
        "title": "Station Wien Café ? CZ_OVA CHAMELEON",
        "text_html": "Mezi čtyřma očima je hned jasné, <span class=\"slang-token\" data-term=\"kaj\">kaj</span> vedou nitky – diskrétně, přesně a tak, aby to v tichosti <span class=\"slang-token\" data-term=\"fachat\">fachalo</span>.",
        "phonetics": "[ME-zi CHTIR-ma O-chi-ma ye hned YAS-neh, KAY VE-dow NYIT-ki — DISK-reht-nye, PRES-nye a tak, A-bi to v TI-khos-ti FA-kha-lo]",
        "english_gloss": "Under four eyes it’s immediately clear where the threads lead—discreetly, accurately, and built to run quietly.",
        "delivery_cue": "DE/RU Bridge: DE: unter vier Augen (mezi čtyřma očima), diskret, präzise (přesně), Fach (fachalo) • RU: нитки (nitky), в тишине (v tichosti)",
        "idiom_terms": [
            "kaj",
            "fachat"
        ]
    },
    {
        "uid": "CZ_OVA_WIEN_COUNT",
        "register_id": "CZ_OVA",
        "stage": "COUNTERACT",
        "arena": "wien",
        "title": "Station Wien Café ? CZ_OVA COUNTERACT",
        "text_html": "Posílat to přes deset razítek je úřednická <span class=\"slang-token\" data-term=\"šichta\">šichta</span> – dejme papírům <span class=\"slang-token\" data-term=\"fajront\">fajront</span>, <span class=\"slang-token\" data-term=\"bo\">bo</span> nejlepší dohody padnou tady u mramorového stolku.",
        "phonetics": "[PO-see-lat to pres DE-set RA-zee-tek ye OO-rhed-nits-kaa SHIKH-ta — DEY-me PA-pee-room FAY-ront, bo NEY-lep-shee DO-ho-di PAD-now TA-di]",
        "english_gloss": "Routing this through ten rubber stamps is a bureaucratic grind—give the paperwork quitting time, because the best agreements happen right here at the marble table.",
        "delivery_cue": "DE/RU Bridge: DE: Schicht (šichta), Feierabend (fajront), Papier, Marmor • RU: десять (deset), договор (dohoda)",
        "idiom_terms": [
            "šichta",
            "fajront",
            "bo"
        ]
    },
    {
        "uid": "CZ_OVA_WIEN_CUR",
        "register_id": "CZ_OVA",
        "stage": "CURIOSITY",
        "arena": "wien",
        "title": "Station Wien Café ? CZ_OVA CURIOSITY",
        "text_html": "Zůstane to čistě u tohohle stolu – který klíčový tah spouštíte příští týden pod radarem?",
        "phonetics": "[ZOO-sta-ne to CHIS-tye u TO-ho-hle STO-lu — KTE-ree KLEE-cho-vee tah SPOOSH-tyee-te PREESH-tyee TEE-den pod RA-da-rem?]",
        "english_gloss": "Strictly stays at this marble table—what key move are you launching under the radar next week?",
        "delivery_cue": "DE/RU Bridge: DE: Schlüsselzug (klíčový tah), unter dem Radar • RU: у этого стола (u tohohle stolu), ключевой ход (klíčový tah)",
        "idiom_terms": []
    },
    {
        "uid": "AT_VIE_WIEN_COMP",
        "register_id": "AT_VIE",
        "stage": "COMPLIMENT",
        "arena": "wien",
        "title": "Station Wien Café ? AT_VIE COMPLIMENT",
        "text_html": "Hier hinten in der Kaffeehaus-Loge bei einer Melange merkt man gleich: Deine Ruhe im Spiel ist <span class=\"slang-token\" data-term=\"schwer in Ordnung\">schwer in Ordnung</span>.",
        "phonetics": "",
        "english_gloss": "Back here in the corner Kaffeehaus booth over a Melange you notice right away: your quiet poise is seriously solid.",
        "delivery_cue": "",
        "idiom_terms": [
            "schwer in Ordnung"
        ]
    },
    {
        "uid": "AT_VIE_WIEN_CHAM",
        "register_id": "AT_VIE",
        "stage": "CHAMELEON",
        "arena": "wien",
        "title": "Station Wien Café ? AT_VIE CHAMELEON",
        "text_html": "Unter vier Augen am Marmortisch braucht’s kein <span class=\"slang-token\" data-term=\"G’schichtldrucken\">G’schichtldrucken</span> und keine <span class=\"slang-token\" data-term=\"Pflanzerei\">Pflanzerei</span> – ein Nicken reicht.",
        "phonetics": "",
        "english_gloss": "Under four eyes at the marble table there’s zero need for tall tales or bluffing—one nod suffices.",
        "delivery_cue": "",
        "idiom_terms": [
            "G’schichtldrucken",
            "Pflanzerei"
        ]
    },
    {
        "uid": "AT_VIE_WIEN_COUNT",
        "register_id": "AT_VIE",
        "stage": "COUNTERACT",
        "arena": "wien",
        "title": "Station Wien Café ? AT_VIE COUNTERACT",
        "text_html": "Das offizielle Ausschuss-Theater lassen wir draußen im Regen stehen und geben es <span class=\"slang-token\" data-term=\"an der Garderobe abgeben\">an der Garderobe ab</span>.",
        "phonetics": "",
        "english_gloss": "Let’s leave the official committee theater out in the rain and check it at the coat check.",
        "delivery_cue": "",
        "idiom_terms": [
            "an der Garderobe abgeben"
        ]
    },
    {
        "uid": "AT_VIE_WIEN_CUR",
        "register_id": "AT_VIE",
        "stage": "CURIOSITY",
        "arena": "wien",
        "title": "Station Wien Café ? AT_VIE CURIOSITY",
        "text_html": "Ganz diskret beim kleinen Braunen: Welchen leisen Schachzug setzen wir vor Freitag auf die Schiene?",
        "phonetics": "",
        "english_gloss": "Quietly over an espresso: what subtle chess move do we put on the rails before Friday?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "RU_ALA_WIEN_COMP",
        "register_id": "RU_ALA",
        "stage": "COMPLIMENT",
        "arena": "wien",
        "title": "Station Wien Café ? RU_ALA COMPLIMENT",
        "text_html": "За этим угловым столиком в Вене сразу чувствуется школа, родной: тихо, точно и <span class=\"slang-token\" data-term=\"сделали по красоте\">сделали по красоте</span>.",
        "phonetics": "",
        "english_gloss": "At this corner table in Vienna you immediately feel real pedigree, brother: quiet, exact, and crafted with beauty.",
        "delivery_cue": "",
        "idiom_terms": [
            "сделали по красоте"
        ]
    },
    {
        "uid": "RU_ALA_WIEN_CHAM",
        "register_id": "RU_ALA",
        "stage": "CHAMELEON",
        "arena": "wien",
        "title": "Station Wien Café ? RU_ALA CHAMELEON",
        "text_html": "<span class=\"slang-token\" data-term=\"базару нет\">Базару нет</span>, большие дела любят тишину и честное слово <span class=\"slang-token\" data-term=\"без лишних понтов\">без лишних понтов</span>.",
        "phonetics": "",
        "english_gloss": "No question, serious moves love quiet discretion and an honest word with zero posturing.",
        "delivery_cue": "",
        "idiom_terms": [
            "базару нет",
            "без лишних понтов"
        ]
    },
    {
        "uid": "RU_ALA_WIEN_COUNT",
        "register_id": "RU_ALA",
        "stage": "COUNTERACT",
        "arena": "wien",
        "title": "Station Wien Café ? RU_ALA COUNTERACT",
        "text_html": "Ждать десять согласований — это держать <span class=\"slang-token\" data-term=\"горный беркут в золотой клетке\">горный беркут в золотой клетке</span> бумажной волокиты.",
        "phonetics": "",
        "english_gloss": "Waiting on ten committee sign-offs is locking a mountain golden eagle in a cage of red tape.",
        "delivery_cue": "",
        "idiom_terms": [
            "горный беркут в золотой клетке"
        ]
    },
    {
        "uid": "RU_ALA_WIEN_CUR",
        "register_id": "RU_ALA",
        "stage": "CURIOSITY",
        "arena": "wien",
        "title": "Station Wien Café ? RU_ALA CURIOSITY",
        "text_html": "Между нами за чашкой кофе: какой тихий ход мы согласуем прямо сейчас одним рукопожатием?",
        "phonetics": "",
        "english_gloss": "Between us over coffee: what quiet move do we lock in right now with a single handshake?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_WIEN_COMP",
        "register_id": "EN_YYC",
        "stage": "COMPLIMENT",
        "arena": "wien",
        "title": "Station Wien Café ? EN_YYC COMPLIMENT",
        "text_html": "Gotta love a quiet Vienna corner booth, bud—zero noise, zero <span class=\"slang-token\" data-term=\"all hat and no cattle\">all hat and no cattle</span>, just two people who actually move the needle.",
        "phonetics": "",
        "english_gloss": "Warm Station Wien corner-booth rapport with grounded Calgary candor.",
        "delivery_cue": "",
        "idiom_terms": [
            "all hat and no cattle"
        ]
    },
    {
        "uid": "EN_YYC_WIEN_CHAM",
        "register_id": "EN_YYC",
        "stage": "CHAMELEON",
        "arena": "wien",
        "title": "Station Wien Café ? EN_YYC CHAMELEON",
        "text_html": "Best calls never happen on a thirty-person Zoom; they happen over two espressos and a napkin sketch right here.",
        "phonetics": "",
        "english_gloss": "Corner-table conspiracy alignment.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_WIEN_COUNT",
        "register_id": "EN_YYC",
        "stage": "COUNTERACT",
        "arena": "wien",
        "title": "Station Wien Café ? EN_YYC COUNTERACT",
        "text_html": "Letting committee red tape stall this play is like leaving a <span class=\"slang-token\" data-term=\"69 Mustang collecting dust\">69 Mustang collecting dust</span> in diplomatic parking.",
        "phonetics": "",
        "english_gloss": "Wry Station Wien pushback against bureaucratic drift.",
        "delivery_cue": "",
        "idiom_terms": [
            "69 Mustang collecting dust"
        ]
    },
    {
        "uid": "EN_YYC_WIEN_CUR",
        "register_id": "EN_YYC",
        "stage": "CURIOSITY",
        "arena": "wien",
        "title": "Station Wien Café ? EN_YYC CURIOSITY",
        "text_html": "Off the record before the waiter brings the check—what’s the quiet move we’re locking in first?",
        "phonetics": "",
        "english_gloss": "Discreet corner-table open loop.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_WIEN_COMP",
        "register_id": "ES_SOT",
        "stage": "COMPLIMENT",
        "arena": "wien",
        "title": "Station Wien Café ? ES_SOT COMPLIMENT",
        "text_html": "En este rincón tranquilo de café vienés se nota quién juega el ajedrez fino: tu planteamiento <span class=\"slang-token\" data-term=\"tiene duende\">tiene duende</span> y precisión.",
        "phonetics": "",
        "english_gloss": "In this quiet Viennese café corner you can tell who plays fine chess: your approach has both duende and precision.",
        "delivery_cue": "",
        "idiom_terms": [
            "tiene duende"
        ]
    },
    {
        "uid": "ES_SOT_WIEN_CHAM",
        "register_id": "ES_SOT",
        "stage": "CHAMELEON",
        "arena": "wien",
        "title": "Station Wien Café ? ES_SOT CHAMELEON",
        "text_html": "Media voz, <span class=\"slang-token\" data-term=\"tener buena muñeca\">buena muñeca</span> y confianza limpia en la mesa de mármol—así es como salen las jugadas serias.",
        "phonetics": "",
        "english_gloss": "Low voice, subtle wrist finesse, and clean trust at the marble table—that’s how serious plays get done.",
        "delivery_cue": "",
        "idiom_terms": [
            "tener buena muñeca"
        ]
    },
    {
        "uid": "ES_SOT_WIEN_COUNT",
        "register_id": "ES_SOT",
        "stage": "COUNTERACT",
        "arena": "wien",
        "title": "Station Wien Café ? ES_SOT COUNTERACT",
        "text_html": "Esperar al comité eterno sería <span class=\"slang-token\" data-term=\"mirar los toros desde la barrera\">mirar los toros desde la barrera</span> teniendo la llave en la mano.",
        "phonetics": "",
        "english_gloss": "Waiting on an endless committee would be watching the bulls from behind the barrier while holding the key in your hand.",
        "delivery_cue": "",
        "idiom_terms": [
            "mirar los toros desde la barrera"
        ]
    },
    {
        "uid": "ES_SOT_WIEN_CUR",
        "register_id": "ES_SOT",
        "stage": "CURIOSITY",
        "arena": "wien",
        "title": "Station Wien Café ? ES_SOT CURIOSITY",
        "text_html": "Aquí en confianza frente al café: ¿qué movimiento silencioso activamos esta misma semana?",
        "phonetics": "",
        "english_gloss": "Here in confidence over coffee: what quiet move do we activate this very week?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "CZ_OVA_B2B_COMP",
        "register_id": "CZ_OVA",
        "stage": "COMPLIMENT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? CZ_OVA COMPLIMENT",
        "text_html": "Dobrý den u jednacího stolu – ta vaše architektura je úžasný kus práce a základ drží <span class=\"slang-token\" data-term=\"na první dobrou\">na první dobrou</span>, žádná <span class=\"slang-token\" data-term=\"navoněná bída\">navoněná bída</span>.",
        "phonetics": "[DOB-ree den u YED-na-tsee-ho STO-lu — ta VA-she AR-khi-tek-tu-ra ye OO-zhas-nee kus PRAA-tse a ZAA-klad DR-zhee na PRV-nee DOB-row]",
        "english_gloss": "Good day at the boardroom table—your architecture is an amazing piece of engineering and the foundation holds on the first take, zero perfumed flash.",
        "delivery_cue": "DE/RU Bridge: DE: Architektur, erstaunlich (úžasný ≠ RU ужасный!) • RU: добрый день (dobrý den), работа (práce), основа держит (základ drží)",
        "idiom_terms": [
            "na první dobrou",
            "navoněná bída"
        ]
    },
    {
        "uid": "CZ_OVA_B2B_CHAM",
        "register_id": "CZ_OVA",
        "stage": "CHAMELEON",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? CZ_OVA CHAMELEON",
        "text_html": "A jestli dovolíte, <span class=\"slang-token\" data-term=\"odložit smoking\">odložme kravaty</span> – v terénu hned vidím, <span class=\"slang-token\" data-term=\"kaj\">kaj</span> vás brzdí ruční předávky, zatímco jádro má čistě <span class=\"slang-token\" data-term=\"fachat\">fachat</span>.",
        "phonetics": "[A YES-tli DO-vo-lee-te, OD-lozh-me KRA-va-ti — v TE-reh-nu hned VI-deem, KAY vaas BRZ-dyee RUCH-nyee PRE-daav-ki... CHIS-tye FA-khat]",
        "english_gloss": "And if you allow, let’s drop the ties—on the engineering floor I see right away where manual handoffs slow you down, when the core should just run cleanly.",
        "delivery_cue": "DE/RU Bridge: DE: Krawatte (kravata), Terrain (terén), Fach (fachat) • RU: отложим галстуки (odložme kravaty), куда (kaj), ручные (ruční)",
        "idiom_terms": [
            "odložit smoking",
            "kaj",
            "fachat"
        ]
    },
    {
        "uid": "CZ_OVA_B2B_COUNT",
        "register_id": "CZ_OVA",
        "stage": "COUNTERACT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? CZ_OVA COUNTERACT",
        "text_html": "Pálit seniorní inženýry na slepování tabulek je drahá <span class=\"slang-token\" data-term=\"šichta\">šichta</span> – dejme téhle dřině <span class=\"slang-token\" data-term=\"fajront\">fajront</span>, <span class=\"slang-token\" data-term=\"bo\">bo</span> automatizace to sfoukne za hodinu.",
        "phonetics": "[PAA-lit SE-ni-or-nyee IN-zhe-nee-ri na SLE-po-vaa-nyee TA-bu-lek ye DRA-haa SHIKH-ta — DEY-me TEH-hle DRHI-nye FAY-ront, bo AW-to-ma-ti-za-tse to SFOWK-ne za HO-di-nu]",
        "english_gloss": "Burning senior engineers on patching spreadsheets is an expensive shift—let’s give that grind quitting time, because automation handles it in one hour.",
        "delivery_cue": "DE/RU Bridge: DE: Ingenieur, Schicht (šichta), Feierabend (fajront), Stunde (hodina ≠ RU година!) • RU: дорого (drahá), автоматизация",
        "idiom_terms": [
            "šichta",
            "fajront",
            "bo"
        ]
    },
    {
        "uid": "CZ_OVA_B2B_CUR",
        "register_id": "CZ_OVA",
        "stage": "CURIOSITY",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? CZ_OVA CURIOSITY",
        "text_html": "Řekni mi teď na rovinu jako inženýr inženýrovi – které úzké hrdlo v produkci vyřešíme v pilotu jako úplně první?",
        "phonetics": "[REK-ni mi ted na RO-vi-nu YA-ko IN-zhe-neer IN-zhe-nee-ro-vi — KTE-reh OOZ-keh HRD-lo v PRO-duk-tsi VI-rhe-shee-me v PI-lo-tu YA-ko OO-pl-nye PRV-nyee?]",
        "english_gloss": "Tell me straight now, engineer to engineer—which production bottleneck do we eliminate very first in the pilot?",
        "delivery_cue": "DE/RU Bridge: DE: Engpass (úzké hrdlo), Produktion, Pilot • RU: как инженер инженеру (jako inženýr inženýrovi), узкое горло (úzké hrdlo)",
        "idiom_terms": []
    },
    {
        "uid": "AT_VIE_B2B_COMP",
        "register_id": "AT_VIE",
        "stage": "COMPLIMENT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? AT_VIE COMPLIMENT",
        "text_html": "Im Boardroom sieht man selten ein System mit so sauberer Substanz – technisch ist das <span class=\"slang-token\" data-term=\"schwer in Ordnung\">schwer in Ordnung</span>.",
        "phonetics": "",
        "english_gloss": "In the boardroom you rarely see a system with such clean substance—technically that is seriously solid.",
        "delivery_cue": "",
        "idiom_terms": [
            "schwer in Ordnung"
        ]
    },
    {
        "uid": "AT_VIE_B2B_CHAM",
        "register_id": "AT_VIE",
        "stage": "CHAMELEON",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? AT_VIE CHAMELEON",
        "text_html": "Lassen wir die Folien-<span class=\"slang-token\" data-term=\"Pflanzerei\">Pflanzerei</span> und das <span class=\"slang-token\" data-term=\"G’schichtldrucken\">G’schichtldrucken</span> weg und reden wir direkt wie im Maschinenraum.",
        "phonetics": "",
        "english_gloss": "Let’s skip the slide-deck window-dressing and tall tales and talk directly like in the engine room.",
        "delivery_cue": "",
        "idiom_terms": [
            "Pflanzerei",
            "G’schichtldrucken"
        ]
    },
    {
        "uid": "AT_VIE_B2B_COUNT",
        "register_id": "AT_VIE",
        "stage": "COUNTERACT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? AT_VIE COUNTERACT",
        "text_html": "Eure besten Entwickler mit manuellen Freigaben aufzuhalten? Diese Bremse geben wir heute <span class=\"slang-token\" data-term=\"an der Garderobe abgeben\">an der Garderobe ab</span>.",
        "phonetics": "",
        "english_gloss": "Holding up your best developers with manual approvals? Let’s check that brake at the coat check today.",
        "delivery_cue": "",
        "idiom_terms": [
            "an der Garderobe abgeben"
        ]
    },
    {
        "uid": "AT_VIE_B2B_CUR",
        "register_id": "AT_VIE",
        "stage": "CURIOSITY",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? AT_VIE CURIOSITY",
        "text_html": "Von Techniker zu Techniker: Welchen Flaschenhals drehen wir im ersten Zwei-Wochen-Sprint sofort ab?",
        "phonetics": "",
        "english_gloss": "Engineer to engineer: which bottleneck do we shut off immediately in the first two-week sprint?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "RU_ALA_B2B_COMP",
        "register_id": "RU_ALA",
        "stage": "COMPLIMENT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? RU_ALA COMPLIMENT",
        "text_html": "На уровне совета директоров скажу прямо: ядро системы вы собрали крепко и <span class=\"slang-token\" data-term=\"сделали по красоте\">сделали по красоте</span>.",
        "phonetics": "",
        "english_gloss": "At the boardroom level I’ll say it straight: you built the core system solidly and with real craft.",
        "delivery_cue": "",
        "idiom_terms": [
            "сделали по красоте"
        ]
    },
    {
        "uid": "RU_ALA_B2B_CHAM",
        "register_id": "RU_ALA",
        "stage": "CHAMELEON",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? RU_ALA CHAMELEON",
        "text_html": "<span class=\"slang-token\" data-term=\"базару нет\">Базару нет</span>, давай без галстуков и <span class=\"slang-token\" data-term=\"без лишних понтов\">без лишних понтов</span> перейдём сразу к тому, как дышит продакшн.",
        "phonetics": "",
        "english_gloss": "No question, let’s drop the ties and zero hollow slides and go straight to how production breathes.",
        "delivery_cue": "",
        "idiom_terms": [
            "базару нет",
            "без лишних понтов"
        ]
    },
    {
        "uid": "RU_ALA_B2B_COUNT",
        "register_id": "RU_ALA",
        "stage": "COUNTERACT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? RU_ALA COUNTERACT",
        "text_html": "Грузить сильных инженеров ручной рутиной — это держать <span class=\"slang-token\" data-term=\"горный беркут в золотой клетке\">горный беркут в золотой клетке</span> таблиц и отчётов.",
        "phonetics": "",
        "english_gloss": "Loading strong engineers with manual drudgery is keeping a mountain golden eagle in a cage of spreadsheets.",
        "delivery_cue": "",
        "idiom_terms": [
            "горный беркут в золотой клетке"
        ]
    },
    {
        "uid": "RU_ALA_B2B_CUR",
        "register_id": "RU_ALA",
        "stage": "CURIOSITY",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? RU_ALA CURIOSITY",
        "text_html": "Скажи как технарь технарю: какой самый узкий узел в пайплайне мы развяжем первым уже на этой неделе?",
        "phonetics": "",
        "english_gloss": "Tell me engineer to engineer: what tightest knot in the pipeline do we untie first this very week?",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_B2B_COMP",
        "register_id": "EN_YYC",
        "stage": "COMPLIMENT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? EN_YYC COMPLIMENT",
        "text_html": "Stepping out of the C-suite slide deck, bud—your core engineering team is zero <span class=\"slang-token\" data-term=\"all hat and no cattle\">all hat and no cattle</span>; that architecture is rock-solid.",
        "phonetics": "",
        "english_gloss": "Executive-to-engineering praise validating real technical horsepower.",
        "delivery_cue": "",
        "idiom_terms": [
            "all hat and no cattle"
        ]
    },
    {
        "uid": "EN_YYC_B2B_CHAM",
        "register_id": "EN_YYC",
        "stage": "CHAMELEON",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? EN_YYC CHAMELEON",
        "text_html": "Let’s loosen the ties and talk shop floor: clean APIs, deterministic pipelines, zero death-by-PowerPoint.",
        "phonetics": "",
        "english_gloss": "Clean register drop from boardroom formality to trench candor.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "EN_YYC_B2B_COUNT",
        "register_id": "EN_YYC",
        "stage": "COUNTERACT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? EN_YYC COUNTERACT",
        "text_html": "Having senior devs babysit manual handoffs is like using a <span class=\"slang-token\" data-term=\"69 Mustang collecting dust\">69 Mustang collecting dust</span> just to haul groceries.",
        "phonetics": "",
        "english_gloss": "Sharp B2B pattern interrupt against manual engineering waste.",
        "delivery_cue": "",
        "idiom_terms": [
            "69 Mustang collecting dust"
        ]
    },
    {
        "uid": "EN_YYC_B2B_CUR",
        "register_id": "EN_YYC",
        "stage": "CURIOSITY",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? EN_YYC CURIOSITY",
        "text_html": "Whiteboard to production—if we wire up a clean two-week pilot tomorrow, which bottleneck are we knocking out first?",
        "phonetics": "",
        "english_gloss": "Concrete B2B pilot open-loop hook.",
        "delivery_cue": "",
        "idiom_terms": []
    },
    {
        "uid": "ES_SOT_B2B_COMP",
        "register_id": "ES_SOT",
        "stage": "COMPLIMENT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? ES_SOT COMPLIMENT",
        "text_html": "En la sala de juntas se ven mil presentaciones, pero vuestra ingeniería de base <span class=\"slang-token\" data-term=\"tiene duende\">tiene duende</span> y solidez real.",
        "phonetics": "",
        "english_gloss": "In the boardroom you see a thousand slide decks, yet your core engineering has real duende and solidity.",
        "delivery_cue": "",
        "idiom_terms": [
            "tiene duende"
        ]
    },
    {
        "uid": "ES_SOT_B2B_CHAM",
        "register_id": "ES_SOT",
        "stage": "CHAMELEON",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? ES_SOT CHAMELEON",
        "text_html": "Fuera corbatas un minuto: en trinchera técnica lo que vale es <span class=\"slang-token\" data-term=\"tener buena muñeca\">tener buena muñeca</span> para que producción fluya limpia.",
        "phonetics": "",
        "english_gloss": "Ties off for a minute: in the technical trench what counts is real finesse so production flows cleanly.",
        "delivery_cue": "",
        "idiom_terms": [
            "tener buena muñeca"
        ]
    },
    {
        "uid": "ES_SOT_B2B_COUNT",
        "register_id": "ES_SOT",
        "stage": "COUNTERACT",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? ES_SOT COUNTERACT",
        "text_html": "Tener al equipo senior apagando fuegos manuales es <span class=\"slang-token\" data-term=\"mirar los toros desde la barrera\">mirar los toros desde la barrera</span> mientras la automatización espera.",
        "phonetics": "",
        "english_gloss": "Having the senior team putting out manual fires is watching from behind the barrier while automation sits ready.",
        "delivery_cue": "",
        "idiom_terms": [
            "mirar los toros desde la barrera"
        ]
    },
    {
        "uid": "ES_SOT_B2B_CUR",
        "register_id": "ES_SOT",
        "stage": "CURIOSITY",
        "arena": "b2b",
        "title": "B2B Boardroom → Trench ? ES_SOT CURIOSITY",
        "text_html": "De ingeniero a ingeniero: ¿qué cuello de botella crítico despejamos primero en el piloto de esta semana?",
        "phonetics": "",
        "english_gloss": "Engineer to engineer: what critical bottleneck do we clear first in this week’s pilot?",
        "delivery_cue": "",
        "idiom_terms": []
    }
]

ARENA_8_EDGES = [
    {
        "id": "E_CZ_OVA_SPARK_1",
        "source_uid": "CZ_OVA_SPARK_COMP",
        "target_uid": "CZ_OVA_SPARK_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_SPARK_2",
        "source_uid": "CZ_OVA_SPARK_CHAM",
        "target_uid": "CZ_OVA_SPARK_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_SPARK_3",
        "source_uid": "CZ_OVA_SPARK_COUNT",
        "target_uid": "CZ_OVA_SPARK_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_SPARK_1",
        "source_uid": "AT_VIE_SPARK_COMP",
        "target_uid": "AT_VIE_SPARK_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_SPARK_2",
        "source_uid": "AT_VIE_SPARK_CHAM",
        "target_uid": "AT_VIE_SPARK_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_SPARK_3",
        "source_uid": "AT_VIE_SPARK_COUNT",
        "target_uid": "AT_VIE_SPARK_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_SPARK_1",
        "source_uid": "RU_ALA_SPARK_COMP",
        "target_uid": "RU_ALA_SPARK_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_SPARK_2",
        "source_uid": "RU_ALA_SPARK_CHAM",
        "target_uid": "RU_ALA_SPARK_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_SPARK_3",
        "source_uid": "RU_ALA_SPARK_COUNT",
        "target_uid": "RU_ALA_SPARK_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_SPARK_1",
        "source_uid": "EN_YYC_SPARK_COMP",
        "target_uid": "EN_YYC_SPARK_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_SPARK_2",
        "source_uid": "EN_YYC_SPARK_CHAM",
        "target_uid": "EN_YYC_SPARK_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_SPARK_3",
        "source_uid": "EN_YYC_SPARK_COUNT",
        "target_uid": "EN_YYC_SPARK_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_SPARK_1",
        "source_uid": "ES_SOT_SPARK_COMP",
        "target_uid": "ES_SOT_SPARK_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_SPARK_2",
        "source_uid": "ES_SOT_SPARK_CHAM",
        "target_uid": "ES_SOT_SPARK_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_SPARK_3",
        "source_uid": "ES_SOT_SPARK_COUNT",
        "target_uid": "ES_SOT_SPARK_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_ADVENTURE_1",
        "source_uid": "CZ_OVA_ADVENTURE_COMP",
        "target_uid": "CZ_OVA_ADVENTURE_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_ADVENTURE_2",
        "source_uid": "CZ_OVA_ADVENTURE_CHAM",
        "target_uid": "CZ_OVA_ADVENTURE_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_ADVENTURE_3",
        "source_uid": "CZ_OVA_ADVENTURE_COUNT",
        "target_uid": "CZ_OVA_ADVENTURE_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_ADVENTURE_1",
        "source_uid": "AT_VIE_ADVENTURE_COMP",
        "target_uid": "AT_VIE_ADVENTURE_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_ADVENTURE_2",
        "source_uid": "AT_VIE_ADVENTURE_CHAM",
        "target_uid": "AT_VIE_ADVENTURE_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_ADVENTURE_3",
        "source_uid": "AT_VIE_ADVENTURE_COUNT",
        "target_uid": "AT_VIE_ADVENTURE_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_ADVENTURE_1",
        "source_uid": "RU_ALA_ADVENTURE_COMP",
        "target_uid": "RU_ALA_ADVENTURE_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_ADVENTURE_2",
        "source_uid": "RU_ALA_ADVENTURE_CHAM",
        "target_uid": "RU_ALA_ADVENTURE_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_ADVENTURE_3",
        "source_uid": "RU_ALA_ADVENTURE_COUNT",
        "target_uid": "RU_ALA_ADVENTURE_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_ADVENTURE_1",
        "source_uid": "EN_YYC_ADVENTURE_COMP",
        "target_uid": "EN_YYC_ADVENTURE_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_ADVENTURE_2",
        "source_uid": "EN_YYC_ADVENTURE_CHAM",
        "target_uid": "EN_YYC_ADVENTURE_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_ADVENTURE_3",
        "source_uid": "EN_YYC_ADVENTURE_COUNT",
        "target_uid": "EN_YYC_ADVENTURE_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_ADVENTURE_1",
        "source_uid": "ES_SOT_ADVENTURE_COMP",
        "target_uid": "ES_SOT_ADVENTURE_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_ADVENTURE_2",
        "source_uid": "ES_SOT_ADVENTURE_CHAM",
        "target_uid": "ES_SOT_ADVENTURE_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_ADVENTURE_3",
        "source_uid": "ES_SOT_ADVENTURE_COUNT",
        "target_uid": "ES_SOT_ADVENTURE_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_RUNWAY_1",
        "source_uid": "CZ_OVA_RUNWAY_COMP",
        "target_uid": "CZ_OVA_RUNWAY_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_RUNWAY_2",
        "source_uid": "CZ_OVA_RUNWAY_CHAM",
        "target_uid": "CZ_OVA_RUNWAY_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_RUNWAY_3",
        "source_uid": "CZ_OVA_RUNWAY_COUNT",
        "target_uid": "CZ_OVA_RUNWAY_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_RUNWAY_1",
        "source_uid": "AT_VIE_RUNWAY_COMP",
        "target_uid": "AT_VIE_RUNWAY_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_RUNWAY_2",
        "source_uid": "AT_VIE_RUNWAY_CHAM",
        "target_uid": "AT_VIE_RUNWAY_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_RUNWAY_3",
        "source_uid": "AT_VIE_RUNWAY_COUNT",
        "target_uid": "AT_VIE_RUNWAY_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_RUNWAY_1",
        "source_uid": "RU_ALA_RUNWAY_COMP",
        "target_uid": "RU_ALA_RUNWAY_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_RUNWAY_2",
        "source_uid": "RU_ALA_RUNWAY_CHAM",
        "target_uid": "RU_ALA_RUNWAY_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_RUNWAY_3",
        "source_uid": "RU_ALA_RUNWAY_COUNT",
        "target_uid": "RU_ALA_RUNWAY_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_RUNWAY_1",
        "source_uid": "EN_YYC_RUNWAY_COMP",
        "target_uid": "EN_YYC_RUNWAY_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_RUNWAY_2",
        "source_uid": "EN_YYC_RUNWAY_CHAM",
        "target_uid": "EN_YYC_RUNWAY_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_RUNWAY_3",
        "source_uid": "EN_YYC_RUNWAY_COUNT",
        "target_uid": "EN_YYC_RUNWAY_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_RUNWAY_1",
        "source_uid": "ES_SOT_RUNWAY_COMP",
        "target_uid": "ES_SOT_RUNWAY_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_RUNWAY_2",
        "source_uid": "ES_SOT_RUNWAY_CHAM",
        "target_uid": "ES_SOT_RUNWAY_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_RUNWAY_3",
        "source_uid": "ES_SOT_RUNWAY_COUNT",
        "target_uid": "ES_SOT_RUNWAY_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_HOCHKULTUR_1",
        "source_uid": "CZ_OVA_HOCHKULTUR_COMP",
        "target_uid": "CZ_OVA_HOCHKULTUR_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_HOCHKULTUR_2",
        "source_uid": "CZ_OVA_HOCHKULTUR_CHAM",
        "target_uid": "CZ_OVA_HOCHKULTUR_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_HOCHKULTUR_3",
        "source_uid": "CZ_OVA_HOCHKULTUR_COUNT",
        "target_uid": "CZ_OVA_HOCHKULTUR_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_HOCHKULTUR_1",
        "source_uid": "AT_VIE_HOCHKULTUR_COMP",
        "target_uid": "AT_VIE_HOCHKULTUR_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_HOCHKULTUR_2",
        "source_uid": "AT_VIE_HOCHKULTUR_CHAM",
        "target_uid": "AT_VIE_HOCHKULTUR_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_HOCHKULTUR_3",
        "source_uid": "AT_VIE_HOCHKULTUR_COUNT",
        "target_uid": "AT_VIE_HOCHKULTUR_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_HOCHKULTUR_1",
        "source_uid": "RU_ALA_HOCHKULTUR_COMP",
        "target_uid": "RU_ALA_HOCHKULTUR_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_HOCHKULTUR_2",
        "source_uid": "RU_ALA_HOCHKULTUR_CHAM",
        "target_uid": "RU_ALA_HOCHKULTUR_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_HOCHKULTUR_3",
        "source_uid": "RU_ALA_HOCHKULTUR_COUNT",
        "target_uid": "RU_ALA_HOCHKULTUR_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_HOCHKULTUR_1",
        "source_uid": "EN_YYC_HOCHKULTUR_COMP",
        "target_uid": "EN_YYC_HOCHKULTUR_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_HOCHKULTUR_2",
        "source_uid": "EN_YYC_HOCHKULTUR_CHAM",
        "target_uid": "EN_YYC_HOCHKULTUR_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_HOCHKULTUR_3",
        "source_uid": "EN_YYC_HOCHKULTUR_COUNT",
        "target_uid": "EN_YYC_HOCHKULTUR_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_HOCHKULTUR_1",
        "source_uid": "ES_SOT_HOCHKULTUR_COMP",
        "target_uid": "ES_SOT_HOCHKULTUR_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_HOCHKULTUR_2",
        "source_uid": "ES_SOT_HOCHKULTUR_CHAM",
        "target_uid": "ES_SOT_HOCHKULTUR_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_HOCHKULTUR_3",
        "source_uid": "ES_SOT_HOCHKULTUR_COUNT",
        "target_uid": "ES_SOT_HOCHKULTUR_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_POLO_1",
        "source_uid": "CZ_OVA_POLO_COMP",
        "target_uid": "CZ_OVA_POLO_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_POLO_2",
        "source_uid": "CZ_OVA_POLO_CHAM",
        "target_uid": "CZ_OVA_POLO_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_POLO_3",
        "source_uid": "CZ_OVA_POLO_COUNT",
        "target_uid": "CZ_OVA_POLO_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_POLO_1",
        "source_uid": "AT_VIE_POLO_COMP",
        "target_uid": "AT_VIE_POLO_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_POLO_2",
        "source_uid": "AT_VIE_POLO_CHAM",
        "target_uid": "AT_VIE_POLO_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_POLO_3",
        "source_uid": "AT_VIE_POLO_COUNT",
        "target_uid": "AT_VIE_POLO_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_POLO_1",
        "source_uid": "RU_ALA_POLO_COMP",
        "target_uid": "RU_ALA_POLO_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_POLO_2",
        "source_uid": "RU_ALA_POLO_CHAM",
        "target_uid": "RU_ALA_POLO_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_POLO_3",
        "source_uid": "RU_ALA_POLO_COUNT",
        "target_uid": "RU_ALA_POLO_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_POLO_1",
        "source_uid": "EN_YYC_POLO_COMP",
        "target_uid": "EN_YYC_POLO_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_POLO_2",
        "source_uid": "EN_YYC_POLO_CHAM",
        "target_uid": "EN_YYC_POLO_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_POLO_3",
        "source_uid": "EN_YYC_POLO_COUNT",
        "target_uid": "EN_YYC_POLO_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_POLO_1",
        "source_uid": "ES_SOT_POLO_COMP",
        "target_uid": "ES_SOT_POLO_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_POLO_2",
        "source_uid": "ES_SOT_POLO_CHAM",
        "target_uid": "ES_SOT_POLO_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_POLO_3",
        "source_uid": "ES_SOT_POLO_COUNT",
        "target_uid": "ES_SOT_POLO_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_WIEN_1",
        "source_uid": "CZ_OVA_WIEN_COMP",
        "target_uid": "CZ_OVA_WIEN_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_WIEN_2",
        "source_uid": "CZ_OVA_WIEN_CHAM",
        "target_uid": "CZ_OVA_WIEN_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_WIEN_3",
        "source_uid": "CZ_OVA_WIEN_COUNT",
        "target_uid": "CZ_OVA_WIEN_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_WIEN_1",
        "source_uid": "AT_VIE_WIEN_COMP",
        "target_uid": "AT_VIE_WIEN_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_WIEN_2",
        "source_uid": "AT_VIE_WIEN_CHAM",
        "target_uid": "AT_VIE_WIEN_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_WIEN_3",
        "source_uid": "AT_VIE_WIEN_COUNT",
        "target_uid": "AT_VIE_WIEN_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_WIEN_1",
        "source_uid": "RU_ALA_WIEN_COMP",
        "target_uid": "RU_ALA_WIEN_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_WIEN_2",
        "source_uid": "RU_ALA_WIEN_CHAM",
        "target_uid": "RU_ALA_WIEN_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_WIEN_3",
        "source_uid": "RU_ALA_WIEN_COUNT",
        "target_uid": "RU_ALA_WIEN_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_WIEN_1",
        "source_uid": "EN_YYC_WIEN_COMP",
        "target_uid": "EN_YYC_WIEN_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_WIEN_2",
        "source_uid": "EN_YYC_WIEN_CHAM",
        "target_uid": "EN_YYC_WIEN_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_WIEN_3",
        "source_uid": "EN_YYC_WIEN_COUNT",
        "target_uid": "EN_YYC_WIEN_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_WIEN_1",
        "source_uid": "ES_SOT_WIEN_COMP",
        "target_uid": "ES_SOT_WIEN_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_WIEN_2",
        "source_uid": "ES_SOT_WIEN_CHAM",
        "target_uid": "ES_SOT_WIEN_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_WIEN_3",
        "source_uid": "ES_SOT_WIEN_COUNT",
        "target_uid": "ES_SOT_WIEN_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_B2B_1",
        "source_uid": "CZ_OVA_B2B_COMP",
        "target_uid": "CZ_OVA_B2B_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_B2B_2",
        "source_uid": "CZ_OVA_B2B_CHAM",
        "target_uid": "CZ_OVA_B2B_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_CZ_OVA_B2B_3",
        "source_uid": "CZ_OVA_B2B_COUNT",
        "target_uid": "CZ_OVA_B2B_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_B2B_1",
        "source_uid": "AT_VIE_B2B_COMP",
        "target_uid": "AT_VIE_B2B_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_B2B_2",
        "source_uid": "AT_VIE_B2B_CHAM",
        "target_uid": "AT_VIE_B2B_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_AT_VIE_B2B_3",
        "source_uid": "AT_VIE_B2B_COUNT",
        "target_uid": "AT_VIE_B2B_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_B2B_1",
        "source_uid": "RU_ALA_B2B_COMP",
        "target_uid": "RU_ALA_B2B_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_B2B_2",
        "source_uid": "RU_ALA_B2B_CHAM",
        "target_uid": "RU_ALA_B2B_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_RU_ALA_B2B_3",
        "source_uid": "RU_ALA_B2B_COUNT",
        "target_uid": "RU_ALA_B2B_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_B2B_1",
        "source_uid": "EN_YYC_B2B_COMP",
        "target_uid": "EN_YYC_B2B_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_B2B_2",
        "source_uid": "EN_YYC_B2B_CHAM",
        "target_uid": "EN_YYC_B2B_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_EN_YYC_B2B_3",
        "source_uid": "EN_YYC_B2B_COUNT",
        "target_uid": "EN_YYC_B2B_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_B2B_1",
        "source_uid": "ES_SOT_B2B_COMP",
        "target_uid": "ES_SOT_B2B_CHAM",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_B2B_2",
        "source_uid": "ES_SOT_B2B_CHAM",
        "target_uid": "ES_SOT_B2B_COUNT",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    },
    {
        "id": "E_ES_SOT_B2B_3",
        "source_uid": "ES_SOT_B2B_COUNT",
        "target_uid": "ES_SOT_B2B_CUR",
        "edge_type": "FLOWS_TO",
        "weight": 0.84,
        "days_ago": 1,
        "drills": 3,
        "stability": 9
    }
]
