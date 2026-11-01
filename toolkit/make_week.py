"""Render a week of Pearls Collection posts from a JSON spec.

Usage: python3 make_week.py spec.json
spec.json:
{"folder": "2026-11-03",
 "posts": [
   {"name": "review", "type": "review", "quote": "...", "source": "Airbnb guest, October 2026", "photo": "809-living.jpg"},
   {"name": "owner-tip", "type": "tip", "eyebrow": "OWNERS ASK US", "title": "Thinking of a<br>holiday home?",
    "items": [["Question?", "Answer."], ...]},
   {"name": "home-703", "type": "spotlight", "home": "703"}
 ]}
Output: ../posts/<folder>/<name>.jpg (1080x1350, spotlight 1080x1080). Push them, then use
https://raw.githubusercontent.com/pearlscollectioncc-sketch/Pearlmedia/main/posts/<folder>/<name>.jpg in Metricool.
"""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from emblem import emblem, star

CREAM, INK, INK2, GOLD, GOLDD, ESP = '#F4EDE2', '#3A2A1C', '#5A4530', '#A9824A', '#8A6630', '#2A1E14'
CATALOG = {'703': 'pearls-catalog-1-bedroom-703.jpg', '506': 'pearls-catalog-studio-506.jpg', '110': 'pearls-catalog-studio-110.jpg',
           '412': 'pearls-catalog-1-bedroom-412.jpg', '809': 'pearls-catalog-studio-809.jpg'}
_u = [0]


def uid():
    _u[0] += 1
    return f'k{_u[0]}'


def page(body, w=1080, h=1350, bg=CREAM):
    return f'''<!doctype html><html><head><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Cinzel" rel="stylesheet">
<style>html,body{{margin:0;background:{bg}}}*{{box-sizing:border-box}}</style></head><body>
<div style="width:{w}px;height:{h}px;position:relative;overflow:hidden;background:{bg}">{body}</div></body></html>'''


def lockup():
    return f'''<div style="display:flex;align-items:center;gap:18px">{emblem(50, 2.2, uid(), tone='bronze')}
<div style="display:flex;flex-direction:column;align-items:center;gap:9px;color:#5E4320">
<span style="font-family:'Cinzel',serif;font-weight:600;font-size:34px;line-height:1;letter-spacing:.1em;margin-right:-.1em">PEARLS</span>
<span style="display:flex;align-items:center;gap:8px">{star(10, GOLD)}<span style="font-family:'Cinzel',serif;font-weight:500;font-size:13px;line-height:1;letter-spacing:.32em;margin-right:-.32em">COLLECTION</span>{star(10, GOLD)}</span></div></div>'''


def review(p):
    stars5 = ''.join(star(34, '#C9A465') for _ in range(5))
    fs = 70 if len(p['quote']) < 110 else 58
    return page(f'''<div style="position:absolute;left:0;right:0;top:0;height:520px"><img src="photos/{p['photo']}" style="width:100%;height:100%;object-fit:cover;display:block"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:830px;background:{ESP};padding:60px 64px 56px;display:flex;flex-direction:column;gap:28px">
<span style="font-family:'Jost',sans-serif;font-weight:500;font-size:22px;letter-spacing:.3em;color:#C9A465">GUEST REVIEW OF THE WEEK</span>
<div style="display:flex;gap:10px">{stars5}</div>
<div style="font-family:'Cormorant Garamond',serif;font-weight:600;font-size:{fs}px;line-height:1.05;color:#F4EDE2">“{p['quote']}”</div>
<span style="font-family:'Jost',sans-serif;font-size:28px;color:#E2D5C1">{p['source']}</span>
<div style="margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end">
<span style="font-family:'Jost',sans-serif;font-weight:500;font-size:26px;color:#F4EDE2">Airbnb Superhost · 4.9 on Airbnb · 140+ reviews</span>{emblem(50, 2.4, uid())}</div></div>''')


def tip(p):
    qa = ''.join(f'''<div style="padding:30px 0;border-top:2px solid #E2D5C1;display:flex;flex-direction:column;gap:10px">
<span style="font-family:'Cormorant Garamond',serif;font-weight:700;font-size:48px;line-height:1.05;color:{INK}">{q}</span>
<span style="font-family:'Jost',sans-serif;font-size:31px;line-height:1.35;color:{INK2}">{a}</span></div>''' for q, a in p['items'])
    return page(f'''<div style="position:absolute;inset:0;padding:58px 64px 60px;display:flex;flex-direction:column">{lockup()}
<span style="margin-top:46px;font-family:'Jost',sans-serif;font-weight:600;font-size:24px;letter-spacing:.3em;color:{GOLDD}">{p.get('eyebrow', 'OWNERS ASK US')}</span>
<div style="margin-top:14px;font-family:'Cormorant Garamond',serif;font-weight:700;font-size:96px;line-height:.98;color:{INK}">{p['title']}</div>
<div style="margin-top:34px">{qa}</div>
<span style="margin-top:auto;align-self:flex-start;display:inline-flex;background:{INK};color:#fff;border-radius:999px;padding:24px 42px;font-family:'Jost',sans-serif;font-weight:600;font-size:34px">Free plan: WhatsApp +971 58 611 8979</span></div>''')


_PW_CHECK = "const fs=require('fs');process.exit(fs.existsSync(require('playwright').chromium.executablePath())?0:1)"


def playwright_env(rd):
    """Return an env in which bshot.js finds a Playwright whose browser is actually installed.
    Prefers the machine's preinstalled Playwright (global npm root); a local copy in render/node_modules
    shadows it and usually expects a different browser build, so it is removed when it doesn't work.
    Only if no working Playwright exists is a local one installed together with its browser."""
    env = dict(os.environ)
    try:
        groot = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
        if groot:
            env['NODE_PATH'] = groot + (os.pathsep + env['NODE_PATH'] if env.get('NODE_PATH') else '')
    except OSError:
        pass
    ok = lambda: subprocess.run(['node', '-e', _PW_CHECK], cwd=rd, env=env, capture_output=True).returncode == 0
    if ok():
        return env
    local = [os.path.join(rd, 'node_modules', n) for n in ('playwright', 'playwright-core')]
    if any(os.path.isdir(p) for p in local):
        for p in local:
            shutil.rmtree(p, ignore_errors=True)
        if ok():
            return env
    subprocess.run(['npm', 'install', '--silent', '--no-save', 'playwright'], cwd=rd, check=True)
    subprocess.run(['npx', 'playwright', 'install', 'chromium'], cwd=rd, env=env, check=True)
    return env


def main(spec_path):
    spec = json.load(open(spec_path))
    src = os.path.join(HERE, 'build'); os.makedirs(src, exist_ok=True)
    if not os.path.exists(os.path.join(src, 'photos')):
        os.symlink(os.path.join(HERE, 'photos'), os.path.join(src, 'photos'))
    out = os.path.join(os.path.dirname(HERE), 'posts', spec['folder']); os.makedirs(out, exist_ok=True)
    sizes = {}
    for p in spec['posts']:
        if p['type'] == 'spotlight':
            shutil.copy(os.path.join(HERE, 'catalog', CATALOG[p['home']]), os.path.join(out, p['name'] + '.jpg')); continue
        html = review(p) if p['type'] == 'review' else tip(p)
        open(os.path.join(src, p['name'] + '.html'), 'w').write(html); sizes[p['name']] = [1080, 1350, False, 1]
    json.dump(sizes, open(os.path.join(src, 'sizes.json'), 'w'))
    rd = os.path.join(HERE, 'render')
    if not os.path.isdir(os.path.join(rd, 'node_modules', '@fontsource')):
        subprocess.run(['npm', 'install', '--silent'], cwd=rd, check=True)
    if sizes:
        env = playwright_env(rd)
        subprocess.run(['node', os.path.join(rd, 'bshot.js'), src, out], check=True, env=env)
        from PIL import Image
        for n in sizes:
            Image.open(os.path.join(out, n + '.png')).convert('RGB').save(os.path.join(out, n + '.jpg'), quality=92)
            os.remove(os.path.join(out, n + '.png'))
    print('rendered into', out, os.listdir(out))


if __name__ == '__main__':
    main(sys.argv[1])
