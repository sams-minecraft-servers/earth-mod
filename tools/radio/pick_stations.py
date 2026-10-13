#!/usr/bin/env python3
"""Picks the radio stations for the country radio: for every country, the three most voted-for
working stations in the public directory radio-browser.info (a first choice and two alternates,
each from a different broadcaster). Where the country's national broadcaster is known (PREFERRED) and
the directory has it, that is the first choice instead.

    tools/radio/pick_stations.py            writes radio/stations.json and radio/stations.csv

Nothing here may be broadcast on the server until its station has given permission; the csv is
the list the owner works through, and `permission` in stations.json is set by hand as answers
come in (the pack builder only publishes stations marked "yes").
A station already in stations.json keeps its place and its permission when this is run again.
"""
import csv, json, os, re, subprocess, sys, time, urllib.parse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'radio')
MIRRORS = ['de2', 'de1', 'all']
CODECS = {'MP3', 'AAC', 'AAC+', 'OGG'}

def ask(path):
    # The directory drops about half of all connections and sometimes hangs; asking again works.
    for attempt in range(60):
        host = MIRRORS[attempt % len(MIRRORS)]
        reply = subprocess.run(['curl', '-s', '--max-time', '20', '-A', 'earth.tj-radio/0.1', 'https://%s.api.radio-browser.info/json/%s' % (host, path)], capture_output=True)
        if reply.returncode == 0 and reply.stdout[:1] in (b'[', b'{'):
            try: return json.loads(reply.stdout)
            except ValueError: pass
        time.sleep(min(0.5 + attempt * 0.5, 8))
    raise RuntimeError('the directory did not answer: ' + path)

# Where I know a country's national or public broadcaster, it is preferred as the first choice over
# whatever has the most votes (which is often an internet-only music channel). Names are looked for
# in this order, as whole words in the station's name.
PREFERRED = {
    'US': ['NPR', 'WNYC', 'KEXP', 'KCRW'], 'CA': ['CBC Radio One', 'CBC Music', 'ICI Première'], 'MX': ['Radio Educación', 'IMER', 'Los 40'],
    'GB': ['BBC Radio 4', 'BBC Radio 2', 'BBC World Service'], 'IE': ['RTÉ Radio 1', 'RTE Radio 1', 'RTÉ'], 'FR': ['France Inter', 'FIP', 'France Info'],
    'DE': ['Deutschlandfunk', 'WDR 2', '1LIVE'], 'ES': ['RNE', 'Radio Nacional', 'Cadena SER'], 'PT': ['Antena 1', 'RDP'], 'IT': ['Rai Radio 1', 'Rai Radio 2'],
    'NL': ['NPO Radio 1', 'NPO Radio 2'], 'BE': ['VRT Radio 1', 'La Première', 'Studio Brussel'], 'LU': ['RTL Radio Lëtzebuerg', '100,7'],
    'CH': ['SRF 1', 'La Première', 'SRF 3'], 'AT': ['Ö1', 'OE1', 'FM4', 'Ö3'], 'DK': ['DR P1', 'DR P3'], 'SE': ['Sveriges Radio P1', 'SR P1', 'P3'],
    'NO': ['NRK P1', 'NRK'], 'FI': ['Yle Radio 1', 'Yle Radio Suomi', 'YLE'], 'IS': ['Rás 1', 'Rás 2', 'RÚV'], 'PL': ['Polskie Radio', 'Jedynka', 'Trójka'],
    'CZ': ['Radiožurnál', 'ČRo', 'Český rozhlas'], 'SK': ['Rádio Slovensko', 'RTVS'], 'HU': ['Kossuth', 'Petőfi'], 'RO': ['Radio România Actualități', 'Radio Romania'],
    'BG': ['Хоризонт', 'Horizont', 'BNR'], 'GR': ['Πρώτο', 'ERT', 'ERA'], 'TR': ['TRT Radyo 1', 'TRT'], 'RU': ['Радио России', 'Маяк', 'Mayak'],
    'UA': ['Українське радіо', 'Ukrainian Radio', 'UR1'], 'LT': ['LRT Radijas', 'LRT'], 'LV': ['Latvijas Radio 1', 'LR1'], 'EE': ['Vikerraadio', 'Raadio 2'],
    'HR': ['HRT', 'HR 1'], 'RS': ['Radio Beograd', 'RTS'], 'SI': ['Radio Slovenija', 'Prvi', 'Val 202'], 'BA': ['BH Radio 1'], 'AL': ['Radio Tirana'],
    'ME': ['Radio Crne Gore'], 'MD': ['Radio Moldova'], 'AM': ['Public Radio of Armenia'], 'KZ': ['Qazaq Radiosy', 'Kazakh Radio'], 'IL': ['Reshet Bet', 'Kan', 'Galgalatz'],
    'IN': ['All India Radio', 'Vividh Bharati', 'AIR'], 'PK': ['Radio Pakistan', 'FM 101'], 'BD': ['Bangladesh Betar'], 'LK': ['SLBC'], 'NP': ['Radio Nepal'],
    'CN': ['中国之声', 'CNR', 'CRI'], 'JP': ['NHK', 'J-WAVE'], 'KR': ['KBS', 'MBC'], 'TW': ['ICRT', '中廣'], 'HK': ['RTHK'], 'SG': ['CNA938', 'Gold 905', 'Class 95'],
    'MY': ['RTM', 'Hitz'], 'VN': ['VOV'], 'ID': ['RRI', 'Prambors'], 'PH': ['DZMM', 'DZBB'], 'AU': ['ABC Radio National', 'triple j', 'ABC NewsRadio'],
    'NZ': ['RNZ National', 'RNZ'], 'ZA': ['SAfm', '5FM', 'Metro FM'], 'NG': ['Radio Nigeria', 'FRCN', 'Wazobia', 'Cool FM'], 'KE': ['KBC', 'Capital FM'],
    'GH': ['GBC', 'Joy FM'], 'ET': ['Fana'], 'TZ': ['TBC', 'Clouds FM'], 'SN': ['RFM', 'RTS'], 'CI': ["Radio Côte d'Ivoire", 'RTI'], 'MA': ['SNRT', 'Medi 1', 'Hit Radio'],
    'DZ': ['Chaîne 3', 'Chaine 3'], 'TN': ['Mosaïque', 'Mosaique', 'RTCI'], 'BR': ['Rádio Nacional', 'CBN', 'Jovem Pan'], 'AR': ['Radio Nacional', 'Radio Mitre', 'La 100'],
    'CL': ['Cooperativa', 'Bío-Bío', 'Bio Bio', 'ADN'], 'CO': ['Radio Nacional de Colombia', 'Caracol Radio'], 'PE': ['RPP', 'Radio Nacional'],
    'CU': ['Radio Rebelde', 'Radio Reloj'], 'JM': ['RJR', 'Irie FM'], 'VA': ['Radio Vaticana'], 'CY': ['CyBC', 'RIK'], 'MT': ['Radju Malta'],
}

def qualifies(s):
    return s.get('lastcheckok') == 1 and s.get('codec', '').upper() in CODECS and s.get('homepage', '').strip().startswith('http')

def pick(s, why):
    return {'name': ' '.join(s['name'].split()), 'homepage': s['homepage'].strip(), 'stream': (s.get('url_resolved') or s['url']).strip(),
            'codec': s['codec'], 'bitrate': s.get('bitrate', 0), 'language': s.get('language', ''), 'tags': s.get('tags', ''),
            'votes': s.get('votes', 0), 'id': s['stationuuid'], 'chosen': why, 'permission': 'not asked'}

def preferred(code):
    """The country's national broadcaster as the directory has it, or None."""
    for wanted in PREFERRED.get(code, []):
        found = ask('stations/search?' + urllib.parse.urlencode({'countrycode': code, 'name': wanted, 'order': 'votes', 'reverse': 'true', 'limit': 20, 'hidebroken': 'true'}))
        whole = re.compile(r'(?<!\w)' + re.escape(wanted) + r'(?!\w)', re.IGNORECASE)
        for s in found:
            if qualifies(s) and whole.search(s['name']) and broadcaster(s): return pick(s, 'national broadcaster')
        time.sleep(0.3)
    return None

def broadcaster(station):
    """The site a station belongs to, so that three channels of one broadcaster count as one."""
    host = urllib.parse.urlparse(station['homepage'].strip()).netloc.lower().split(':')[0]
    parts = [p for p in host.split('.') if p != 'www']
    return '.'.join(parts[-3:] if len(parts) > 2 and len(parts[-1]) == 2 and len(parts[-2]) <= 3 else parts[-2:])

def main():
    out = os.path.join(ROOT, 'stations.json')
    kept = {c['code']: c for c in json.load(open(out))} if os.path.exists(out) else {}
    countries = sorted((c for c in ask('countries') if c['stationcount'] > 0 and len(c['iso_3166_1']) == 2), key=lambda c: c['name'])
    result = []
    for n, country in enumerate(countries):
        code = country['iso_3166_1']
        if code in kept: result.append(kept[code]); continue
        found = ask('stations/search?' + urllib.parse.urlencode({'countrycode': code, 'order': 'votes', 'reverse': 'true', 'limit': 60, 'hidebroken': 'true'}))
        picks, seen = [], set()
        for s in found:
            if not qualifies(s): continue
            owner = broadcaster(s)
            if not owner or owner in seen: continue
            seen.add(owner)
            picks.append(pick(s, 'most votes'))
            if len(picks) == 3: break
        result.append({'code': code, 'country': country['name'], 'stations': picks})
        if n % 25 == 24: print('%d of %d countries' % (n + 1, len(countries)), flush=True)
        time.sleep(0.3)
    for country in result:
        stations = country['stations']
        if country['code'] not in PREFERRED or any(s['permission'] != 'not asked' or s.get('chosen') == 'national broadcaster' for s in stations): continue
        first = preferred(country['code'])
        if first:
            country['stations'] = ([first] + [s for s in stations if s['id'] != first['id'] and broadcaster(s) != broadcaster(first)])[:3]
    os.makedirs(ROOT, exist_ok=True)
    with open(out + '.part', 'w') as f: json.dump(result, f, indent=1, ensure_ascii=False)
    os.replace(out + '.part', out)
    with open(os.path.join(ROOT, 'stations.csv'), 'w', newline='') as f:
        rows = csv.writer(f)
        rows.writerow(['Country', 'Code', 'Choice', 'Station', 'Why chosen', 'Website', 'Stream', 'Language', 'Permission'])
        for c in result:
            for i, s in enumerate(c['stations']): rows.writerow([c['country'], c['code'], ['first', 'alternate 1', 'alternate 2'][i], s['name'], s.get('chosen', 'most votes'), s['homepage'], s['stream'], s['language'], s['permission']])
    print('%d countries: %d with a first choice, %d with none that qualify' % (len(result), sum(1 for c in result if c['stations']), sum(1 for c in result if not c['stations'])))

if __name__ == '__main__':
    main()
