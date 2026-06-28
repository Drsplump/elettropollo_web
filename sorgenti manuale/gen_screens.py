# Generatore SVG schermate TFT Elettropollo
# 240x320 px, scala 160x213 per il web (viewBox="0 0 240 320")

# Palette colori firmware
C = {
    'BG':       '#1C1008',
    'SURFACE':  '#2C1A08',
    'CARD':     '#3A2210',
    'BORDER':   '#6B4020',
    'VERGUS':   '#7B3F00',
    'VERG_LT':  '#C1692A',
    'CREAM':    '#FEB6A0',
    'CREAM_DIM':'#DDD8C0',
    'TEXT':     '#F5E2C0',
    'SUB':      '#C4CB90',
    'MUTED':    '#E48A50',
    'GREEN':    '#670C20',   # verde (codice TFT vero)
    'RED':      '#FB8820',   # rosso caldo
    'AMBER':    '#FDC200',
    'PURPLE':   '#C39E80',
    'BLUE':     '#659E80',
    'SCROLLBAR':'#C1692A',
}

W, H = 240, 320
HDR = 28
ROW_H = 40
VIS = 6      # righe visibili
SCROLL_W = 4
CONTENT_W = W - SCROLL_W  # 236

def svg_open(aria=""):
    return f'<svg width="160" height="213" viewBox="0 0 240 320" xmlns="http://www.w3.org/2000/svg" aria-label="{aria}">\n'

def svg_close():
    return '</svg>'

def rect(x,y,w,h,fill,stroke=None,sw=1,rx=0):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}"'
    if rx: s += f' rx="{rx}"'
    s += f' fill="{fill}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{sw}"'
    return s + '/>'

def text(x,y,txt,fill,anchor='start',size=12,bold=False):
    fw = 'bold' if bold else 'normal'
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="sans-serif" font-weight="{fw}" font-size="{size}" fill="{fill}">{txt}</text>'

def line(x1,y1,x2,y2,stroke,sw=1):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}"/>'

def header(title, back=False):
    out = rect(0,0,W,HDR,C['VERGUS'])
    if back:
        out += text(10, 19, '&#x2039;', C['VERG_LT'], size=11)
        out += text(22, 19, title, C['CREAM'], size=13, bold=True)
    else:
        out += text(10, 19, title, C['CREAM'], size=13, bold=True)
    return out

def scrollbar(sel, count):
    """4px scrollbar a destra"""
    out = rect(CONTENT_W, HDR, SCROLL_W, H-HDR, C['SURFACE'])
    if count > VIS:
        th_h = max(20, (H-HDR)*VIS//count)
        th_y = HDR + (H-HDR-th_h)*sel//(count-1) if count>1 else HDR
        out += rect(CONTENT_W, th_y, SCROLL_W, th_h, C['SCROLLBAR'])
    else:
        out += rect(CONTENT_W, HDR, SCROLL_W, H-HDR, C['SCROLLBAR'])
    return out

def menu_row(pos, label, value='', selected=False, has_children=False, total_rows=0, idx=0):
    """Disegna una riga menu alla posizione visiva pos (0..5)"""
    ry = HDR + pos * ROW_H
    # sfondo alternato
    if selected:
        bg = C['VERGUS']
    elif pos % 2 == 0:
        bg = C['BG']
    else:
        bg = C['SURFACE']
    out = rect(0, ry, CONTENT_W, ROW_H-1, bg)
    if selected:
        out += rect(0, ry, 3, ROW_H-1, C['VERG_LT'])
    # label
    lbl_color = C['CREAM'] if selected else C['TEXT']
    out += text(30, ry+15, label, lbl_color, size=12, bold=True)
    # valore
    if value:
        val_color = C['CREAM_DIM'] if selected else C['SUB']
        out += text(30, ry+30, value, val_color, size=10)
    # freccia figli
    if has_children:
        arr_color = C['CREAM'] if selected else C['VERG_LT']
        out += text(CONTENT_W-2, ry+ROW_H//2+4, '&#x203A;', arr_color, anchor='end', size=13, bold=True)
    # divisore
    if not selected:
        out += line(26, ry+ROW_H-1, CONTENT_W, ry+ROW_H-1, C['BORDER'])
    return out

def counter(sel, count):
    return text(CONTENT_W-3, H-2, f'{sel+1}/{count}', C['MUTED'], anchor='end', size=10)

def bg_fill():
    return rect(0,0,W,H,C['BG'])

# ─────────────────────────────────────────────
# Funzione wrapper: genera SVG completo per un menu
# rows = lista di (label, value, has_children)
# sel = indice riga selezionata (0-based)
# first_vis = prima riga visibile
# ─────────────────────────────────────────────
def menu_svg(aria, title, rows, sel=0, first_vis=0, back=True):
    count = len(rows)
    out = svg_open(aria)
    out += bg_fill()
    out += header(title, back=back)
    out += scrollbar(sel, count)
    for vi in range(VIS):
        idx = first_vis + vi
        if idx >= count:
            break
        lbl, val, has_ch = rows[idx]
        out += menu_row(vi, lbl, val, selected=(idx==sel), has_children=has_ch,
                        total_rows=count, idx=idx)
    out += counter(sel, count)
    out += svg_close()
    return out

# ─────────────────────────────────────────────
# Helper: figura HTML completa (screen + caption)
# ─────────────────────────────────────────────
def figure(svg, caption):
    return f'<figure class="screen-item">{svg}<figcaption>{caption}</figcaption></figure>\n'

def gallery(*figures):
    inner = ''.join(figures)
    return f'<div class="screen-gallery">{inner}</div>\n'

# ════════════════════════════════════════════════
# DEFINIZIONE DI TUTTI I MENU
# ════════════════════════════════════════════════

screens = {}

# ── ROOT (scroll fino a vedere Pulizia selezionata)
root_rows = [
    ('Porta',       '05:18 / 20:51', True),
    ('Cibo',        '07:30 · 8 slot', True),
    ('Acqua',       '08:00 · 8 slot', True),
    ('Pulizia',     '--:-- · disattivo', True),
    ('Termostati',  'set 8.0°C',     True),
    ('Orologio',    '06:42  23 Giu', False),
    ('Manuale',     '',              True),
    ('Sistema',     '',              True),
    ('Utilità',     '',              True),
    ('Guida rapida','',              True),
]

screens['root_pulizia'] = menu_svg(
    'Menu principale — Pulizia selezionata',
    'Menù', root_rows, sel=3, first_vis=0, back=False)

screens['root_manuale'] = menu_svg(
    'Menu principale — Manuale selezionato',
    'Menù', root_rows, sel=6, first_vis=0, back=False)

screens['root_sistema'] = menu_svg(
    'Menu principale — Sistema selezionato',
    'Menù', root_rows, sel=7, first_vis=1, back=False)

screens['root_utilita'] = menu_svg(
    'Menu principale — Utilità selezionato',
    'Menù', root_rows, sel=8, first_vis=2, back=False)

# ── PULIZIA (8 slot, solo ora)
pulizia_rows = [(f'Slot {i+1}', '--:--' if i>0 else '09:00', True) for i in range(8)]
screens['menu_pulizia'] = menu_svg('Sottomenù Pulizia', 'Pulizia', pulizia_rows, sel=0, back=True)

# ── MANUALE (10 voci, toggle on/off)
manuale_rows = [
    ('Cibo man',       'OFF', False),
    ('Acqua man',      'OFF', False),
    ('Riscaldatore',   'OFF', False),
    ('Termo ESP32',    'OFF', False),
    ('Campana man',    'OFF', False),
    ('Aux man',        'OFF', False),
    ('Attiva porta',   'OFF', False),
    ('Ctrl porta',     'OFF', False),
    ('Attiva pulizia', 'OFF', False),
    ('Ctrl pulizia',   'OFF', False),
]
screens['menu_manuale'] = menu_svg('Sottomenù Manuale', 'Manuale', manuale_rows, sel=0, back=True)
# seconda pagina
screens['menu_manuale_p2'] = menu_svg('Sottomenù Manuale pg2', 'Manuale', manuale_rows, sel=6, first_vis=4, back=True)

# ── SISTEMA (12 voci, 2 pagine)
sistema_rows = [
    ('Slot cibo',     '3',          False),
    ('Slot acqua',    '3',          False),
    ('Slot pulizia',  '1',          False),
    ('Tipo orari',    'Astro',      False),
    ('Rit chiusura',  '10 min',     False),
    ('DST',           'ON',         False),
    ('UTC',           'UTC +1.0',   False),
    ('Lat',           '45.7845°',   False),
    ('Lon',           '8.4123°',    False),
    ('Sleep disp',    '5 min',      False),
    ('Lingua',        'Italiano',   False),
    ('Inv relè',      '',           True),
]
screens['menu_sistema'] = menu_svg('Sottomenù Sistema', 'Sistema', sistema_rows, sel=0, back=True)
screens['menu_sistema_p2'] = menu_svg('Sottomenù Sistema pg2', 'Sistema', sistema_rows, sel=9, first_vis=6, back=True)

# ── UTILITÀ (8 voci — con Bilancia)
utilita_rows = [
    ('Campana',       '',  True),
    ('Relè aux',      '',  True),
    ('Ctrl micro',    '',  True),
    ('Ctrl livello',  '',  True),
    ('Ctrl pulizia',  '',  True),
    ('Bilancia',      '',  True),
    ('Notifiche WiFi','',  True),
    ('Home Assist.',  '',  True),
]
screens['menu_utilita'] = menu_svg('Sottomenù Utilità', 'Utilità', utilita_rows, sel=0, back=True)

# ── BILANCIA UOVA (9 voci)
bilancia_rows = [
    ('Abilitata',     'ON',    False),
    ('Tara ora',      '',      False),
    ('Peso live',     '0 g / 0 uova', False),
    ('Soglia gallina','500 g', False),
    ('Fattore',       '420.0', False),
    ('Min uovo g',    '35 g',  False),
    ('Max uovo g',    '150 g', False),
    ('Peso/uovo g',   '60 g',  False),
    ('Debounce s',    '9 s',   False),
]
screens['menu_bilancia'] = menu_svg('Sottomenù Bilancia', 'Bilancia', bilancia_rows, sel=0, back=True)

# ── CAMPANA
campana_rows = [
    ('Abilitata',  'OFF',   False),
    ('Ant. min',   '0 min', False),
    ('Ant. sec',   '0 s',   False),
    ('Durata',     '5 s',   False),
]
screens['menu_campana'] = menu_svg('Sottomenù Campana', 'Campana', campana_rows, sel=0, back=True)

# ── RELÈ AUX (8 eventi)
aux_rows = [(f'Evento {i+1}', '--:-- / --:--', True) for i in range(8)]
aux_rows[0] = ('Evento 1', '08:00 / 22:00', True)
screens['menu_aux'] = menu_svg('Sottomenù Relè aux', 'Relè aux', aux_rows, sel=0, back=True)

# ── CTRL MICRO PORTA
micro_rows = [
    ('Abilitato',  'ON',   False),
    ('Timeout',    '30 s', False),
    ('Diagnostica','',     False),
    ('Test porta', '',     False),
]
screens['menu_micro'] = menu_svg('Sottomenù Ctrl micro', 'Ctrl micro', micro_rows, sel=0, back=True)

# ── CTRL LIVELLO
livello_rows = [
    ('Abilitato',  'ON',  False),
    ('Diagnostica','',    False),
    ('Notif TG',   'ON',  False),
]
screens['menu_livello'] = menu_svg('Sottomenù Ctrl livello', 'Ctrl livello', livello_rows, sel=0, back=True)

# ── CTRL PULIZIA (con microinterruttori)
ctrl_pul_rows = [
    ('Abilitata',    'ON',   False),
    ('Timeout',      '60 s', False),
    ('Diagnostica',  '',     False),
    ('Test pulizia', '',     False),
]
screens['menu_ctrl_pulizia'] = menu_svg('Sottomenù Ctrl pulizia', 'Ctrl pulizia', ctrl_pul_rows, sel=0, back=True)

# ── NOTIFICHE WIFI
wifi_rows = [
    ('Config AP',      '',          False),
    ('SSID',           'ElettroCfg',False),
    ('Password',       '********',  False),
    ('IP AP',          '192.168.4.1',False),
    ('Stato STA',      'Connesso',  False),
    ('IP STA',         '192.168.1.42',False),
    ('Cred Telegram',  'OK',        False),
    ('Test Telegram',  '',          False),
    ('Tipi notif',     '',          True),
    ('Reset WiFi/AP',  '',          False),
    ('Reset Telegram', '',          False),
]
screens['menu_wifi'] = menu_svg('Sottomenù Notifiche WiFi', 'WiFi / Telegram', wifi_rows, sel=0, back=True)
screens['menu_wifi_p2'] = menu_svg('Sottomenù Notifiche WiFi pg2', 'WiFi / Telegram', wifi_rows, sel=8, first_vis=3, back=True)

# ── TIPI NOTIFICA
notif_rows = [
    ('Cibo',         'ON',  False),
    ('Acqua',        'ON',  False),
    ('Porta ON',     'ON',  False),
    ('Porta OFF',    'ON',  False),
    ('Aux ON',       'OFF', False),
    ('Aux OFF',      'OFF', False),
    ('Antigelo ON',  'ON',  False),
    ('Antigelo OFF', 'ON',  False),
    ('Volt',         'ON',  False),
    ('Soglia Volt',  '11.5V',False),
]
screens['menu_notif'] = menu_svg('Sottomenù Tipi notifica', 'Tipi notif', notif_rows, sel=0, back=True)

# ── HOME ASSISTANT
ha_rows = [
    ('Abilitata',  'ON',              False),
    ('Stato',      'Connesso',        False),
    ('Broker',     '192.168.1.10',    False),
    ('Republish',  '',                False),
]
screens['menu_ha'] = menu_svg('Sottomenù Home Assistant', 'Home Assist.', ha_rows, sel=0, back=True)

# ── INV RELÈ (dentro Sistema)
inv_rows = [
    ('Cibo',       'NO', False),
    ('Acqua',      'NO', False),
    ('Riscald.',   'NO', False),
    ('Campana',    'NO', False),
    ('Aux',        'NO', False),
    ('Termo ESP32','NO', False),
    ('Pul motore', 'NO', False),
    ('Pul ctrl',   'NO', False),
    ('Porta att',  'NO', False),
    ('Porta ctrl', 'NO', False),
]
screens['menu_inv_rele'] = menu_svg('Sottomenù Inversione relè', 'Inv relè', inv_rows, sel=0, back=True)

# ════════════════════════════════════
# OUTPUT: stampa tutto
# ════════════════════════════════════
for name, svg in screens.items():
    print(f'=== {name} ===')
    print(svg)
    print()

