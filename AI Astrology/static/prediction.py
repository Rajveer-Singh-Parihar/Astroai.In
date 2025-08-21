from datetime import datetime
from dateutil.relativedelta import relativedelta
import json, os

# Point to ../data relative to this file
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def _load_json(name: str):
    with open(os.path.join(DATA_DIR, name), "r", encoding="utf-8") as f:
        return json.load(f)

# Filenames in the repo use these spellings
ZODIAC_TRAITS = _load_json("zodics_traits.json")
NUMEROLOGY = _load_json("numerlogy.json")

ZODIAC_TABLE = [
    ((1,20),(2,18),"Aquarius"),
    ((2,19),(3,20),"Pisces"),
    ((3,21),(4,19),"Aries"),
    ((4,20),(5,20),"Taurus"),
    ((5,21),(6,20),"Gemini"),
    ((6,21),(7,22),"Cancer"),
    ((7,23),(8,22),"Leo"),
    ((8,23),(9,22),"Virgo"),
    ((9,23),(10,22),"Libra"),
    ((10,23),(11,21),"Scorpio"),
    ((11,22),(12,21),"Sagittarius"),
    ((12,22),(1,19),"Capricorn")
]

def zodiac_sign(day: int, month: int) -> str:
    for start, end, sign in ZODIAC_TABLE:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign
    return "Capricorn"

def reduce_to_digit(n: int) -> int:
    while n > 9 and n not in (11,22,33):
        n = sum(int(d) for d in str(n))
    return n

def life_path(dob: str) -> int:
    digits = [int(c) for c in dob if c.isdigit()]
    return reduce_to_digit(sum(digits))

def destiny_number(name: str) -> int:
    mapping = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,
               'j':1,'k':2,'l':3,'m':4,'n':5,'o':6,'p':7,'q':8,'r':9,
               's':1,'t':2,'u':3,'v':4,'w':5,'x':6,'y':7,'z':8}
    total = sum(mapping.get(ch,0) for ch in name.lower() if ch.isalpha())
    return reduce_to_digit(total)

def lucky_number(lp: int, dn: int, weekday: str) -> int:
    weekday_map = {"Monday":2,"Tuesday":9,"Wednesday":5,"Thursday":3,"Friday":6,"Saturday":8,"Sunday":1}
    raw = lp + dn + weekday_map.get(weekday,7)
    return reduce_to_digit(raw)

def build_profile(name: str, dob_str: str) -> dict:
    # Try multiple date formats
    date_formats = [
        "%Y-%m-%d",      # 1990-05-15
        "%d-%m-%Y",      # 15-05-1990
        "%d/%m/%Y",      # 15/05/1990
        "%m/%d/%Y",      # 05/15/1990
        "%d-%m-%y",      # 15-05-90
        "%d/%m/%y",      # 15/05/90
        "%Y/%m/%d",      # 1990/05/15
    ]
    
    dt = None
    for fmt in date_formats:
        try:
            dt = datetime.strptime(dob_str.strip(), fmt)
            break
        except ValueError:
            continue
    
    if dt is None:
        # If all formats fail, try to parse common patterns
        try:
            # Remove any extra spaces and common separators
            clean_date = dob_str.strip().replace(' ', '').replace('.', '-').replace(',', '-')
            # Try to extract day, month, year
            parts = clean_date.replace('-', '/').split('/')
            if len(parts) == 3:
                day, month, year = parts
                # Handle 2-digit years
                if len(year) == 2:
                    year = '20' + year if int(year) < 50 else '19' + year
                dt = datetime(int(year), int(month), int(day))
        except:
            # Last resort: assume YYYY-MM-DD and try to fix common mistakes
            try:
                # If user entered DD-MM-YYYY, convert to YYYY-MM-DD
                parts = dob_str.strip().split('-')
                if len(parts) == 3 and len(parts[0]) == 2 and len(parts[2]) == 4:
                    day, month, year = parts
                    dt = datetime(int(year), int(month), int(day))
            except:
                raise ValueError(f"Could not parse date: {dob_str}. Please use format: DD-MM-YYYY or YYYY-MM-DD")
    
    # Check if date parsing was successful
    if dt is None:
        raise ValueError(f"Could not parse date: {dob_str}. Please use format: DD-MM-YYYY or YYYY-MM-DD")
    
    z = zodiac_sign(dt.day, dt.month)
    # Use the parsed date for life path calculation
    dob_for_life_path = dt.strftime("%Y-%m-%d")
    lp = life_path(dob_for_life_path)
    dn = destiny_number(name)
    traits = ZODIAC_TRAITS.get(z,{})
    lpd = NUMEROLOGY.get(str(lp),"")
    dnd = NUMEROLOGY.get(str(dn),"")

    # Extra insights
    py = _personal_year(dt)
    future = _future_prediction(py, z)
    remedies = _remedies(z, lp, dt.strftime("%A"))
    marriage = _marriage_life_outlook(z, dn)

    profile = {
        "name": name,
        "dob": dob_str,
        "age": relativedelta(datetime.today(), dt).years,
        "weekday": dt.strftime("%A"),
        "zodiac": z,
        "life_path": lp,
        "life_path_desc": lpd,
        "destiny": dn,
        "destiny_desc": dnd,
        "traits": traits,
        "lucky_number": lucky_number(lp,dn,dt.strftime("%A")),
        "personal_year": py,
        "future_prediction": future,
        "remedies": remedies,
        "marriage_life": marriage
    }
    return profile


# ---------- Additional insights ----------

def _reduce_to_single_digit(n: int) -> int:
    # Reduce to 1-9 ignoring master numbers (used for personal year cycles)
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def _personal_year(dt: datetime) -> int:
    # Numerology personal year for current calendar year
    total = sum(int(c) for c in f"{dt.month:02d}{dt.day:02d}{datetime.today().year}")
    return _reduce_to_single_digit(total)

def _zodiac_element(sign: str) -> str:
    fire = {"Aries","Leo","Sagittarius"}
    earth = {"Taurus","Virgo","Capricorn"}
    air = {"Gemini","Libra","Aquarius"}
    water = {"Cancer","Scorpio","Pisces"}
    if sign in fire: return "Fire"
    if sign in earth: return "Earth"
    if sign in air: return "Air"
    if sign in water: return "Water"
    return ""

def _future_prediction(personal_year: int, zodiac: str) -> str:
    year_themes = {
        1: "a year of new beginnings, fresh energy, and decisive action",
        2: "a year of patience, cooperation, and relationship building",
        3: "a year of creativity, self‑expression, and social visibility",
        4: "a year of hard work, systems, and laying reliable foundations",
        5: "a year of change, travel, and surprising opportunities",
        6: "a year of family focus, responsibility, and healing",
        7: "a year of learning, reflection, and inner growth",
        8: "a year of ambition, career momentum, and financial discipline",
        9: "a year of completion, release, and compassionate service",
    }
    element = _zodiac_element(zodiac)
    element_flavor = {
        "Fire": "Lean into bold moves and leadership.",
        "Earth": "Stay steady; practical steps will compound.",
        "Air": "Network widely and communicate your ideas.",
        "Water": "Trust intuition and protect your emotional bandwidth.",
        "": "Trust your balanced instincts.",
    }[element]
    core = year_themes.get(personal_year, "a meaningful, balanced cycle")
    return f"Expect {core}. {element_flavor} Focus on one clear priority each quarter to harness this cycle."

def _remedies(zodiac: str, life_path_num: int, weekday: str) -> str:
    element = _zodiac_element(zodiac)
    colors = {
        "Fire": "red/orange",
        "Earth": "green/brown",
        "Air": "sky blue/white",
        "Water": "sea blue/silver",
        "": "soft neutrals",
    }[element]
    lp_tip = {
        1: "start at dawn and set a single bold intention",
        2: "practice breathwork to balance emotions",
        3: "write three affirmations out loud",
        4: "organize your space for 15 minutes",
        5: "take a brisk walk and welcome change",
        6: "call a loved one and offer support",
        7: "meditate in silence for seven minutes",
        8: "review finances and set weekly targets",
        9: "donate or help someone without recognition",
    }.get(life_path_num, "take one small mindful action")
    weekday_flow = {
        "Monday": "nurture and reset",
        "Tuesday": "act courageously",
        "Wednesday": "learn and connect",
        "Thursday": "plan growth moves",
        "Friday": "heal relationships",
        "Saturday": "tidy and structure",
        "Sunday": "reflect and recharge",
    }.get(weekday, "stay balanced")
    return (
        f"Wear or visualize {colors} for alignment. Today, {weekday_flow}; "
        f"to harmonize your path {lp_tip}. A short gratitude note before sleep will amplify results."
    )

def _marriage_life_outlook(zodiac: str, destiny_num: int) -> str:
    pair_style = {
        "Aries": "dynamic partnership that thrives on shared adventures",
        "Taurus": "steady, affectionate bond built on reliability",
        "Gemini": "playful, chatty connection that needs variety",
        "Cancer": "deeply caring home life with strong emotional roots",
        "Leo": "warm, generous romance that loves celebration",
        "Virgo": "thoughtful, service‑oriented teamwork with routines",
        "Libra": "harmonious, elegant union centered on fairness",
        "Scorpio": "intense, loyal commitment with private depth",
        "Sagittarius": "expansive, freedom‑loving bond with exploration",
        "Capricorn": "devoted, long‑term alliance with shared goals",
        "Aquarius": "open‑minded, future‑focused partnership",
        "Pisces": "gentle, empathetic union with spiritual connection",
    }
    tone = pair_style.get(zodiac, "balanced, supportive partnership")
    dn_hint = {
        1: "Lead with appreciation, not competition.",
        2: "Make space for feelings and gentle check‑ins.",
        3: "Keep dates creative and conversations flowing.",
        4: "Schedule quality time; reliability builds romance.",
        5: "Travel together or try new hobbies to bond.",
        6: "Prioritize home rituals and mutual care.",
        7: "Share inner worlds and protect quiet time.",
        8: "Set shared ambitions and celebrate progress.",
        9: "Practice forgiveness and acts of service.",
        11: "Honor intuition; listen between the lines.",
        22: "Build something lasting together—home or mission.",
        33: "Lead with compassion; avoid self‑sacrifice.",
    }.get(destiny_num, "Communicate openly and keep promises.")
    return f"Marriage outlook: {tone}. {dn_hint}"
