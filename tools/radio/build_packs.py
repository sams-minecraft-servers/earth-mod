#!/usr/bin/env python3
"""Records a sample from each country's station and builds one small resource pack per country.

    tools/radio/build_packs.py record [minutes, default 25] [at once, default 16]
    tools/radio/build_packs.py build

record: for every country in radio/stations.json, records its first-choice station (an alternate
if that one gives nothing) into <data>/radio/recordings/<code>/ as five-minute stereo Ogg parts at
48 kbit/s, and notes which station it was in source.json. A country recorded less than a day ago
is skipped, so it can be stopped and started again, or run every few days to refresh.

build: makes <data>/radio/packs/<code>.zip for every recorded country (sounds
earthradio:<code>.<part>), static.zip (the radio static, earthradio:static.<n>) and manifest.json
(each pack's SHA-1, size, parts and their lengths, station, and the permission from stations.json).

Nothing here publishes anything. The packs are other people's broadcasts: a country's pack may only
be put where players can download it once its station's permission in stations.json says "yes".
<data> is EARTH_DATA or /home/ubuntu/earth-data.
"""
import hashlib, json, os, shutil, subprocess, sys, time, zipfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
STATIONS = os.path.join(HERE, '..', '..', 'radio', 'stations.json')
DATA = os.path.join(os.environ.get('EARTH_DATA', '/home/ubuntu/earth-data'), 'radio')
PART_SECONDS = 300
MCMETA = {'pack': {'description': 'earth.tj country radio', 'pack_format': 97, 'min_format': 97, 'max_format': 99}}

def seconds(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path], capture_output=True, text=True, timeout=60).stdout.strip()
    try: return float(out)
    except ValueError: return 0.0

def record_one(country, minutes):
    code = country['code'].lower()
    folder = os.path.join(DATA, 'recordings', code)
    note = os.path.join(folder, 'source.json')
    if os.path.exists(note) and time.time() - os.path.getmtime(note) < 86400: return code, 'recorded less than a day ago'
    for station in country['stations']:
        fresh = folder + '.new'
        shutil.rmtree(fresh, ignore_errors=True)
        os.makedirs(fresh)
        # -rw_timeout gives up on a stream that goes silent; the outer timeout stops one that never ends.
        command = ['ffmpeg', '-nostdin', '-loglevel', 'error', '-rw_timeout', '30000000', '-user_agent', 'earth.tj-radio/0.1',
                   '-t', str(minutes * 60), '-i', station['stream'], '-vn', '-ac', '2', '-ar', '44100', '-c:a', 'libvorbis', '-b:a', '48k',
                   '-f', 'segment', '-segment_time', str(PART_SECONDS), '-reset_timestamps', '1', os.path.join(fresh, '%02d.ogg')]
        try: subprocess.run(command, capture_output=True, timeout=minutes * 60 + 180)
        except subprocess.TimeoutExpired: pass
        parts = sorted(f for f in os.listdir(fresh) if f.endswith('.ogg'))
        lengths = [round(seconds(os.path.join(fresh, f)), 1) for f in parts]
        # A last part of a few seconds is dropped; a recording under two minutes in all is a failure.
        while parts and lengths[-1] < 30: os.remove(os.path.join(fresh, parts.pop())); lengths.pop()
        if sum(lengths) >= 120:
            with open(os.path.join(fresh, 'source.json'), 'w') as f:
                json.dump({'station': station['name'], 'homepage': station['homepage'], 'id': station['id'], 'recorded': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()),
                           'parts': dict(zip(parts, lengths))}, f, indent=1, ensure_ascii=False)
            shutil.rmtree(folder, ignore_errors=True)
            os.replace(fresh, folder)
            return code, '%s, %.0f minutes' % (station['name'], sum(lengths) / 60)
        shutil.rmtree(fresh, ignore_errors=True)
    return code, 'FAILED: no station gave a recording'

def record(minutes, at_once):
    countries = [c for c in json.load(open(STATIONS)) if c['stations']]
    print('%d countries to record, %d minutes each, %d at once' % (len(countries), minutes, at_once), flush=True)
    failed = 0
    with ThreadPoolExecutor(at_once) as pool:
        for n, (code, result) in enumerate(pool.map(lambda c: record_one(c, minutes), countries)):
            failed += result.startswith('FAILED')
            print('%s  %d of %d  %s: %s' % (time.strftime('%Y-%m-%d %H:%M'), n + 1, len(countries), code, result), flush=True)
    print('finished: %d countries recorded, %d failed' % (len(countries) - failed, failed), flush=True)

def zip_pack(path, sounds, files):
    """A pack holding `files` ({path in pack: file on disk}) and a sounds.json; returns its SHA-1 and size."""
    with zipfile.ZipFile(path + '.part', 'w', zipfile.ZIP_STORED) as z:
        z.writestr('pack.mcmeta', json.dumps(MCMETA, indent=1))
        z.writestr('assets/earthradio/sounds.json', json.dumps(sounds, indent=1))
        for name, source in sorted(files.items()): z.write(source, name)
    os.replace(path + '.part', path)
    return hashlib.sha1(open(path, 'rb').read()).hexdigest(), os.path.getsize(path)

def build():
    packs = os.path.join(DATA, 'packs')
    os.makedirs(packs, exist_ok=True)
    permission = {s['id']: s['permission'] for c in json.load(open(STATIONS)) for s in c['stations']}
    names = {c['code'].lower(): c['country'] for c in json.load(open(STATIONS))}
    manifest = {'packs': {}}

    # Radio static: three seconds of band-limited noise with a slow flutter, in a few variants so it does not sound looped.
    work = os.path.join(DATA, 'static')
    os.makedirs(work, exist_ok=True)
    sounds, files = {}, {}
    for n in range(4):
        out = os.path.join(work, '%d.ogg' % n)
        subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'lavfi', '-i', 'anoisesrc=color=pink:duration=3:seed=%d:amplitude=0.6' % (n + 1),
                        '-af', 'highpass=f=500,lowpass=f=5000,tremolo=f=%g:d=0.5,afade=t=in:d=0.15,afade=t=out:st=2.85:d=0.15' % (3 + n * 1.7),
                        '-ac', '2', '-ar', '44100', '-c:a', 'libvorbis', '-b:a', '48k', out], check=True, timeout=120)
        sounds['static.%d' % n] = {'sounds': [{'name': 'earthradio:static/%d' % n}]}
        files['assets/earthradio/sounds/static/%d.ogg' % n] = out
    sha1, size = zip_pack(os.path.join(packs, 'static.zip'), sounds, files)
    manifest['static'] = {'file': 'static.zip', 'sha1': sha1, 'bytes': size, 'sounds': sorted(sounds), 'seconds': 3}

    recordings = os.path.join(DATA, 'recordings')
    for code in sorted(os.listdir(recordings) if os.path.isdir(recordings) else []):
        note = os.path.join(recordings, code, 'source.json')
        if not os.path.exists(note): continue
        source = json.load(open(note))
        sounds, files, parts = {}, {}, []
        for part, length in sorted(source['parts'].items()):
            n = part[:-4]
            sounds['%s.%s' % (code, n)] = {'sounds': [{'name': 'earthradio:%s/%s' % (code, n), 'stream': True}]}
            files['assets/earthradio/sounds/%s/%s.ogg' % (code, n)] = os.path.join(recordings, code, part)
            parts.append({'sound': 'earthradio:%s.%s' % (code, n), 'seconds': length})
        sha1, size = zip_pack(os.path.join(packs, code + '.zip'), sounds, files)
        manifest['packs'][code] = {'country': names.get(code, code.upper()), 'file': code + '.zip', 'sha1': sha1, 'bytes': size, 'station': source['station'],
                                   'homepage': source['homepage'], 'recorded': source['recorded'], 'permission': permission.get(source['id'], 'not asked'), 'parts': parts}
    with open(os.path.join(packs, 'manifest.json.part'), 'w') as f: json.dump(manifest, f, indent=1, ensure_ascii=False)
    os.replace(os.path.join(packs, 'manifest.json.part'), os.path.join(packs, 'manifest.json'))
    total = sum(p['bytes'] for p in manifest['packs'].values())
    print('%d country packs, %.0f MB in all, largest %.1f MB; %d with permission' % (len(manifest['packs']), total / 1e6,
          max([p['bytes'] for p in manifest['packs'].values()] or [0]) / 1e6, sum(1 for p in manifest['packs'].values() if p['permission'] == 'yes')))

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else ''
    if mode == 'record': record(int(sys.argv[2]) if len(sys.argv) > 2 else 25, int(sys.argv[3]) if len(sys.argv) > 3 else 16)
    elif mode == 'build': build()
    else: sys.exit(__doc__)
