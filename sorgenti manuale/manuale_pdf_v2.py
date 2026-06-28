# -*- coding: utf-8 -*-
"""
Elettropollo — Manuale utente PDF v2.2
- Copertina: pagina 1 del PDF originale (immagine illustrata)
- Contenuto: testo aggiornato v2.2
- Screenshot: schermate TFT SVG convertite in PNG inline
"""

import subprocess, re, io
from pypdf import PdfReader, PdfWriter
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import Drawing
from reportlab.platypus.flowables import Flowable

# ── Palette ───────────────────────────────────────────────────────────────────
PLUM    = colors.HexColor('#473550')
PLUM_D  = colors.HexColor('#2b1f33')
TERRA   = colors.HexColor('#C25A33')
SUN     = colors.HexColor('#F2BE7A')
CREAM   = colors.HexColor('#F8EEDC')
CREAM2  = colors.HexColor('#f3e8d4')
INK     = colors.HexColor('#3a2e22')
GREY    = colors.HexColor('#7d6c57')
WHITE   = colors.white

W, H = A4
ML, MR, MT, MB = 2.2*cm, 2.2*cm, 2.5*cm, 2.2*cm

# ── Carica gli SVG delle schermate ───────────────────────────────────────────
_SCRIPT_DIR = __import__('os').path.dirname(__import__('os').path.abspath(__file__))

def load_screens():
    result = subprocess.run(['python3', __import__('os').path.join(_SCRIPT_DIR, 'gen_screens.py')],
                            capture_output=True, text=True)
    screens = {}
    current, buf = None, []
    for line in result.stdout.splitlines():
        m = re.match(r'^=== (\S+) ===$', line)
        if m:
            if current and buf: screens[current] = '\n'.join(buf).strip()
            current, buf = m.group(1), []
        else:
            buf.append(line)
    if current and buf: screens[current] = '\n'.join(buf).strip()
    return screens

SCREENS = load_screens()

# SVG aggiuntivi che non sono nel gen_screens (splash + main screens)
SPLASH_SVG = '''<svg width="240" height="320" viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <rect width="240" height="130" fill="#461E5A"/><rect y="0" width="240" height="11" fill="#461E5A"/><rect y="11" width="240" height="11" fill="#4E2260"/><rect y="22" width="240" height="11" fill="#5A2A68"/><rect y="33" width="240" height="11" fill="#663266"/><rect y="44" width="240" height="11" fill="#763A60"/><rect y="55" width="240" height="11" fill="#864250"/><rect y="66" width="240" height="11" fill="#96503C"/><rect y="77" width="240" height="11" fill="#A65E2A"/><rect y="88" width="240" height="11" fill="#B46818"/><rect y="99" width="240" height="11" fill="#C07010"/><rect y="110" width="240" height="210" fill="#1C1008"/>
  <circle cx="120" cy="65" r="24" fill="#FDC200"/><circle cx="120" cy="65" r="19" fill="#FFEC00"/>
  <rect x="148" y="92" width="62" height="50" fill="#1C1008"/><polygon points="148,92 210,92 179,70" fill="#1C1008"/><rect x="162" y="104" width="12" height="14" fill="#7B3F00"/><rect x="172" y="84" width="10" height="6" fill="#C1692A"/>
  <circle cx="28" cy="112" r="7" fill="#1C1008"/><ellipse cx="30" cy="120" rx="10" ry="7" fill="#1C1008"/><circle cx="62" cy="114" r="6" fill="#1C1008"/><ellipse cx="64" cy="121" rx="9" ry="6" fill="#1C1008"/>
  <text x="120" y="162" text-anchor="middle" font-family="sans-serif" font-weight="bold" font-size="17" fill="#FEB6A0">ELETTROPOLLO</text>
  <text x="120" y="183" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#C1692A">La domotica del pollaio</text>
  <text x="120" y="199" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#6B6050">firmware v2.2</text>
  <line x1="10" y1="218" x2="230" y2="218" stroke="#7B3F00" stroke-width="1"/>
  <text x="10" y="232" font-family="sans-serif" font-size="11" fill="#6B6050">Avvio sistema...</text>
  <rect x="10" y="248" width="18" height="10" rx="3" fill="#C1692A"/><rect x="32" y="248" width="18" height="10" rx="3" fill="#C1692A"/><rect x="54" y="248" width="18" height="10" rx="3" fill="#C1692A"/><rect x="76" y="248" width="18" height="10" rx="3" fill="#C1692A"/><rect x="98" y="248" width="18" height="10" rx="3" fill="#C1692A"/><rect x="120" y="248" width="18" height="10" rx="3" fill="#C1692A"/>
  <rect x="142" y="248" width="18" height="10" rx="3" fill="#3A2210"/><rect x="164" y="248" width="18" height="10" rx="3" fill="#3A2210"/><rect x="186" y="248" width="18" height="10" rx="3" fill="#3A2210"/><rect x="208" y="248" width="18" height="10" rx="3" fill="#3A2210"/>
  <rect x="10" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/><rect x="32" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/><rect x="54" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/><rect x="76" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/><rect x="98" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/><rect x="120" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/><rect x="142" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/><rect x="164" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/><rect x="186" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/><rect x="208" y="248" width="18" height="10" rx="3" fill="none" stroke="#6B4020" stroke-width="1"/>
  <text x="120" y="300" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#4A3020">vergustechnologies</text>
  <text x="120" y="312" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#4A3020">@proton.me</text>
</svg>'''

MAIN_OPEN_SVG = '''<svg width="240" height="320" viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <rect width="240" height="320" fill="#1C1008"/><rect width="240" height="28" fill="#7B3F00"/>
  <text x="10" y="19" font-family="sans-serif" font-weight="bold" font-size="13" fill="#FEB6A0">ELETTROPOLLO</text>
  <circle cx="218" cy="14" r="4" fill="#670C20"/>
  <text x="230" y="19" text-anchor="end" font-family="sans-serif" font-size="11" fill="#C0A080">06:42</text>
  <rect x="10" y="32" width="220" height="68" rx="4" fill="#0C0118" stroke="#364620" stroke-width="1"/>
  <text x="20" y="46" font-family="sans-serif" font-size="10" fill="#E48A50">PORTA</text>
  <text x="218" y="46" text-anchor="end" font-family="sans-serif" font-weight="bold" font-size="11" fill="#C39E80">chiude 20:45</text>
  <text x="20" y="66" font-family="sans-serif" font-weight="bold" font-size="15" fill="#670C20">PORTA APERTA</text>
  <ellipse cx="22" cy="90" rx="6" ry="2" stroke="#C4CB90" stroke-width="1" fill="none"/><circle cx="22" cy="90" r="3" fill="#0C0118"/><circle cx="22" cy="90" r="3" fill="#C4CB90"/>
  <text x="28" y="94" font-family="sans-serif" font-size="10" fill="#C4CB90">Modo astronomico</text>
  <rect x="10" y="104" width="108" height="44" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="18" y="118" font-family="sans-serif" font-size="10" fill="#E48A50">ALBA</text>
  <text x="18" y="138" font-family="sans-serif" font-weight="bold" font-size="15" fill="#FDC200">05:18</text>
  <rect x="122" y="104" width="108" height="44" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="130" y="118" font-family="sans-serif" font-size="10" fill="#E48A50">TRAMONTO</text>
  <text x="130" y="138" font-family="sans-serif" font-weight="bold" font-size="15" fill="#C39E80">20:51</text>
  <rect x="10" y="152" width="108" height="52" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="18" y="166" font-family="sans-serif" font-size="10" fill="#E48A50">TEMP.</text>
  <text x="18" y="187" font-family="sans-serif" font-weight="bold" font-size="15" fill="#659E80">22.4°C</text>
  <rect x="122" y="152" width="108" height="52" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="132" y="166" font-family="sans-serif" font-size="10" fill="#E48A50">BATTERIA</text>
  <text x="132" y="184" font-family="sans-serif" font-weight="bold" font-size="13" fill="#670C20">12.6V</text>
  <rect x="132" y="192" width="88" height="7" rx="2" fill="#6B4020"/><rect x="132" y="192" width="72" height="7" rx="2" fill="#670C20"/>
  <rect x="10" y="208" width="220" height="100" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="18" y="222" font-family="sans-serif" font-size="9" fill="#E48A50">PROSSIME EROGAZIONI</text>
  <text x="18" y="240" font-family="sans-serif" font-size="10" fill="#C4CB90">Cibo</text>
  <text x="18" y="255" font-family="sans-serif" font-weight="bold" font-size="12" fill="#FDC200">07:30</text>
  <text x="91" y="240" font-family="sans-serif" font-size="10" fill="#C4CB90">Acqua</text>
  <text x="91" y="255" font-family="sans-serif" font-weight="bold" font-size="12" fill="#659E80">08:00</text>
  <text x="164" y="240" font-family="sans-serif" font-size="10" fill="#C4CB90">Pulizia</text>
  <text x="164" y="255" font-family="sans-serif" font-weight="bold" font-size="12" fill="#DDDCC0">--:--</text>
  <line x1="16" y1="265" x2="224" y2="265" stroke="#6B4020" stroke-width="1"/>
  <text x="18" y="280" font-family="sans-serif" font-size="10" fill="#E48A50">AUX</text>
  <text x="48" y="280" font-family="sans-serif" font-weight="bold" font-size="11" fill="#670C20">ON</text>
  <text x="18" y="295" font-family="sans-serif" font-size="10" fill="#C4CB90">poi OFF 22:00</text>
</svg>'''

MAIN_CLOSED_SVG = '''<svg width="240" height="320" viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg">
  <rect width="240" height="320" fill="#1C1008"/><rect width="240" height="28" fill="#7B3F00"/>
  <text x="10" y="19" font-family="sans-serif" font-weight="bold" font-size="13" fill="#FEB6A0">ELETTROPOLLO</text>
  <circle cx="218" cy="14" r="4" fill="#5F5E5A"/>
  <text x="230" y="19" text-anchor="end" font-family="sans-serif" font-size="11" fill="#C0A080">22:15</text>
  <rect x="10" y="32" width="220" height="68" rx="4" fill="#180000" stroke="#B20420" stroke-width="1"/>
  <text x="20" y="46" font-family="sans-serif" font-size="10" fill="#E48A50">PORTA</text>
  <text x="218" y="46" text-anchor="end" font-family="sans-serif" font-weight="bold" font-size="11" fill="#C39E80">apre 05:18</text>
  <text x="20" y="66" font-family="sans-serif" font-weight="bold" font-size="15" fill="#FB8820">PORTA CHIUSA</text>
  <circle cx="19" cy="90" r="2" fill="#C4CB90"/><rect x="17" y="86" width="4" height="6" fill="#C4CB90"/><line x1="15" y1="84" x2="23" y2="84" stroke="#C4CB90" stroke-width="1"/>
  <text x="28" y="94" font-family="sans-serif" font-size="10" fill="#C4CB90">Orari manuali</text>
  <rect x="10" y="104" width="108" height="44" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="18" y="118" font-family="sans-serif" font-size="10" fill="#E48A50">ALBA</text>
  <text x="18" y="138" font-family="sans-serif" font-weight="bold" font-size="15" fill="#FDC200">06:30</text>
  <rect x="122" y="104" width="108" height="44" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="130" y="118" font-family="sans-serif" font-size="10" fill="#E48A50">TRAMONTO</text>
  <text x="130" y="138" font-family="sans-serif" font-weight="bold" font-size="15" fill="#C39E80">20:10</text>
  <rect x="10" y="152" width="108" height="52" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="18" y="166" font-family="sans-serif" font-size="10" fill="#E48A50">TEMP.</text>
  <text x="18" y="187" font-family="sans-serif" font-weight="bold" font-size="15" fill="#659E80">8.1°C</text>
  <rect x="122" y="152" width="108" height="52" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="132" y="166" font-family="sans-serif" font-size="10" fill="#E48A50">BATTERIA</text>
  <text x="132" y="184" font-family="sans-serif" font-weight="bold" font-size="13" fill="#FB8820">11.1V</text>
  <rect x="132" y="192" width="88" height="7" rx="2" fill="#6B4020"/><rect x="132" y="192" width="22" height="7" rx="2" fill="#FB8820"/>
  <rect x="10" y="208" width="220" height="100" rx="4" fill="#3A2210" stroke="#6B4020" stroke-width="1"/>
  <text x="18" y="222" font-family="sans-serif" font-size="9" fill="#E48A50">PROSSIME EROGAZIONI</text>
  <text x="18" y="240" font-family="sans-serif" font-size="10" fill="#C4CB90">Cibo</text>
  <text x="18" y="255" font-family="sans-serif" font-weight="bold" font-size="12" fill="#FDC200">07:30</text>
  <text x="91" y="240" font-family="sans-serif" font-size="10" fill="#C4CB90">Acqua</text>
  <text x="91" y="255" font-family="sans-serif" font-weight="bold" font-size="12" fill="#659E80">07:45</text>
  <text x="164" y="240" font-family="sans-serif" font-size="10" fill="#C4CB90">Pulizia</text>
  <text x="164" y="255" font-family="sans-serif" font-weight="bold" font-size="12" fill="#DDDCC0">09:00</text>
  <line x1="16" y1="265" x2="224" y2="265" stroke="#6B4020" stroke-width="1"/>
  <text x="18" y="280" font-family="sans-serif" font-size="10" fill="#E48A50">AUX</text>
  <text x="48" y="280" font-family="sans-serif" font-weight="bold" font-size="11" fill="#FB8820">OFF</text>
  <text x="18" y="295" font-family="sans-serif" font-size="10" fill="#C4CB90">poi ON 08:30</text>
</svg>'''

SCREENS['splash']      = SPLASH_SVG
SCREENS['main_open']   = MAIN_OPEN_SVG
SCREENS['main_closed'] = MAIN_CLOSED_SVG

def svg_to_rl_drawing(key, display_w_cm):
    """Converte SVG in ReportLab Drawing tramite svglib."""
    svg_src = SCREENS[key]
    buf = io.BytesIO(svg_src.encode())
    drawing = svg2rlg(buf)
    if drawing is None:
        return None
    w = display_w_cm * cm
    h = w * 320 / 240
    sx = w / drawing.width
    sy = h / drawing.height
    drawing.width  = w
    drawing.height = h
    drawing.transform = (sx, 0, 0, sy, 0, 0)
    return drawing

def screen_row(keys_captions, display_w_cm=3.8):
    """Genera una riga di schermate affiancate con didascalie."""
    cw = W - ML - MR
    n = len(keys_captions)
    col_w = cw / n
    img_w = display_w_cm * cm
    img_h = img_w * 320 / 240

    cells = []
    for key, caption in keys_captions:
        drawing = svg_to_rl_drawing(key, display_w_cm)
        cap = Paragraph(caption, ParagraphStyle('sc',
            fontName='Helvetica', fontSize=7.5, textColor=GREY,
            alignment=TA_CENTER, leading=10, spaceAfter=0))
        cells.append([drawing or Spacer(img_w, img_h), cap])

    data = [[c[0] for c in cells], [c[1] for c in cells]]
    ts = TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,0), 'BOTTOM'),
        ('VALIGN', (0,1), (-1,1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ])
    return Table(data, colWidths=[col_w]*n, style=ts)


# ── Stili testo ───────────────────────────────────────────────────────────────
def S(name, **kw):
    bases = {
        'h1':   dict(fontName='Helvetica-Bold', fontSize=15, textColor=PLUM,
                     spaceBefore=16, spaceAfter=5, leading=19),
        'h2':   dict(fontName='Helvetica-Bold', fontSize=12, textColor=TERRA,
                     spaceBefore=12, spaceAfter=3, leading=16),
        'h3':   dict(fontName='Helvetica-Bold', fontSize=10.5, textColor=PLUM_D,
                     spaceBefore=8, spaceAfter=2, leading=14),
        'body': dict(fontName='Helvetica', fontSize=10, textColor=INK,
                     spaceAfter=5, leading=15, alignment=TA_JUSTIFY),
        'bullet': dict(fontName='Helvetica', fontSize=10, textColor=INK,
                       spaceAfter=3, leading=14, leftIndent=12),
        'tip':  dict(fontName='Helvetica', fontSize=9.5, textColor=PLUM_D,
                     leading=14),
        'warn': dict(fontName='Helvetica', fontSize=9.5,
                     textColor=colors.HexColor('#6b3015'), leading=14),
        'tbl_hdr': dict(fontName='Helvetica-Bold', fontSize=9.5, textColor=WHITE, leading=13),
        'tbl_k':   dict(fontName='Helvetica-Bold', fontSize=9.5, textColor=PLUM, leading=13),
        'tbl_v':   dict(fontName='Helvetica', fontSize=9.5, textColor=INK, leading=13),
        'code':    dict(fontName='Courier', fontSize=9, textColor=PLUM_D, leading=13),
        'caption': dict(fontName='Helvetica', fontSize=7.5, textColor=GREY,
                        alignment=TA_CENTER, leading=10),
        'footer':  dict(fontName='Helvetica', fontSize=8, textColor=GREY),
        'step_n':  dict(fontName='Helvetica-Bold', fontSize=13, textColor=WHITE,
                        alignment=TA_CENTER, leading=16),
        'step_t':  dict(fontName='Helvetica-Bold', fontSize=10.5, textColor=PLUM_D,
                        leading=14, spaceAfter=1),
        'step_b':  dict(fontName='Helvetica', fontSize=9.5, textColor=INK, leading=13),
    }
    d = bases.get(name, {})
    d.update(kw)
    return ParagraphStyle(name, **d)

def h1(t):
    return [Paragraph(t, S('h1')),
            HRFlowable(width='100%', thickness=1.5, color=TERRA, spaceAfter=4)]

def h2(t): return [Paragraph(t, S('h2'))]
def h3(t): return [Paragraph(t, S('h3'))]
def body(t): return Paragraph(t, S('body'))
def sp(h=4): return Spacer(1, h)

def bullet(items):
    return [Paragraph(f'• {i}', S('bullet')) for i in items]

class Box(Flowable):
    def __init__(self, text, kind='tip'):
        super().__init__()
        self.text = text
        self.kind = kind
        self.bg  = colors.HexColor('#fcf0d8') if kind=='tip' else colors.HexColor('#fbe5d4')
        self.brd = SUN if kind=='tip' else TERRA
        self.lbl = '■ SUGGERIMENTO' if kind=='tip' else '■■ ATTENZIONE'
        self.lc  = PLUM_D if kind=='tip' else colors.HexColor('#6b3015')
        self.st  = S('tip') if kind=='tip' else S('warn')

    def wrap(self, aW, aH):
        self._w = aW
        p = Paragraph(self.text, self.st)
        _, ph = p.wrap(aW-20, 9999)
        self._h = ph + 28
        return aW, self._h

    def draw(self):
        c = self.canv
        c.setFillColor(self.bg); c.roundRect(0,0,self._w,self._h,8,fill=1,stroke=0)
        c.setStrokeColor(self.brd); c.setLineWidth(1.5)
        c.roundRect(0,0,self._w,self._h,8,fill=0,stroke=1)
        c.setFillColor(self.lc); c.setFont('Helvetica-Bold',8)
        c.drawString(10, self._h-14, self.label if hasattr(self,'label') else self.lbl)
        p = Paragraph(self.text, self.st)
        p.wrap(self._w-20, self._h); p.drawOn(c, 10, 8)

def tip(t): return Box(t, 'tip')
def warn(t): return Box(t, 'warn')

def dtable(headers, rows, cws=None):
    cw_total = W - ML - MR
    if cws is None:
        n = len(headers)
        cws = [cw_total*0.36] + [cw_total*0.64/(n-1)]*(n-1)
    data = [[Paragraph(h, S('tbl_hdr')) for h in headers]]
    for row in rows:
        data.append([Paragraph(str(row[0]), S('tbl_k'))] +
                    [Paragraph(str(c), S('tbl_v')) for c in row[1:]])
    ts = TableStyle([
        ('BACKGROUND',(0,0),(-1,0),PLUM),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,CREAM2]),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#d8cfbf')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
    ])
    return Table(data, colWidths=cws, style=ts, repeatRows=1)

def cmd_table(rows):
    cw = W - ML - MR
    data = [[Paragraph('Comando', S('tbl_hdr')), Paragraph('Effetto', S('tbl_hdr'))]]
    for cmd, desc in rows:
        data.append([Paragraph(f'<font name="Courier" size="9">{cmd}</font>', S('tbl_v')),
                     Paragraph(desc, S('tbl_v'))])
    ts = TableStyle([
        ('BACKGROUND',(0,0),(-1,0),PLUM),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE,CREAM2]),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#d8cfbf')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
    ])
    return Table(data, colWidths=[cw*0.28, cw*0.72], style=ts, repeatRows=1)

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(GREY); canvas.setFont('Helvetica', 8)
    canvas.drawString(ML, MB-6, 'ELETTROPOLLO · Manuale utente')
    canvas.drawRightString(W-MR, MB-6, 'Vergus · Elettropollo v2.2')
    canvas.drawCentredString(W/2, MB-6, f'Pagina {doc.page}')
    canvas.setStrokeColor(CREAM2); canvas.setLineWidth(0.5)
    canvas.line(ML, MB, W-MR, MB)
    canvas.restoreState()

# ═══════════════════════════════════════════════════════════════════════════════
# STORIA (contenuto)
# ═══════════════════════════════════════════════════════════════════════════════
def build_story():
    story = []

    # ── PRIMI PASSI ────────────────────────────────────────────────────────────
    story += h1('Primi passi rapidi')
    story.append(body('Non hai voglia di leggere tutto il manuale adesso? Bastano dieci minuti '
        'per accendere Elettropollo e vederlo funzionare. Segui questi cinque passi.'))
    story.append(sp(6))

    steps = [
        ('1','Imposta l\'orologio','Menù → Orologio. Ora, minuti e data: tutta l\'automazione dipende da qui.'),
        ('2','Inserisci le coordinate GPS','Menù → Sistema → Lat e Lon (più UTC +1 e DST), per l\'apertura su alba e tramonto.'),
        ('3','Programma un orario cibo','Menù → Cibo → Slot 1: imposta Ora e Durata. Bastano pochi secondi.'),
        ('4','Connetti WiFi + Telegram','Menù → Utilità → Notifiche WiFi → Config AP, poi configura dal telefono.'),
        ('5','Manda /status','Scrivi al bot: se risponde con il rapporto, sei operativo.'),
    ]
    cw = W-ML-MR
    for num,title,desc in steps:
        td = [[Paragraph(num,S('step_n')),
               [Paragraph(title,S('step_t')),Paragraph(desc,S('step_b'))]]]
        ts = TableStyle([
            ('BACKGROUND',(0,0),(0,0),TERRA),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',(1,0),(1,0),10),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('ROWBACKGROUNDS',(0,0),(-1,-1),[CREAM]),
            ('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#d8cfbf')),
        ])
        story.append(KeepTogether([Table(td,colWidths=[1.1*cm,cw-1.1*cm],style=ts),sp(4)]))

    story.append(sp(4))
    story.append(tip('Hai già fatto tutto e qualcosa non torna? Salta direttamente al capitolo 12, Risoluzione dei problemi.'))
    story.append(PageBreak())

    # ── AVVERTENZE ─────────────────────────────────────────────────────────────
    story += h1('Avvertenze e limitazione di responsabilità')
    story.append(body('Leggere attentamente prima dell\'installazione e dell\'uso. '
        'L\'utilizzo del prodotto implica l\'accettazione delle presenti condizioni.'))
    story += h2('Natura del prodotto')
    story.append(body('Elettropollo è un sistema di automazione ausiliario per pollai. '
        'Non è un dispositivo di sicurezza né un sistema di custodia degli animali: non sostituisce '
        'la sorveglianza, la cura e il controllo periodico diretto da parte del proprietario, '
        'che restano responsabilità esclusiva dell\'utilizzatore.'))
    story += h2('Limitazione di responsabilità')
    story.append(body('Nei limiti massimi consentiti dalla legge applicabile, il produttore non '
        'potrà essere ritenuto responsabile per danni diretti o indiretti derivanti dall\'uso, '
        'dall\'uso improprio o dal mancato funzionamento del prodotto, inclusi a titolo '
        'esemplificativo: perdita o lesione di animali, mancata apertura o chiusura della porta, '
        'mancata erogazione di cibo o acqua, interruzioni di connettività, mancato recapito di '
        'notifiche, eventi atmosferici, azione di predatori.'))
    story.append(body('Il funzionamento di alcune funzioni dipende da servizi di terze parti '
        '(rete WiFi, piattaforma Telegram) sui quali il produttore non ha alcun controllo.'))
    story.append(PageBreak())

    # ── 1. BENVENUTO ───────────────────────────────────────────────────────────
    story += h1('1. Benvenuto')
    story.append(body('Elettropollo si occupa del tuo pollaio ogni giorno, al posto tuo: apre e '
        'chiude la porta seguendo il sole, distribuisce mangime e acqua agli orari che decidi tu, '
        'esegue la pulizia del fondo, protegge dal gelo e ti tiene aggiornato sul telefono tramite Telegram.'))
    story.append(body('Questo manuale descrive la centralina Elettropollo con firmware v2.2. '
        'Non serve alcuna competenza tecnica: tutte le impostazioni si fanno con una manopola, '
        'un tasto e il display TFT a colori 2,4″.'))
    story += h2('Cosa gestisce il sistema')
    story += bullet([
        'Porta del pollaio — apertura e chiusura automatica, a orari fissi o sull\'alba e il tramonto reali.',
        'Cibo e acqua — fino a 8 erogazioni al giorno ciascuno, con orario e durata indipendenti.',
        'Pulizia — ciclo motorizzato del fondo, programmabile fino a 8 volte al giorno.',
        'Antigelo — riscaldatore automatico con termostato per proteggere l\'acqua dal gelo.',
        'Campana — suono di richiamo prima della chiusura serale.',
        'Relè ausiliario — comanda un\'utenza a tua scelta a fasce orarie.',
        'Notifiche e comandi Telegram — il pollaio ti scrive, e tu puoi comandarlo da remoto.',
        'Home Assistant — integrazione MQTT nativa con discovery automatica delle entità.',
        'Batteria — monitoraggio della tensione con avviso se scende sotto soglia.',
        'Bilancia uova (opzionale) — cella di carico HX711, conta automaticamente le deposizioni, reset a mezzanotte.',
    ])
    story.append(sp(4))
    story.append(warn('La centralina comanda motori e può comandare utenze elettriche esterne. '
        'Prima di qualsiasi intervento su cablaggi o collegamenti, togli alimentazione.'))

    # ── 2. CONOSCI LA CENTRALINA ───────────────────────────────────────────────
    story += h1('2. Conosci la centralina')
    story += h2('Comandi fisici')
    story.append(dtable(['Comando','Cosa fa'],[
        ['Manopola (encoder)','Ruota per scorrere le voci di menu o cambiare un valore.'],
        ['Pressione della manopola','Conferma, entra in una voce, salva il valore.'],
        ['Tasto BACK','Torna indietro o annulla la modifica in corso.'],
        ['Encoder — Ritardo chiusura',
         'Da Menù → Porta → Rit chiusura: ruota per impostare il ritardo di chiusura serale '
         '(0–90 minuti), poi premi per confermare.'],
    ]))
    story.append(sp(10))
    story += h2('Il display TFT a colori')
    story.append(body('Il display TFT 2,4″ (240×320 px) mostra quattro aree nella schermata principale: '
        'stato della porta con orario prossima transizione; alba e tramonto del giorno; '
        'temperatura e tensione batteria; prossime erogazioni e stato relè ausiliario.'))
    story.append(sp(8))

    story.append(KeepTogether([
        screen_row([
            ('splash',     'Avvio sistema'),
            ('main_open',  'Porta aperta — modo astro'),
            ('main_closed','Porta chiusa — batteria bassa'),
        ], display_w_cm=4.2),
        sp(6),
    ]))

    story.append(body('Premi la manopola per entrare nel menù. Le voci scorrono con la rotella; '
        'la riga selezionata è evidenziata in viola con striscia arancione a sinistra. '
        'Ogni voce mostra il valore corrente sotto al nome.'))
    story.append(sp(8))
    story.append(KeepTogether([
        screen_row([
            ('root_pulizia', 'Menù principale'),
            ('menu_sistema', 'Sottomenù Sistema'),
            ('menu_utilita', 'Sottomenù Utilità'),
        ], display_w_cm=4.2),
        sp(6),
    ]))
    story += h2('Lingua')
    story.append(body('L\'interfaccia è disponibile in italiano e tedesco (Menù → Sistema → Lingua). '
        'Anche i messaggi Telegram seguono la lingua scelta.'))

    # ── 3. PRIMA CONFIGURAZIONE ────────────────────────────────────────────────
    story += h1('3. Prima configurazione')
    story.append(body('Alla prima accensione segui questi passi nell\'ordine. Bastano dieci minuti.'))
    for title, desc in [
        ('Passo 1 — Imposta l\'orologio.', 'Menù → Orologio. Regola ora, minuti, giorno, mese e anno.'),
        ('Passo 2 — Scegli quanti slot.', 'Menù → Sistema → Slot cibo / Slot acqua / Slot pulizia (1–8).'),
        ('Passo 3 — Programma il cibo.', 'Menù → Cibo → Slot 1…N: Ora (HH:MM) e Durata (0–180 s).'),
        ('Passo 4 — Programma l\'acqua.', 'Menù → Acqua, stessa logica del cibo.'),
        ('Passo 5 — Configura la porta.', 'Menù → Sistema → Tipo orari: User (fissi) oppure Astro (alba/tramonto).'),
        ('Passo 6 — Imposta i termostati.', 'Menù → Termostati → Sonda: temperatura antigelo (di serie 3 °C).'),
        ('Passo 7 — Collega WiFi e Telegram.', 'Facoltativo. Segui il capitolo 9.'),
    ]:
        story.append(body(f'<b>{title}</b> {desc}'))
    story.append(sp(4))
    story.append(tip('Un orario a --:-- o una durata a 0 disattivano lo slot.'))

    # ── 4. LA PORTA ────────────────────────────────────────────────────────────
    story += h1('4. La porta')
    story += h2('Due modalità')
    story.append(body('<b>User (orari fissi).</b> Imposti tu apertura e chiusura in Menù → Porta → Apertura / Chiusura.'))
    story.append(body('<b>Astro (astronomica).</b> La centralina calcola alba e tramonto reali ogni giorno. '
        'Gli orari si aggiornano da soli con le stagioni.'))
    story.append(dtable(['Voce','Valore da impostare','Nota'],[
        ['UTC','+1.0','Fuso orario base (senza ora legale)'],
        ['DST','ON / OFF','Ora legale: ON in estate, OFF in inverno'],
        ['Lat','45.7845','Latitudine decimale, positiva = Nord'],
        ['Lon','8.4123','Longitudine decimale, positiva = Est'],
    ], cws=[(W-ML-MR)*f for f in [0.22,0.22,0.56]]))
    story.append(sp(6))
    story += h2('Ritardo di chiusura')
    story.append(body('Puoi posticipare la chiusura rispetto al tramonto fino a 90 minuti, '
        'impostandolo da Menù → Porta → Rit chiusura con l\'encoder.'))
    story += h2('Microinterruttori di posizione')
    story.append(body('Se installati, la centralina verifica che la porta raggiunga la posizione '
        'comandata entro il timeout. In caso di blocco segnala guasto sul display e via Telegram.'))
    story.append(sp(4))
    story.append(warn('Il guasto porta è l\'avviso più importante: se arriva di sera la porta '
        'potrebbe essere rimasta aperta. Verifica appena possibile.'))

    # ── 5. CIBO E ACQUA ────────────────────────────────────────────────────────
    story += h1('5. Cibo e acqua')
    story.append(body('Ogni giorno la centralina attiva il distributore agli orari programmati, '
        'per la durata impostata, una sola volta per slot. Fino a 8 slot al giorno per cibo e 8 per acqua.'))
    story.append(dtable(['Parametro','Valore'],[
        ['Slot','fino a 8 al giorno per cibo e 8 per acqua'],
        ['Ora','HH:MM, oppure --:-- per disattivare'],
        ['Durata','0–180 secondi per slot'],
    ]))
    story.append(sp(4))
    story.append(tip('Le galline amano la routine: orari regolari mattina e tardo pomeriggio riducono stress e sprechi.'))

    # ── 6. MONITORAGGIO LIVELLO ────────────────────────────────────────────────
    story += h1('6. Monitoraggio del livello')
    story.append(body('Sensori non invasivi XKC-Y25-NPN applicati all\'esterno dei contenitori '
        'rilevano quando le scorte stanno per finire, senza contatto con il contenuto. '
        'Applica il sensore all\'altezza della riserva minima (circa il 20% del volume). '
        'Collegamento: rosso → 12V, nero → GND, giallo → GPIO.'))
    story.append(dtable(['Evento','Notifica Telegram'],[
        ['Livello acqua basso','Avviso di rabbocco del contenitore acqua.'],
        ['Livello cibo basso','Avviso di rabbocco delle granaglie.'],
    ]))

    # ── 7. PULIZIA ─────────────────────────────────────────────────────────────
    story += h1('7. Pulizia automatica')
    story.append(body('Un motore con sensori di punto zero e fine corsa muove il fondo del pollaio. '
        'Ogni ciclo rientra al punto zero, esegue la corsa completa e torna a riposo. '
        'Fino a 8 cicli al giorno; se una fase supera il timeout il ciclo si ferma e segnala guasto.'))
    story.append(sp(8))
    story.append(KeepTogether([
        screen_row([
            ('menu_pulizia',     'Slot pulizia'),
            ('menu_ctrl_pulizia','Ctrl pulizia'),
        ], display_w_cm=4.2),
        sp(4),
    ]))

    # ── 7b. CONTROLLO MANUALE ──────────────────────────────────────────────────
    story += h1('7b. Controllo manuale')
    story.append(body('Il menù Manuale permette di attivare o disattivare ogni uscita in tempo reale, '
        'indipendentemente dagli orari programmati. Utile per test e tarature.'))
    story.append(dtable(['Voce','Effetto'],[
        ['Cibo man / Acqua man','Aziona subito il relè distributore.'],
        ['Riscaldatore','Attiva/disattiva il riscaldatore antigelo.'],
        ['Campana man','Suona la campana manualmente.'],
        ['Aux man','Attiva/disattiva il relè ausiliario.'],
        ['Attiva porta / Ctrl porta','Attiva porta = uscita di potenza; Ctrl porta = segnale direzione.'],
        ['Attiva pulizia / Ctrl pulizia','Stessa logica per il motore di pulizia.'],
    ]))
    story.append(sp(8))
    story.append(KeepTogether([
        screen_row([
            ('menu_manuale',   'Controllo manuale pg.1'),
            ('menu_manuale_p2','Controllo manuale pg.2'),
        ], display_w_cm=4.2),
        sp(6),
    ]))
    story.append(warn('I comandi porta e pulizia del menù manuale sono attivi finché non li riporti a OFF. '
        'Non lasciare la porta in uno stato sbagliato per distrazione.'))

    # ── 7c. SISTEMA ────────────────────────────────────────────────────────────
    story += h1('7c. Sistema')
    story.append(body('Il menù Sistema raccoglie tutti i parametri di configurazione globale.'))
    story.append(dtable(['Voce','Descrizione'],[
        ['Slot cibo / acqua / pulizia','Numero di slot giornalieri attivi (1–8) per ogni funzione.'],
        ['Tipo orari','User = orari fissi, Astro = alba/tramonto calcolati.'],
        ['Rit chiusura','Ritardo di chiusura (0–90 min), impostato con l\'encoder.'],
        ['DST','Ora legale: ON in estate, OFF in inverno.'],
        ['UTC','Fuso orario base (es. +1.0 per l\'Italia).'],
        ['Lat / Lon','Coordinate GPS decimali per il calcolo astronomico.'],
        ['Sleep disp','Minuti di inattività prima dello spegnimento display (0 = sempre acceso).'],
        ['Lingua','Italiano o Deutsch.'],
        ['Inv relè','Inverte la logica NC/NO di ogni singolo relè.'],
    ]))
    story.append(sp(8))
    story.append(KeepTogether([
        screen_row([
            ('menu_sistema',   'Sistema pg.1'),
            ('menu_sistema_p2','Sistema pg.2'),
            ('menu_inv_rele',  'Inversione relè'),
        ], display_w_cm=4.2),
        sp(6),
    ]))

    # ── 7d. UTILITÀ ────────────────────────────────────────────────────────────
    story += h1('7d. Utilità')
    story += h2('Campana')
    story.append(body('Suona prima della chiusura serale per richiamare le galline. '
        'Si impostano anticipo (minuti + secondi, fino a 30 min) e durata del suono (fino a 30 s).'))
    story += h2('Relè ausiliario')
    story.append(body('Fino a 8 fasce orarie indipendenti per un\'uscita libera. '
        'Controllabile anche via Telegram con /aux_on, /aux_off, /aux_auto.'))
    story += h2('Ctrl microinterruttori porta')
    story.append(body('Verifica che la porta raggiunga la posizione entro il timeout. '
        'Diagnostica per lo stato dei sensori in tempo reale e Test porta per un ciclo di prova.'))
    story += h2('Ctrl livello')
    story.append(body('Abilita i sensori XKC, diagnostica live e notifica Telegram sul livello basso.'))
    story += h2('Ctrl pulizia')
    story.append(body('Timeout per fase, diagnostica sensori e avvio ciclo di test.'))
    story.append(sp(8))
    story.append(KeepTogether([
        screen_row([
            ('menu_utilita','Utilità'),
            ('menu_campana','Campana'),
            ('menu_aux',   'Relè ausiliario'),
        ], display_w_cm=4.2),
        sp(4),
    ]))
    story.append(KeepTogether([
        screen_row([
            ('menu_micro',      'Ctrl micro porta'),
            ('menu_livello',    'Ctrl livello'),
            ('menu_ctrl_pulizia','Ctrl pulizia'),
        ], display_w_cm=4.2),
        sp(6),
    ]))

    # ── 7e. BILANCIA UOVA ──────────────────────────────────────────────────────
    story += h1('7e. Bilancia uova')
    story.append(body('La bilancia uova usa una cella di carico HX711 per rilevare automaticamente '
        'ogni deposizione delle galline. Il modulo è opzionale: se l\'HX711 non risponde '
        'all\'avvio la funzione rimane disabilitata. Accesso dal menù: Utilità → Bilancia.'))
    story += h2('Come funziona')
    story.append(body('La state machine ha tre stati:'))
    story += bullet([
        'IDLE — nessuna gallina sul nido. La bilancia campiona il peso netto ogni 400 ms.',
        'HEN_IN — peso netto ≥ soglia gallina (default 500 g sopra la tara corrente): gallina rilevata.',
        'SETTLING — gallina uscita: il sistema aspetta il debounce (default 9 s). Se il peso residuo '
        'rientra tra Min g e Max g viene contato come uovo e la tara aggiornata al peso assoluto corrente.',
    ])
    story.append(body('Con la porta chiusa la state machine è sospesa per evitare falsi positivi. '
        'Il contatore si azzera automaticamente a mezzanotte (la tara viene mantenuta).'))
    story.append(sp(8))
    story.append(KeepTogether([
        screen_row([
            ('menu_bilancia','Bilancia uova'),
        ], display_w_cm=4.2),
        sp(6),
    ]))
    story += h2('Parametri del menù Bilancia')
    story.append(dtable(['Voce','Funzione'],[
        ['Abilitata','Abilita/disabilita la state machine. Se OFF non vengono effettuati campionamenti.'],
        ['Tara ora','Acquisisce il peso corrente come tara: azzera il peso netto senza toccare il contatore uova.'],
        ['Peso live','Apre la schermata di monitoraggio con peso netto in tempo reale e contatore uova del giorno.'],
        ['Soglia gallina (g)','Peso netto minimo (g sopra tara) per riconoscere una gallina. Default 500 g.'],
        ['Fattore','Fattore di calibrazione HX711 (raw/grammo). Da regolare con un peso noto. Default 420.'],
        ['Min uovo g','Peso residuo minimo per contare un uovo. Default 35 g.'],
        ['Max uovo g','Peso massimo per singolo uovo. Residui superiori vengono ignorati come anomalia. Default 150 g.'],
        ['Peso/uovo g','Peso medio atteso per uovo, usato per stimare il numero se più uova vengono deposte insieme. Default 60 g.'],
        ['Debounce s','Secondi di peso stabile dopo l\'uscita della gallina prima di decidere. Default 9 s.'],
    ]))
    story.append(sp(6))
    story += h2('Pulsante fisico tara (GPIO 34)')
    story.append(body('Un pulsante fisico collegato al GPIO 34 permette di azzerare bilancia e '
        'contatore senza entrare nel menù: tieni premuto almeno 800 ms. '
        'Ideale subito dopo la raccolta delle uova.'))
    story.append(tip('Per calibrare il Fattore: metti un peso noto (es. 500 g) sul piatto, apri '
        'Peso live e confronta il valore mostrato con il peso reale. '
        'Aumenta il fattore se il display legge troppo poco, diminuiscilo se legge troppo.'))
    story += h2('Comandi Telegram bilancia')
    story.append(cmd_table([
        ('/uova','Uova deposte oggi, peso netto corrente e stato bilancia (IDLE / gallina / debounce).'),
        ('/uova_reset','Azzera il contatore uova di oggi (la tara rimane invariata).'),
        ('/uova_tara','Acquisisce la tara al peso corrente e azzera il contatore (equivale al pulsante fisico).'),
    ]))

    # ── 8. ANTIGELO, CAMPANA, AUX ──────────────────────────────────────────────
    story += h1('8. Antigelo, campana e relè ausiliario')
    story.append(body('<b>Antigelo.</b> Una sonda DS18B20 controlla il riscaldatore: sotto il setpoint '
        '(di serie 3 °C) si accende, con isteresi di ±1 °C. Imposta in Menù → Termostati → Sonda.'))
    story.append(body('<b>Campana.</b> Suona prima della chiusura serale. Imposta anticipo e durata '
        'in Menù → Utilità → Campana.'))
    story.append(body('<b>Relè ausiliario.</b> Fino a 8 fasce orarie o controllo Telegram '
        '(/aux_on, /aux_off, /aux_auto) per luce, pompa, recinto o qualsiasi altro carico.'))

    # ── 9. WIFI E TELEGRAM ─────────────────────────────────────────────────────
    story += h1('9. WiFi e Telegram')
    story.append(body('La configurazione avviene tramite una pagina web servita direttamente '
        'dall\'access point interno della centralina. Non serve installare nessuna app.'))
    story += h2('Passo 1 — Attiva l\'access point')
    story.append(body('Menù → Utilità → Notifiche WiFi → Config AP. '
        'In alternativa, dalla schermata principale tieni premuta la manopola per 2 secondi: '
        'il portale si avvia (o si ferma se già attivo) senza aprire il menù.'))
    story.append(tip('SSID: ElettroCfg   ·   Password: pollo1234'))
    story += h2('Passo 2 — Apri la pagina di configurazione')
    story.append(body('Collegati alla rete ElettroCfg, poi apri il browser all\'IP mostrato sul '
        'display alla voce IP AP (di solito 192.168.4.1).'))
    story += h2('Passo 3 — Compila i campi')
    story.append(dtable(['Campo','Cosa inserire'],[
        ['SSID rete','Il nome della tua rete WiFi di casa. Puoi selezionarla dalla lista in fondo alla pagina.'],
        ['Password rete','La password del tuo router.'],
        ['Telegram — Bot token','Token ottenuto da @BotFather (es. 123456789:AAbbcc...).'],
        ['Telegram — Chat ID','Il tuo ID numerico, ottenuto scrivendo a @userinfobot.'],
    ]))
    story.append(sp(6))
    story += h2('Passo 4 — Crea il bot Telegram')
    story += bullet([
        'Apri Telegram e cerca @BotFather.',
        'Manda /newbot, scegli nome e username (deve finire in bot, es. MioPollaioBot).',
        'BotFather risponde con il token — copialo nel campo Bot token.',
        'Scrivi a @userinfobot: risponde con il tuo Chat ID — inseriscilo nell\'apposito campo.',
    ])
    story.append(sp(4))
    story.append(tip('Per notifiche su un gruppo Telegram usa l\'ID del gruppo come Chat ID (inizia con -100).'))
    story += h2('Passo 5 — Salva e verifica')
    story.append(body('Premi Salva e collega. Quando Stato STA mostra Connesso, '
        'vai su Test Telegram: se arriva il messaggio di prova sei operativo.'))
    story += h2('Comandi Telegram')
    story.append(cmd_table([
        ('/help','Mostra la lista di tutti i comandi.'),
        ('/status','Rapporto completo: orari, temperatura, batteria, porta, cibo, acqua, AUX.'),
        ('/cibo_now','Avvia subito una razione di cibo.'),
        ('/acqua_now','Avvia subito una razione d\'acqua.'),
        ('/pulizia_now','Avvia subito un ciclo di pulizia.'),
        ('/porta_aperta','Forza la porta aperta (override).'),
        ('/porta_chiusa','Forza la porta chiusa (override).'),
        ('/porta_auto','Riporta la porta alla programmazione automatica.'),
        ('/aux_on · /aux_off','Forza il relè ausiliario ON oppure OFF.'),
        ('/aux_auto','Riporta il relè AUX alla programmazione oraria.'),
        ('/version','Versione firmware installato.'),
        ('/uova','Uova deposte oggi, peso netto corrente e stato bilancia (IDLE / gallina / debounce). Richiede modulo HX711.'),
        ('/uova_reset','Azzera il contatore uova di oggi (la tara rimane invariata).'),
        ('/uova_tara','Acquisisce la tara al peso corrente e azzera il contatore (equivale al pulsante fisico).'),
    ]))
    story.append(sp(4))
    story.append(warn('Gli override porta e AUX restano attivi finché non invii il comando _auto. '
        'Se dimentichi /porta_auto attivo, la sera la porta non si chiuderà.'))
    story.append(sp(8))
    story += h2('Tipi di notifica')
    story.append(body('In Menù → Utilità → Notifiche WiFi → Tipi notif scegli quali avvisi ricevere:'))
    story.append(dtable(['Notifica','Quando arriva'],[
        ['Cibo / Acqua','A ogni erogazione completata.'],
        ['Porta ON / OFF','All\'apertura e alla chiusura della porta.'],
        ['Aux ON / OFF','Quando il relè ausiliario cambia stato.'],
        ['Antigelo ON / OFF','Quando il riscaldatore si accende o si spegne.'],
        ['Volt + Soglia','Quando la tensione scende sotto la soglia configurata (9,0–14,5 V).'],
        ['Livello basso','Quando acqua o granaglie scendono sotto la soglia del sensore.'],
    ]))
    story.append(sp(8))
    story.append(KeepTogether([
        screen_row([
            ('menu_wifi',   'WiFi / Telegram pg.1'),
            ('menu_wifi_p2','WiFi / Telegram pg.2'),
            ('menu_notif',  'Tipi di notifica'),
        ], display_w_cm=4.2),
        sp(6),
    ]))

    # ── 9b. HOME ASSISTANT ─────────────────────────────────────────────────────
    story += h1('9b. Home Assistant')
    story.append(body('Elettropollo si integra con Home Assistant tramite MQTT con Discovery '
        'automatica: una volta configurato il broker, tutte le entità appaiono in HA senza '
        'toccare file YAML.'))
    story += h2('Prerequisiti')
    story += bullet([
        'Home Assistant installato e raggiungibile sulla rete locale.',
        'Add-on Mosquitto broker installato e avviato (o qualsiasi broker MQTT).',
        'MQTT Discovery abilitata in HA (attiva per default).',
    ])
    story += h2('Configurazione')
    story.append(body('Nella pagina web WiFi compila la sezione Home Assistant MQTT:'))
    story.append(dtable(['Campo','Cosa inserire'],[
        ['Broker (host o IP)','IP del server Home Assistant, es. 192.168.1.10.'],
        ['Porta','Lascia 1883 (default). Cambia solo se hai configurato una porta diversa.'],
        ['Username MQTT','Utente MQTT creato in HA → Mosquitto → Configurazione → Utenti.'],
        ['Password MQTT','Password dell\'utente MQTT.'],
    ]))
    story.append(sp(6))
    story.append(body('Poi dal display: Menù → Utilità → Home Assist. → Abilitata → ON. '
        'Elettropollo si connette e pubblica la Discovery.'))
    story += h2('Entità create automaticamente')
    story.append(dtable(['Entità','Tipo','Descrizione'],[
        ['Porta','Cover','Stato aperta/chiusa con controllo remoto da HA.'],
        ['Temperatura','Sensor','Lettura sonda DS18B20 in °C (se presente).'],
        ['Temperatura ESP32','Sensor','Temperatura interna del microcontrollore.'],
        ['Tensione','Sensor','Tensione batteria in V (se monitoraggio volt abilitato).'],
        ['Livello acqua','Binary sensor','ON = acqua presente, OFF = livello basso.'],
        ['Livello grano','Binary sensor','ON = grano presente, OFF = livello basso.'],
        ['AUX','Switch','Controllo diretto del relè ausiliario da HA.'],
        ['Cibo ora','Button','Avvia una razione di cibo immediata.'],
        ['Acqua ora','Button','Avvia una razione d\'acqua immediata.'],
        ['Pulizia ora','Button','Avvia un ciclo di pulizia immediato.'],
        ['Uova oggi','Sensor','Contatore uova deposte nel giorno corrente (solo se il modulo HX711 è presente).'],
    ], cws=[(W-ML-MR)*f for f in [0.28,0.20,0.52]]))
    story.append(sp(4))
    story.append(tip('Se le entità non compaiono in HA usa Menù → Utilità → Home Assist. → Republish. '
        'Puoi verificare lo stato in Menù → Utilità → Home Assist. → Stato.'))
    story.append(sp(8))
    story.append(KeepTogether([
        screen_row([
            ('menu_ha','Home Assistant MQTT'),
        ], display_w_cm=4.2),
        sp(6),
    ]))

    # ── 10. BATTERIA ───────────────────────────────────────────────────────────
    story += h1('10. Alimentazione e batteria')
    story.append(body('La centralina misura continuamente la tensione di alimentazione e la mostra '
        'nella schermata principale e nel rapporto /status. Se scende sotto la soglia ricevi '
        'una notifica Telegram.'))
    story.append(tip('Per una batteria al piombo 12 V la soglia di serie (11,5 V) va bene. '
        'Per una LiFePO4 puoi alzarla a 12,5–12,8 V per avere più preavviso.'))

    # ── 11. IMPOSTAZIONI AVANZATE ──────────────────────────────────────────────
    story += h1('11. Impostazioni avanzate')
    story += h2('Inversione relè')
    story.append(body('In Menù → Sistema → Inv relè puoi invertire la logica NC/NO di ogni singolo '
        'relè. Da toccare solo se sai cosa stai facendo.'))
    story += h2('Salvataggio delle impostazioni')
    story.append(body('Tutte le impostazioni vengono salvate nella memoria interna e sopravvivono '
        'alla mancanza di corrente. Il modulo RTC DS3231 mantiene data e ora anche dopo un blackout prolungato.'))

    # ── 12. RISOLUZIONE PROBLEMI ───────────────────────────────────────────────
    story += h1('12. Risoluzione dei problemi')
    story.append(dtable(['Problema','Cosa controllare'],[
        ['La porta non si apre/chiude agli orari attesi',
         'Verifica data e ora. In Astro controlla UTC, DST, Lat e Lon. Assicurati che nessun override Telegram sia attivo (invia /porta_auto).'],
        ['Avviso "guasto porta micro"',
         'La porta non ha raggiunto la posizione entro il timeout: cerca ostacoli o sporco. Usa Diagnostica e Test porta in Utilità → Ctrl micro.'],
        ['Cibo o acqua non erogati',
         'Slot con orario valido e durata > 0. Numero slot attivi in Sistema sufficiente. Prova dal menù Manuale.'],
        ['La pulizia si ferma a metà',
         'Controlla sensori punto zero e fine corsa (Diagnostica) e timeout sufficiente per la corsa completa.'],
        ['Niente notifiche Telegram',
         'Verifica Stato STA, poi Test Telegram. Controlla token e Chat ID. Verifica che il tipo di notifica sia attivo in Tipi notif.'],
        ['HA non vede le entità',
         'Verifica Abilitata ON e stato MQTT Connesso. Se broker di recente ripristinato usa Republish. Controlla MQTT Discovery in HA.'],
        ['Display spento',
         'Sleep automatico: ruota o premi la manopola. Regola in Sistema → Sleep disp.'],
        ['Orari astronomici sbagliati',
         'Latitudine o longitudine errate (occhio al segno), UTC sbagliato, o DST non aggiornato.'],
        ['Riscaldatore non parte',
         'Verifica setpoint (Termostati → Sonda) e ricorda isteresi: accende a setpoint−1 °C.'],
        ['Notifica livello assente',
         'Sensore a contatto con la parete. Per granaglie agita il contenitore. Controlla cablaggio (rosso→12V, nero→GND, giallo→GPIO).'],
    ], cws=[(W-ML-MR)*0.36, (W-ML-MR)*0.64]))

    # ── 13. MAPPA DEL MENÙ ─────────────────────────────────────────────────────
    story += h1('13. Mappa del menù')
    story.append(body('Riferimento rapido di tutte le voci. Dalla schermata principale: premi la manopola.'))
    story.append(dtable(['Voce','Contenuto'],[
        ['Porta','Apertura · Chiusura · Rit chiusura · Modalità · DST · UTC · Lat · Lon'],
        ['Cibo','Slot 1–8 → Ora · Durata'],
        ['Acqua','Slot 1–8 → Ora · Durata'],
        ['Pulizia','Slot 1–8 → Ora'],
        ['Termostati','Sonda · ESP32'],
        ['Orologio','Ora, minuti, giorno, mese, anno'],
        ['Manuale','Cibo · Acqua · Riscaldatore · Termo ESP32 · Campana · Aux · Porta (att+ctrl) · Pulizia (att+ctrl)'],
        ['Sistema','Slot cibo/acqua/pulizia · Tipo orari · Rit chiusura · DST · UTC · Lat · Lon · Sleep disp · Lingua · Inv relè'],
        ['Utilità','Campana · Relè aux · Ctrl micro · Ctrl livello · Ctrl pulizia · Bilancia · Notifiche WiFi · Home Assist.'],
        ['Guida rapida','Sommario · Orari porta · Cibo · Acqua · Termostato · Manuale · Sistema · Utilità'],
    ]))
    story.append(sp(8))
    story += h2('Dati tecnici essenziali')
    story.append(dtable(['Parametro','Valore'],[
        ['Slot cibo / acqua / pulizia','1–8 ciascuno, indipendenti'],
        ['Durata erogazione','0–180 secondi per slot'],
        ['Ritardo chiusura porta','0–90 minuti (impostato via encoder)'],
        ['Timeout micro porta','fino a 120 s (di serie 25 s)'],
        ['Timeout ciclo pulizia','fino a 600 s'],
        ['Campana','anticipo fino a 30 min, durata fino a 30 s'],
        ['Eventi relè ausiliario','fino a 8 fasce ON/OFF al giorno'],
        ['Soglia avviso tensione','9,0–14,5 V (di serie 11,5 V)'],
        ['Termostato antigelo','setpoint di serie 3 °C, isteresi ±1 °C'],
        ['Lingue','Italiano, Deutsch'],
        ['Sensori livello','2× XKC-Y25-NPN, non invasivi, applicati esternamente'],
        ['Access point config','SSID: ElettroCfg  ·  Password: pollo1234'],
        ['Broker MQTT default','IP locale, porta 1883'],
    ]))

    # ── 14. SCHEDA TECNICA ─────────────────────────────────────────────────────
    story += h1('14. Scheda tecnica')
    story.append(dtable(['Caratteristica','Specifica'],[
        ['Unità di controllo','Modulo ESP32-S3 Freenove dual-core con WiFi integrato'],
        ['Display','TFT a colori 2,4″ 240×320 px (ST7789), con spegnimento automatico configurabile'],
        ['Interfaccia utente','Encoder rotativo con pulsante, tasto BACK'],
        ['Orologio','Modulo RTC DS3231 con batteria tampone'],
        ['Sensore temperatura','Sonda digitale DS18B20 impermeabile'],
        ['Calcolo astronomico','Alba e tramonto calcolati localmente ogni giorno (nessuna connessione richiesta)'],
        ['Uscite','10 relè: cibo, acqua, riscaldatore, campana, ausiliario, ventola quadro, motore pulizia, inversione pulizia, attivazione porta, controllo porta'],
        ['Ingressi','2 microinterruttori posizione porta, 2 sensori corsa pulizia, 2 sensori livello XKC-Y25-NPN'],
        ['Bilancia uova (opzionale)','Cella di carico HX711, GPIO DOUT=10 SCK=33, pulsante tara GPIO=34, calibrazione da menù, reset mezzanotte'],
        ['Connettività','WiFi 2,4 GHz; access point integrato; Telegram; MQTT/Home Assistant Discovery'],
        ['Memoria impostazioni','Memoria interna non volatile con verifica integrità'],
        ['Lingue interfaccia','Italiano e tedesco (display e messaggi Telegram)'],
        ['Alimentazione','12 V CC, adatto a impianto solare con batteria'],
        ['Firmware','Elettropollo v2.2, sviluppato in proprio'],
    ]))
    story.append(sp(12))
    story.append(body('Buon lavoro, e buone uova. ■'))

    return story

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD: genera il PDF del contenuto, poi unisce con la copertina
# ═══════════════════════════════════════════════════════════════════════════════
CONTENT_PDF = __import__('os').path.join(_SCRIPT_DIR, 'manuale_content.pdf')
FINAL_PDF   = __import__('os').path.join(_SCRIPT_DIR, '..', 'assets', 'Elettropollo_Manuale_Utente.pdf')
COVER_PDF   = __import__('os').path.join(_SCRIPT_DIR, 'cover.pdf')

doc = SimpleDocTemplate(
    CONTENT_PDF, pagesize=A4,
    leftMargin=ML, rightMargin=MR, topMargin=MT, bottomMargin=MB,
    title='Elettropollo - Manuale utente',
    author='Vergus',
)
doc.build(build_story(), onFirstPage=on_page, onLaterPages=on_page)
print(f'Contenuto generato: {CONTENT_PDF}')

# Unisce copertina + contenuto
writer = PdfWriter()
for path in [COVER_PDF, CONTENT_PDF]:
    reader = PdfReader(path)
    for page in reader.pages:
        writer.add_page(page)

with open(FINAL_PDF, 'wb') as f:
    writer.write(f)

import os
size = os.path.getsize(FINAL_PDF)
print(f'PDF finale: {FINAL_PDF} ({size//1024} KB)')

from pypdf import PdfReader as R
print(f'Pagine totali: {len(R(FINAL_PDF).pages)}')
