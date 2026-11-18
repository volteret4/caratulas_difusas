#!/usr/bin/env python3
"""Resuelve las portadas de tools/albums.txt vía iTunes Search API y genera albums.json."""
import json, sys, time, unicodedata, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "albums.txt"
OUT = ROOT / "albums.json"

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return "".join(c for c in s if c.isalnum())

def lookup(artist, album):
    q = urllib.parse.urlencode({"term": f"{artist} {album}", "entity": "album", "limit": 15, "country": "ES"})
    with urllib.request.urlopen(f"https://itunes.apple.com/search?{q}", timeout=20) as r:
        results = json.load(r)["results"]
    na, nb = norm(artist), norm(album)
    def score(x):
        s = 0
        if norm(x.get("artistName", "")) == na: s += 4
        elif na in norm(x.get("artistName", "")): s += 2
        cn = norm(x.get("collectionName", ""))
        if cn == nb: s += 4
        elif cn.startswith(nb): s += 2
        elif nb in cn: s += 1
        if "deluxe" in cn or "remaster" in cn: s -= 0.5
        return s
    results = [x for x in results if x.get("artworkUrl100")]
    if not results: return None
    best = max(results, key=score)
    if score(best) < 3: return None
    return best["artworkUrl100"].replace("100x100bb", "600x600bb")

def main():
    old = {}
    if OUT.exists():
        old = {(a["artist"], a["album"]): a["cover"] for a in json.loads(OUT.read_text())}
    out = []
    for line in SRC.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        artist, album = [p.strip() for p in line.split("|", 1)]
        cover = old.get((artist, album))
        if not cover:
            for intento in range(4):
                try:
                    cover = lookup(artist, album)
                    break
                except Exception as e:
                    print(f"ERROR {artist} - {album}: {e} (reintento en 60s)", file=sys.stderr)
                    time.sleep(60)
            time.sleep(3)
        if cover:
            out.append({"artist": artist, "album": album, "cover": cover})
            print(f"ok   {artist} - {album}")
        else:
            print(f"FALLO {artist} - {album}", file=sys.stderr)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print(f"\n{len(out)} discos en {OUT.name}")

if __name__ == "__main__":
    main()
