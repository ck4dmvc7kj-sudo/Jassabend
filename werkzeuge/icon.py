"""Erzeugt die App-Icons (schwarz, rotes Z der Jasstafel, weisse Striche) ohne Zusatzpakete."""
import struct, zlib, sys

def zeichne(groesse):
    s = groesse / 512
    px = [[(0, 0, 0)] * groesse for _ in range(groesse)]

    def linie(x0, y0, x1, y1, dicke, farbe):
        x0, y0, x1, y1, r = x0 * s, y0 * s, x1 * s, y1 * s, dicke * s / 2
        dx, dy = x1 - x0, y1 - y0
        laenge2 = dx * dx + dy * dy
        for y in range(max(0, int(min(y0, y1) - r - 1)), min(groesse, int(max(y0, y1) + r + 2))):
            for x in range(max(0, int(min(x0, x1) - r - 1)), min(groesse, int(max(x0, x1) + r + 2))):
                t = max(0, min(1, ((x + .5 - x0) * dx + (y + .5 - y0) * dy) / laenge2))
                ex, ey = x0 + t * dx - x - .5, y0 + t * dy - y - .5
                d = (ex * ex + ey * ey) ** .5
                a = max(0, min(1, r - d + .5))
                if a:
                    alt = px[y][x]
                    px[y][x] = tuple(round(alt[i] * (1 - a) + farbe[i] * a) for i in range(3))

    rot, weiss = (224, 38, 43), (255, 255, 255)
    linie(110, 130, 402, 130, 16, rot)
    linie(402, 130, 110, 382, 16, rot)
    linie(110, 382, 402, 382, 16, rot)
    for i in range(4):
        x = 250 + i * 30
        linie(x, 310, x, 450, 12, weiss)
    linie(232, 340, 362, 420, 12, weiss)
    return px

def png(px, pfad):
    roh = b''.join(b'\x00' + bytes(c for p in zeile for c in p) for zeile in px)
    def block(typ, inhalt):
        return struct.pack('>I', len(inhalt)) + typ + inhalt + struct.pack('>I', zlib.crc32(typ + inhalt))
    h = len(px)
    with open(pfad, 'wb') as f:
        f.write(b'\x89PNG\r\n\x1a\n' + block(b'IHDR', struct.pack('>IIBBBBB', h, h, 8, 2, 0, 0, 0))
                + block(b'IDAT', zlib.compress(roh, 9)) + block(b'IEND', b''))

ziel = sys.argv[1]
for g in (180, 192, 512):
    png(zeichne(g), f'{ziel}/icon-{g}.png')
