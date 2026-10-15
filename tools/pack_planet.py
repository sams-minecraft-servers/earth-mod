#!/usr/bin/env python3
"""Packs the streets and buildings of every one-degree tile that has any (see pack_urban.py), from the
local copy made by download_overture.py, busiest tiles first, skipping tiles already packed.

    <data>/urban-venv/bin/python tools/pack_planet.py

Each tile is packed by its own pack_urban.py process, one at a time, at the lowest disk and CPU
priority and under the memory limit of the service that runs it (deploy/earth-urban-build.service). Restartable. Progress
goes to stdout; the list of tiles is kept in <data>/urban/tiles.txt.
"""
import os, subprocess, sys, time

DATA = os.environ.get('EARTH_DATA', '/home/ubuntu/earth-data')
SOURCE = os.path.join(DATA, 'overture', 'release', '2026-09-23.1')
HERE = os.path.dirname(os.path.abspath(__file__))
LIST = os.path.join(DATA, 'urban', 'tiles.txt')

def name(lat, lon):
    return '%s%02d%s%03d' % ('N' if lat >= 0 else 'S', abs(lat), 'E' if lon >= 0 else 'W', abs(lon))

def tiles():
    if os.path.exists(LIST): return [l.split()[0] for l in open(LIST) if l.strip()]
    import duckdb
    db = duckdb.connect()
    db.execute("SET memory_limit='1GB'; SET threads=2")
    rows = db.execute("SELECT floor(bbox.ymin)::INT, floor(bbox.xmin)::INT, count(*) n FROM read_parquet('%s/theme=buildings/type=building/*')"
                      " GROUP BY 1, 2 ORDER BY n DESC" % SOURCE).fetchall()
    os.makedirs(os.path.dirname(LIST), exist_ok=True)
    with open(LIST + '.part', 'w') as f:
        for lat, lon, n in rows: f.write('%s %d\n' % (name(lat, lon), n))
    os.replace(LIST + '.part', LIST)
    return [name(lat, lon) for lat, lon, _ in rows]

def main():
    todo = tiles()
    print('%d tiles have buildings' % len(todo), flush=True)
    env = dict(os.environ, URBAN_SOURCE=SOURCE)
    for n, tile in enumerate(todo, 1):
        out = os.path.join(DATA, 'urban', tile[:3], tile + '.urb')
        if os.path.exists(out): continue
        r = subprocess.run(['timeout', '3600', sys.executable, os.path.join(HERE, 'pack_urban.py'), tile], env=env, capture_output=True, text=True)
        line = (r.stdout.strip().splitlines() or [''])[-1]
        print('%s  %d of %d  %s' % (time.strftime('%Y-%m-%d %H:%M'), n, len(todo), line if r.returncode == 0 else 'FAILED %s: %s' % (tile, (r.stderr.strip().splitlines() or ['?'])[-1])), flush=True)
    print('finished: every tile is packed', flush=True)

if __name__ == '__main__':
    main()
