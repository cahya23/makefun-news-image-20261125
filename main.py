# The World Today -- Wednesday, 25 November 2026.
#
# A one-page newspaper front page, painted pixel by pixel with
# Python's standard library only. Nothing is read from disk, there
# is no network and no randomness, so two runs write byte-identical
# PNGs. The picture is a masthead, a Brent-crude chart for the lead
# story, six short stories in two rows, an also-today strip and a
# footer, all drawn with a tiny 5x7 bitmap font defined below.
#
# The day's stories, each checked against Reuters reporting dated
# 25 November 2026:
#   LEAD -- GULF: Yemen's Houthis said they attacked Saudi Arabia's
#     Ras Tanura oil refinery and Riyadh's financial district, and
#     threatened Jeddah and every Red Sea port. Saudi air defences
#     downed four drones. Brent crude opened at 90.97 in Asia.
#   HORMUZ: two oil tankers struck naval mines, exploded and caught
#     fire in the Strait of Hormuz, Iran's Revolutionary Guards said.
#   MARKETS: the AI rally faded -- Nvidia fell 5.9% on Tuesday
#     after Monday's 31.5% jump on Jensen Huang's return as chief.
#     Nikkei down 2.9%, Seoul down 5.3% at worst, SoftBank down 15%.
#   PACIFIC: Australia and the Solomon Islands signed a security
#     pact on Wednesday, making Canberra the defence partner of
#     choice, after the islands' 2022 pact with China.
#   CHINA: China opened a graft inquiry into Politburo member Chen
#     Jining, Shanghai's party chief -- the fourth such probe of
#     the leadership body since 2025.
#   COLOMBIA: security forces stormed a supermarket in Cartagena,
#     ending a siege; all hostages were freed.
#   SPAIN: Catalan separatist Carles Puigdemont said he will
#     return to Spain on 12 December, ending nearly a decade of
#     self-imposed exile.
#   ALSO TODAY: Greeks strike over wages and public services; the
#     US shelved proposals to use business deals with Russia to end
#     the Ukraine war; the Cikande candy-factory fire toll rose to
#     26; Pakistan's first astronaut reached China's space station.

import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (248, 243, 232)
INK = (18, 18, 18)
RED = (176, 32, 32)
NAVY = (36, 54, 92)
GREY = (122, 118, 110)
PALE = (233, 227, 214)
GREEN = (46, 128, 68)

# ------------------------------------------------------------------ font
# Each glyph is seven rows of five cells, written as text: '#' is ink,
# '.' is empty. The table is turned into bit rows once, at import time,
# so drawing a glyph is just testing bits.

FONT = {
    'A': (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    'B': ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    'C': (" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "),
    'D': ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    'E': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    'F': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    'G': (" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"),
    'H': ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    'I': (" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    'J': ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    'K': ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    'L': ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    'M': ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    'N': ("#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"),
    'O': (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    'P': ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    'Q': (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    'R': ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    'S': (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    'T': ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    'U': ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    'V': ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    'W': ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    'X': ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    'Y': ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    'Z': ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    '0': (" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "),
    '1': ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    '2': (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
    '3': ("#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "),
    '4': ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    '5': ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    '6': ("  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "),
    '7': ("#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "),
    '8': (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    '9': (" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "),
    '.': ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
    ',': ("     ", "     ", "     ", "     ", " ##  ", "  #  ", " #   "),
    '-': ("     ", "     ", "     ", " ### ", "     ", "     ", "     "),
    "'": ("  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "),
    '%': ("##  #", "## # ", "   # ", "  #  ", " #   ", " # ##", "#  ##"),
    '/': ("    #", "   # ", "   # ", "  #  ", " #   ", " #   ", "#    "),
    '(': ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
    ')': (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
    '+': ("     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "),
    '&': (" ##  ", "#  # ", "# #  ", " #   ", "# # #", "#  # ", " ## #"),
    '!': ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    '?': (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
    '=': ("     ", "     ", "#####", "     ", "#####", "     ", "     "),
    ':': ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
    ';': ("     ", " ##  ", " ##  ", "     ", " ##  ", "  #  ", " #   "),
    ' ': ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
}

BITS = {ch: tuple(sum((1 << (4 - c)) for c, cell in enumerate(row)
                      if cell == '#') for row in rows)
        for ch, rows in FONT.items()}


def cell_w(scale):
    return 6 * scale


def text_width(text, scale):
    return len(text) * cell_w(scale)


# ---------------------------------------------------------------- canvas
# The sheet is one RGB bytearray, W by H. Every mark on the page goes
# through set/fill/seg, and at the end encode_png turns the bytes into
# a PNG with a hand-built IHDR, a single zlib IDAT and IEND -- no
# ancillary chunks, so no timestamps can make two runs differ.

class Sheet:
    def __init__(self, w, h, colour):
        self.w, self.h = w, h
        self.buf = bytearray(colour * (w * h))

    def set(self, x, y, colour):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i:i + 3] = bytes(colour)

    def fill(self, x, y, w, h, colour):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, colour)

    def hbar(self, x, y, w, colour, thick=1):
        self.fill(x, y, w, thick, colour)

    def vbar(self, x, y, h, colour, thick=1):
        self.fill(x, y, thick, h, colour)

    def seg(self, x0, y0, x1, y1, colour, thick=1):
        # Bresenham line between two points.
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx + dy, x0, y0
        while True:
            self.fill(x, y, thick, thick, colour)
            if (x, y) == (x1, y1):
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def tri(self, a, b, c, colour):
        # Filled triangle, one horizontal scanline at a time.
        pts = (a, b, c)
        top, bottom = min(p[1] for p in pts), max(p[1] for p in pts)
        edges = ((a, b), (b, c), (c, a))
        for y in range(top, bottom + 1):
            xs = []
            for (x0, y0), (x1, y1) in edges:
                if y0 != y1 and min(y0, y1) <= y <= max(y0, y1):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            if len(xs) >= 2:
                for x in range(int(min(xs)), int(max(xs)) + 1):
                    self.set(x, y, colour)


def encode_png(sheet):
    raw = bytearray()
    for y in range(sheet.h):
        raw.append(0)
        raw += sheet.buf[y * sheet.w * 3:(y + 1) * sheet.w * 3]
    blob = zlib.compress(bytes(raw), 9)

    def chunk(kind, payload):
        out = struct.pack(">I", len(payload)) + kind + payload
        return out + struct.pack(">I", zlib.crc32(kind + payload)
                                 & 0xFFFFFFFF)

    head = struct.pack(">IIBBBBB", sheet.w, sheet.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", head)
            + chunk(b"IDAT", blob) + chunk(b"IEND", b""))

# ------------------------------------------------------------- type
# Text is always set in capitals: put_text folds lower case up. A
# glyph cell is 6*scale wide and 7*scale tall; wrapped paragraphs
# step 9*scale per line.

def put_text(sheet, x, y, text, scale, colour):
    cx = x
    for ch in text.upper():
        bits = BITS.get(ch)
        if bits:
            for row, rowbits in enumerate(bits):
                for col in range(5):
                    if rowbits & (1 << (4 - col)):
                        sheet.fill(cx + col * scale, y + row * scale,
                                   scale, scale, colour)
        cx += cell_w(scale)
    return cx


def put_centred(sheet, cx, y, text, scale, colour):
    put_text(sheet, cx - text_width(text, scale) // 2, y, text,
             scale, colour)


def fold_lines(text, width):
    lines, cur = [], ""
    for word in text.split(" "):
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= width:
            cur = cur + " " + word
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def put_para(sheet, x, y, text, scale, colour, width, step=None):
    if step is None:
        step = 9 * scale
    for line in fold_lines(text, width):
        put_text(sheet, x, y, line, scale, colour)
        y += step
    return y


# ------------------------------------------------------------- layout
# Columns are 304 wide with 20 between them, starting at x = 36.
# The lead takes the top: a Brent chart on the left, headline and
# deck on the right. Then two rows of three stories, an also-today
# strip and a footer.

MARGIN = 36
COL_W = 304
COL_X = (36, 360, 684)

LEAD = {
    "kicker": "GULF IN FLAMES",
    "headline": "HOUTHIS HIT SAUDI OIL HEARTLAND",
    "deck": ("Yemen's Houthis say they struck the Ras Tanura "
             "refinery and Riyadh's financial district, and "
             "threaten Jeddah and every Red Sea port. Air "
             "defences downed four drones."),
}

ROWS = [
    [
        {"kicker": "STRAIT OF HORMUZ",
         "headline": "TWO TANKERS HIT MINES IN HORMUZ",
         "body": ("Two tankers struck naval mines, exploded and caught "
                  "fire in the Strait of Hormuz, Iran's Revolutionary "
                  "Guards said.")},
        {"kicker": "MARKETS",
         "headline": "AI RALLY FADES AS NVIDIA SLIDES",
         "body": ("Nvidia fell 5.9% after Monday's 31.5% jump on "
                  "Huang's return. Nikkei down 2.9%, Seoul down 5.3%, "
                  "SoftBank down 15%.")},
        {"kicker": "PACIFIC",
         "headline": "SOLOMONS SIGN AUSTRALIA PACT",
         "body": ("Australia and the Solomon Islands signed a security "
                  "pact on Wednesday, making Canberra the defence "
                  "partner of choice.")},
    ],
    [
        {"kicker": "CHINA",
         "headline": "SHANGHAI CHIEF PROBED IN GRAFT SWEEP",
         "body": ("China opened a graft inquiry into Politburo member "
                  "Chen Jining, the fourth such probe since 2025.")},
        {"kicker": "COLOMBIA",
         "headline": "ALL HOSTAGES FREED IN CARTAGENA",
         "body": ("Security forces stormed a supermarket in Cartagena, "
                  "ending a siege. All hostages were freed.")},
        {"kicker": "SPAIN",
         "headline": "PUIGDEMONT TO RETURN ON 12 DEC",
         "body": ("Carles Puigdemont said he will return to Spain on 12 "
                  "December, ending nearly a decade in exile.")},
    ],
]

ALSO = ("GREEKS STRIKE OVER WAGES - US SHELVES RUSSIA "
        "BUSINESS-DEAL PLAN - CIKANDE FIRE TOLL RISES TO 26 - "
        "PAKISTAN'S FIRST ASTRONAUT REACHES CHINA STATION")


def brent_chart(sheet, x, y, w, h):
    sheet.fill(x, y, w, h, PALE)
    sheet.hbar(x, y, w, NAVY, 2)
    sheet.hbar(x, y + h - 2, w, NAVY, 2)
    sheet.vbar(x, y, h, NAVY, 2)
    sheet.vbar(x + w - 2, y, h, NAVY, 2)
    put_text(sheet, x + 20, y + 18, "BRENT 90.97", 5, RED)
    put_text(sheet, x + 20, y + 62, "OIL ON EDGE", 2, INK)
    put_text(sheet, x + 20, y + 84, "GULF SHIPPING UNDER FIRE", 2, GREY)
    base = y + h - 28
    sheet.hbar(x + 34, y + 132, w - 68, GREY, 1)
    sheet.hbar(x + 34, y + 192, w - 68, GREY, 1)
    sheet.vbar(x + 34, y + 112, h - 140, INK, 2)
    sheet.hbar(x + 34, base, w - 68, INK, 2)
    pts = [(44, 210), (114, 216), (174, 196), (234, 204), (294, 176),
           (354, 150), (414, 118), (469, 74), (489, 52)]
    pts = [(x + px, y + py) for px, py in pts]
    for p0, p1 in zip(pts, pts[1:]):
        sheet.seg(p0[0], p0[1], p1[0], p1[1], RED, 4)
    tip = pts[-1]
    sheet.tri((tip[0] + 16, tip[1] - 12), (tip[0] - 8, tip[1] - 2),
              (tip[0] + 2, tip[1] + 20), RED)
    put_text(sheet, x + 34, base + 8, "MON", 2, GREY)
    put_text(sheet, x + w - 70, base + 8, "WED", 2, GREY)


def put_story(sheet, x, y, story):
    put_text(sheet, x, y, story["kicker"], 2, RED)
    y += 22
    y = put_para(sheet, x, y, story["headline"], 3, INK,
                 COL_W // (6 * 3), step=9 * 3)
    y += 6
    return put_para(sheet, x, y, story["body"], 2, INK,
                    COL_W // (6 * 2), step=9 * 2)


def build_page():
    sheet = Sheet(W, H, PAPER)

    # Masthead and date line.
    put_centred(sheet, W // 2, 28, "THE WORLD TODAY", 10, INK)
    sheet.hbar(MARGIN, 122, 220, INK, 2)
    sheet.hbar(W - MARGIN - 220, 122, 220, INK, 2)
    put_centred(sheet, W // 2, 112, "WEDNESDAY, 25 NOVEMBER 2026",
                3, INK)
    sheet.hbar(MARGIN, 144, W - 2 * MARGIN, INK, 3)
    sheet.hbar(MARGIN, 150, W - 2 * MARGIN, INK, 1)

    # Lead: chart on the left, headline and deck on the right.
    brent_chart(sheet, MARGIN, 166, 520, 312)
    rx = 580
    put_text(sheet, rx, 166, LEAD["kicker"], 2, RED)
    put_para(sheet, rx, 194, LEAD["headline"], 4, INK,
             408 // 24, step=36)
    put_para(sheet, rx, 314, LEAD["deck"], 2, INK,
             408 // 12, step=18)
    sheet.hbar(MARGIN, 494, W - 2 * MARGIN, INK, 2)

    # Two rows of three stories.
    for row_y, rule_y, row in ((510, 724, ROWS[0]),
                               (740, 926, ROWS[1])):
        for cx, story in zip(COL_X, row):
            put_story(sheet, cx, row_y, story)
        sheet.hbar(MARGIN, rule_y, W - 2 * MARGIN, INK, 2)

    # Also-today strip and footer.
    put_text(sheet, MARGIN, 940, "ALSO TODAY", 2, RED)
    put_para(sheet, MARGIN, 962, ALSO, 2, INK,
             (W - 2 * MARGIN) // 12, step=18)
    put_text(sheet, MARGIN, 1006, "SOURCES: REUTERS, 25 NOVEMBER 2026",
             2, GREY)
    right = "DRAWN BY HAND - NO PHOTOS"
    put_text(sheet, W - MARGIN - text_width(right, 2), 1006, right,
             2, GREY)
    return sheet


def main():
    sheet = build_page()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(encode_png(sheet))


if __name__ == "__main__":
    main()
