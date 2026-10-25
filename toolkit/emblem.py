"""Vector recreation of the Pearls Collection gold emblem: onion-dome arch, pearl, two calligraphic waves.

emblem(width, weight, uid, tone) returns an inline <svg>. weight scales the line thickness so the
mark stays crisp at small sizes (nav, favicon) and delicate at large sizes (footer, posters).
"""
import math

VB_W, VB_H = 360, 540


def _cubic(p0, p1, p2, p3, t):
    u = 1 - t
    x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
    y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
    return x, y


def _straight(s):
    (x0, y0), _, _, (x3, y3) = s
    return all(abs((x3 - x0) * (y - y0) - (y3 - y0) * (x - x0)) < 1e-6 for x, y in s[1:3])


def _sample(segs, n=22):
    """segs: list of (p0,p1,p2,p3). Returns points along the chain; straight segments get a few points only."""
    pts = []
    for i, s in enumerate(segs):
        m = 3 if _straight(s) else n
        for k in range(m + 1):
            if i and k == 0:
                continue
            pts.append(_cubic(*s, k / m))
    return pts


def _ribbon(segs, profile, n=22, cap='flat'):
    """Closed filled path around a centre line, half-width given by profile(s) for s in 0..1 (arc-length)."""
    pts = _sample(segs, n)
    # arc length
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.dist(a, b))
    tot = L[-1]
    left, right = [], []
    for i, p in enumerate(pts):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = profile(L[i] / tot)
        left.append((p[0] + nx * w, p[1] + ny * w))
        right.append((p[0] - nx * w, p[1] - ny * w))
    poly = left + right[::-1]
    return 'M' + ' '.join(f'{x:.1f} {y:.1f}' for x, y in poly) + 'Z'


def _mirror(segs):
    return [tuple((VB_W - x, y) for x, y in s) for s in segs]


# Arch centre line, left half, from the bottom of the left leg up to the tip.
ARCH_L = [
    ((10, 536), (10, 420), (10, 330), (10, 232)),
    ((10, 232), (10, 162), (58, 124), (108, 90)),
    ((108, 90), (146, 64), (172, 42), (180, 6)),
]
ARCH_R = _mirror(ARCH_L)

# Upper wave: small rise, trough under the pearl, thin tip on the right.
WAVE_U = [
    ((40, 392), (66, 374), (110, 374), (154, 402)),
    ((154, 402), (198, 430), (268, 420), (334, 368)),
]
# Lower wave: thin tail on the left, crest, trough, thin tip on the right.
WAVE_D = [
    ((24, 474), (46, 450), (74, 434), (108, 435)),
    ((108, 435), (142, 436), (168, 474), (212, 479)),
    ((212, 479), (254, 484), (290, 464), (318, 436)),
]


def _bump(s, a, b, c):
    """0 outside [a,c], rises to 1 at b."""
    if s <= a or s >= c:
        return 0.0
    if s <= b:
        x = (s - a) / (b - a)
    else:
        x = (c - s) / (c - b)
    return 0.5 - 0.5 * math.cos(math.pi * x)


def shapes(weight=1.0):
    w = 3.4 * weight  # base half-width of the arch line
    arch_l = _ribbon(ARCH_L, lambda s: w * (1 - 0.35 * _bump(s, 0.86, 1.0, 1.01)))
    # right side: calligraphic swell through the dome and upper leg
    arch_r = _ribbon(ARCH_R, lambda s: w * (1 + 1.7 * _bump(s, 0.3, 0.72, 0.97)) * (1 - 0.35 * _bump(s, 0.9, 1.0, 1.01)))
    wu = _ribbon(WAVE_U, lambda s: max(0.6, (5.4 + 4.2 * weight) * (_bump(s, -0.12, 0.3, 1.0) ** 0.8)), n=24)
    wd = _ribbon(WAVE_D, lambda s: max(0.6, (5.4 + 4.2 * weight) * (_bump(s, -0.02, 0.36, 1.0) ** 0.8)), n=24)
    return arch_l, arch_r, wu, wd


TONES = {
    # metallic gold for light or dark backgrounds
    'gold': [(0, '#7E5C2C'), (.22, '#C9A465'), (.4, '#EFD9A4'), (.55, '#B48C51'), (.75, '#DDBF84'), (1, '#86622F')],
    # deeper gold for small sizes on light backgrounds (more contrast)
    'bronze': [(0, '#6B4C22'), (.3, '#A98245'), (.5, '#C8A262'), (.7, '#9A7439'), (1, '#6B4C22')],
    # flat single colours
    'ink': [(0, '#3A2A1C'), (1, '#3A2A1C')],
    'white': [(0, '#FFFFFF'), (1, '#FFFFFF')],
}


def emblem(width, weight=1.0, uid='pc', tone='gold', pearl=True, title=None, extra=''):
    h = width * VB_H / VB_W
    arch_l, arch_r, wu, wd = shapes(weight)
    stops = ''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in TONES[tone])
    label = f'role="img" aria-label="{title}"' if title else 'aria-hidden="true"'
    pearl_svg = ''
    if pearl:
        pearl_svg = f'''<circle cx="180" cy="290" r="70" fill="url(#{uid}p)"/>
<circle cx="180" cy="290" r="70" fill="url(#{uid}w)"/>
<circle cx="180" cy="290" r="69" stroke="url(#{uid}g)" stroke-width="{1.6 * weight:.1f}" opacity=".8"/>
<ellipse cx="156" cy="264" rx="21" ry="13.5" fill="#FFFFFF" opacity=".85" transform="rotate(-35 156 264)"/>'''
    return f'''<svg width="{width:g}" height="{h:.0f}" viewBox="0 0 {VB_W} {VB_H}" fill="none" xmlns="http://www.w3.org/2000/svg" {label} {extra}>
<defs>
<linearGradient id="{uid}g" x1="0" y1="0" x2="{VB_W}" y2="{VB_H}" gradientUnits="userSpaceOnUse">{stops}</linearGradient>
<radialGradient id="{uid}p" cx="150" cy="258" r="102" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".38" stop-color="#FAF5EC"/><stop offset=".72" stop-color="#E9DCC6"/><stop offset="1" stop-color="#C7AE84"/></radialGradient>
<radialGradient id="{uid}w" cx="196" cy="350" r="74" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#F0CF8E" stop-opacity=".75"/><stop offset="1" stop-color="#F0CF8E" stop-opacity="0"/></radialGradient>
</defs>
<g fill="url(#{uid}g)"><path d="{arch_l}"/><path d="{arch_r}"/><path d="{wu}"/><path d="{wd}"/></g>
{pearl_svg}
</svg>'''


STAR = 'M12 0C12.8 8 16 11.2 24 12C16 12.8 12.8 16 12 24C11.2 16 8 12.8 0 12C8 11.2 11.2 8 12 0Z'


def star(size, color):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true" style="flex:none;display:block"><path d="{STAR}" fill="{color}"/></svg>'


if __name__ == '__main__':
    print(len(emblem(200)))
