#!/usr/bin/env python3
"""Genera las ilustraciones SVG del sitio en public/img.

Solo usa la biblioteca estándar. Ejecutar al cambiar colores o dibujos:
    python scripts/generar_ilustraciones.py
"""

from __future__ import annotations

import math
from pathlib import Path

DESTINO = Path(__file__).resolve().parent.parent / "public" / "img"

HOJA = "#2f6b47"
HOJA_OSCURA = "#1f4d36"
HOJA_CLARA = "#6a9a5b"
TALLO = "#4f7a45"
TRONCO = "#7a5236"
BARRO = "#b85c38"
BARRO_OSCURO = "#97472a"
TIERRA = "#4a3526"
CREMA = "#faf7f0"
AMARILLO = "#e3b23c"
MORADO = "#7b5ea7"
FUCSIA = "#c2367a"


def elipse(x, y, rx, ry, color, giro=0):
    transformacion = f' transform="rotate({giro:.0f} {x:.1f} {y:.1f})"' if giro else ""
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx}" ry="{ry}" fill="{color}"{transformacion}/>'


def circulo(x, y, r, color):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}"/>'


def trazo(d, color, grosor=4):
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{grosor}" '
            'stroke-linecap="round" stroke-linejoin="round"/>')


def forma(d, color):
    return f'<path d="{d}" fill="{color}"/>'


def rect(x, y, ancho, alto, color, radio=0):
    return f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" rx="{radio}" fill="{color}"/>'


def maceta(x=200, y=205, ancho=110, alto=75, color=BARRO, borde=BARRO_OSCURO):
    izq, der = x - ancho / 2, x + ancho / 2
    base = ancho * 0.16
    return (
        forma(f"M{izq} {y} L{der} {y} L{der - base} {y + alto} L{izq + base} {y + alto} Z", color)
        + rect(izq - 6, y - 12, ancho + 12, 16, borde, 4)
    )


def hojas_en_rama(x0, y0, x1, y1, n, largo, color):
    """Pares de hojas repartidas a lo largo de un tallo recto."""
    partes = [trazo(f"M{x0} {y0} L{x1} {y1}", TALLO, 3)]
    angulo = math.degrees(math.atan2(y1 - y0, x1 - x0))
    for i in range(1, n + 1):
        t = i / (n + 0.5)
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        for lado in (-50, 50):
            rad = math.radians(angulo + lado)
            partes.append(elipse(x + math.cos(rad) * largo, y + math.sin(rad) * largo,
                                 largo, largo * 0.4, color, angulo + lado))
    return "".join(partes)


def copa(x, y, puntos, radio, colores):
    return "".join(circulo(x + dx, y + dy, radio, colores[i % len(colores)])
                   for i, (dx, dy) in enumerate(puntos))


# --- Plantas -----------------------------------------------------------------

def monstera():
    partes = []
    for x, y, giro, color in ((140, 115, -35, HOJA_OSCURA), (262, 110, 38, HOJA),
                              (200, 78, 0, HOJA_CLARA), (152, 180, -70, HOJA),
                              (254, 176, 68, HOJA_OSCURA)):
        partes.append(trazo(f"M200 205 Q200 {y + 30} {x} {y}", TALLO, 5))
        cortes = "".join(trazo(f"M{x + lado * 44} {y + dy} L{x + lado * 14} {y + dy - 6}", CREMA, 6)
                         for lado in (-1, 1) for dy in (-6, 16))
        partes.append(f'<g transform="rotate({giro} {x} {y})">'
                      + elipse(x, y, 40, 48, color) + cortes
                      + trazo(f"M{x} {y - 36} L{x} {y + 40}", "#a9c79a", 2) + "</g>")
    return "".join(partes) + maceta()


def sansevieria():
    partes = []
    for base, punta, alto in ((178, 135, 90), (190, 168, 45), (205, 205, 28),
                              (216, 246, 55), (225, 272, 100), (196, 192, 75)):
        d = (f"M{base - 14} 208 Q{(base + punta) / 2 - 26} {(208 + alto) / 2} {punta} {alto} "
             f"Q{(base + punta) / 2 + 24} {(208 + alto) / 2} {base + 14} 208 Z")
        partes.append(f'<path d="{d}" fill="{HOJA}" stroke="{AMARILLO}" stroke-width="4"/>')
    return "".join(partes) + maceta()


def potus():
    partes = [trazo("M200 28 L145 115 M200 28 L255 115 M200 28 L200 105", TRONCO, 3),
              circulo(200, 28, 6, TRONCO)]
    guias = (((158, 118), (90, 130), (96, 252)), ((178, 120), (140, 170), (160, 262)),
             ((228, 120), (292, 120), (300, 235)), ((215, 125), (250, 195), (232, 272)),
             ((196, 118), (196, 92), (140, 82)), ((204, 118), (210, 88), (268, 92)))
    for p0, p1, p2 in guias:
        partes.append(trazo(f"M{p0[0]} {p0[1]} Q{p1[0]} {p1[1]} {p2[0]} {p2[1]}", TALLO, 3))
        for i in range(1, 6):
            t = i / 5
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            partes.append(elipse(x + (8 if i % 2 else -8), y, 13, 9,
                                 HOJA if i % 2 else HOJA_CLARA, 35 if i % 2 else -35))
    return "".join(partes) + maceta(200, 122, 100, 62)


def espatifilo():
    partes = []
    for x, y, giro in ((135, 145, -45), (265, 145, 45), (158, 115, -25),
                       (245, 112, 25), (172, 168, -55), (232, 168, 55)):
        partes.append(trazo(f"M200 205 L{x} {y}", TALLO, 4))
        partes.append(elipse(x, y, 20, 46, HOJA_OSCURA if giro % 2 else HOJA, giro))
    for x, y, giro in ((178, 72, -18), (232, 62, 16), (204, 102, 0)):
        partes.append(trazo(f"M200 205 Q198 150 {x} {y + 18}", TALLO, 3))
        partes.append(f'<g transform="rotate({giro} {x} {y})">'
                      + forma(f"M{x} {y - 30} Q{x + 28} {y} {x} {y + 24} Q{x - 28} {y} {x} {y - 30}Z",
                              "#ffffff")
                      + elipse(x, y + 2, 4, 15, AMARILLO) + "</g>")
    return "".join(partes) + maceta()


def lavanda():
    partes = []
    for i, x in enumerate(range(130, 280, 18)):
        y = 70 + (i % 3) * 22 + abs(x - 200) * 0.25
        partes.append(trazo(f"M{200 + (x - 200) * 0.25} 208 Q{x} 160 {x} {y}", TALLO, 3))
        for j in range(6):
            partes.append(elipse(x + (-4 if j % 2 else 4), y + j * 9, 5, 8,
                                 MORADO if j % 3 else "#9a7fc4"))
    for x, giro in ((160, -40), (178, -20), (222, 20), (240, 40), (200, 0)):
        partes.append(elipse(x, 182, 5, 28, HOJA_CLARA, giro))
    return "".join(partes) + maceta()


def buganvilla():
    partes = [trazo(f"M{x} 40 L{x} 215", TRONCO, 4) for x in (130, 200, 270)]
    partes += [trazo(f"M115 {y} L285 {y}", TRONCO, 4) for y in (75, 130, 180)]
    partes.append(trazo("M200 208 C150 180 250 130 180 95 C140 70 220 55 250 62", TALLO, 5))
    grupos = ((135, 82), (190, 60), (250, 70), (268, 125), (212, 112),
              (155, 140), (232, 165), (122, 190), (178, 180))
    for i, (x, y) in enumerate(grupos):
        partes.append(elipse(x - 18, y + 12, 14, 8, HOJA, -30))
        partes.append(elipse(x + 20, y + 8, 14, 8, HOJA_CLARA, 30))
        for giro in (0, 120, 240):
            rad = math.radians(giro + i * 20)
            partes.append(elipse(x + math.cos(rad) * 10, y + math.sin(rad) * 10, 13, 9,
                                 FUCSIA if i % 3 else "#d9549a", giro + i * 20))
        partes.append(circulo(x, y, 3.5, "#fff3c4"))
    return "".join(partes) + maceta()


def suculentas():
    partes = []
    # Roseta
    for radio, color, n in ((36, HOJA_CLARA, 9), (24, "#8db580", 7), (12, "#b3cfa0", 5)):
        for i in range(n):
            ang = 180 + i * 180 / (n - 1)
            rad = math.radians(ang)
            partes.append(elipse(95 + math.cos(rad) * radio * 0.7,
                                 205 + math.sin(rad) * radio * 0.8, radio * 0.55, 9, color, ang))
    # Columnar
    partes.append(rect(184, 105, 32, 110, HOJA, 16))
    partes.append(trazo("M184 170 H168 V138 M216 155 H232 V122", HOJA, 17))
    partes.append(trazo("M200 118 V205", HOJA_CLARA, 3))
    # Carnosa
    for dx, dy, giro in ((-22, 0, -45), (22, 0, 45), (0, -18, 0), (-12, -34, -25),
                         (12, -36, 25), (0, 2, 90)):
        partes.append(elipse(305 + dx, 192 + dy, 12, 21, "#5f9184", giro))
    for x, color in ((95, BARRO), (200, "#d08a62"), (305, BARRO_OSCURO)):
        partes.append(maceta(x, 215, 72, 55, color))
    return "".join(partes)


def molle():
    partes = [trazo("M200 215 C195 170 208 140 200 95", TRONCO, 10),
              trazo("M200 130 Q160 100 138 92 M202 112 Q245 80 268 90 M200 98 Q200 70 205 55",
                    TRONCO, 5)]
    for x0, y0, x1, y1 in ((138, 92, 98, 178), (160, 98, 138, 192), (268, 90, 308, 175),
                           (242, 88, 262, 185), (205, 55, 160, 130), (205, 55, 250, 135),
                           (138, 92, 108, 112), (268, 90, 302, 110)):
        partes.append(hojas_en_rama(x0, y0, x1, y1, 7, 9, HOJA_CLARA if x0 % 2 else HOJA))
    for x, y in ((120, 150), (282, 148), (176, 142), (236, 128)):
        partes.append(copa(x, y, [(0, 0), (7, 5), (-5, 7), (2, 12), (-1, 19)], 4, ["#d9667a"]))
    return "".join(partes) + maceta(200, 215, 90, 65)


def tara():
    partes = [trazo("M200 215 L200 125 M200 160 Q165 140 145 105 M200 145 Q240 125 260 92",
                    TRONCO, 8)]
    for x0, y0, x1, y1 in ((145, 105, 100, 80), (145, 105, 140, 48), (200, 125, 195, 55),
                           (260, 92, 305, 75), (260, 92, 245, 40), (170, 140, 105, 140),
                           (232, 128, 300, 135)):
        partes.append(hojas_en_rama(x0, y0, x1, y1, 4, 11, HOJA))
    for x, y in ((140, 45), (250, 38), (196, 52)):
        partes.append(copa(x, y, [(0, 0), (10, 6), (-9, 7), (1, 13), (6, -9)], 6, [AMARILLO]))
    for x, y in ((118, 150), (130, 154), (278, 146), (290, 142)):
        partes.append(elipse(x, y + 12, 6, 20, "#b0543f", 8))
    return "".join(partes) + maceta(200, 215, 90, 65)


def _frutal(fruto, forma_hoja_larga=False):
    partes = [trazo("M200 215 L200 140 M200 170 L165 135 M200 158 L238 122", TRONCO, 9)]
    puntos = [(-55, 10), (-30, -28), (10, -42), (48, -22), (62, 14), (28, 22),
              (-18, 20), (4, -8), (-44, -12), (36, 2)]
    if forma_hoja_larga:
        for i, (dx, dy) in enumerate(puntos):
            for giro in (-55, 0, 55):
                partes.append(elipse(200 + dx + giro * 0.3, 112 + dy, 10, 28,
                                     (HOJA, HOJA_OSCURA, HOJA_CLARA)[i % 3], giro))
    else:
        partes.append(copa(200, 112, puntos, 31, [HOJA, HOJA_OSCURA, HOJA_CLARA]))
    return "".join(partes) + fruto + maceta(200, 215, 100, 65)


def limon():
    posiciones = ((158, 100), (215, 72), (252, 125), (180, 138), (228, 112), (150, 132))
    return _frutal("".join(elipse(x, y, 11, 10, "#b7c93b", 20) for x, y in posiciones))


def lucuma():
    fruto = (circulo(240, 160, 22, "#8a9a3f") + circulo(233, 153, 6, "#a9b65a")
             + trazo("M240 138 L236 122", TRONCO, 4))
    return _frutal(fruto, forma_hoja_larga=True)


def aromaticas():
    partes = [hojas_en_rama(105, 200, 100, 105, 4, 14, HOJA_CLARA)]
    for dx, dy in ((-16, 30), (10, 0), (-6, -34), (18, -52), (-20, -10), (22, 40), (2, 48)):
        partes.append(circulo(168 + dx, 148 + dy, 15, HOJA if dy % 4 else "#437f4f"))
    partes.append(trazo("M168 200 V100", TALLO))
    partes.append(hojas_en_rama(228, 200, 235, 110, 6, 10, "#4d8c57"))
    for x, y in ((278, 82), (300, 108), (262, 112)):
        partes.append(hojas_en_rama(282, 202, x, y, 7, 8, HOJA_OSCURA))
    partes.append(rect(70, 195, 260, 70, BARRO, 8) + rect(62, 188, 276, 18, BARRO_OSCURO, 5))
    return "".join(partes)


def almacigos():
    partes = [forma("M55 150 H345 L370 255 H30 Z", "#3d463f")]
    for fila, (y, escala) in enumerate(((168, 0.8), (200, 0.92), (235, 1.05))):
        for col in range(4):
            x = 200 + (col - 1.5) * (66 + fila * 7)
            alto = 24 + ((col + fila) % 3) * 8
            partes.append(elipse(x, y + 4, 27 * escala, 12 * escala, TIERRA))
            partes.append(trazo(f"M{x} {y + 4} V{y - alto}", TALLO, 3))
            partes.append(elipse(x - 11, y - alto, 13, 7, HOJA_CLARA, 25))
            partes.append(elipse(x + 11, y - alto - 2, 13, 7, HOJA, -25))
    return "".join(partes)


def maceta_barro():
    return (elipse(200, 252, 105, 17, BARRO_OSCURO) + elipse(200, 246, 105, 15, BARRO)
            + maceta(200, 105, 170, 138)
            + trazo("M135 135 H265 M142 150 H258", "#d98a63", 4)
            + elipse(200, 93, 82, 5, "#7c3a22"))


def humus():
    return (
        forma("M110 80 H235 L255 255 Q172 270 90 255 Z", "#c9a672")
        + rect(108, 62, 129, 24, "#a98655", 5)
        + rect(118, 125, 110, 85, CREMA, 8)
        + trazo("M173 190 V152", TALLO, 4)
        + elipse(158, 153, 18, 10, HOJA_CLARA, 30) + elipse(188, 148, 18, 10, HOJA, -30)
        + trazo("M143 197 H203", TIERRA, 5)
        + forma("M235 262 Q292 170 350 262 Z", TIERRA)
        + "".join(circulo(x, y, 4, "#6b4d37") for x, y in
                  ((280, 245), (300, 225), (318, 248), (292, 258), (262, 255)))
        + trazo("M293 215 q10 -14 20 -2 t20 -4", "#c97b6a", 6)
    )


def plano_jardin():
    return (
        '<g transform="rotate(-3 200 150)">'
        + rect(70, 45, 260, 210, "#ffffff", 8)
        + rect(88, 63, 224, 174, "#e4eedc", 4)
        + trazo("M88 190 C150 185 150 110 220 108 S290 90 312 80", "#d9c7a0", 24)
        + copa(130, 105, [(0, 0), (18, 8), (4, 20)], 19, [HOJA, HOJA_CLARA])
        + copa(262, 185, [(0, 0), (22, -4), (10, 18)], 20, [HOJA_OSCURA, HOJA])
        + rect(105, 205, 80, 18, BARRO, 4)
        + "".join(circulo(x, 214, 6, MORADO) for x in range(115, 185, 15))
        + elipse(250, 135, 24, 15, "#8fbccc")
        + "</g>"
        + trazo("M300 262 L355 195", AMARILLO, 14)
        + trazo("M295 269 L302 260", TIERRA, 7)
    )


def mantenimiento():
    return (
        copa(115, 170, [(0, 0), (35, -25), (60, 15), (22, 32), (-25, 28), (10, -42)], 33,
             [HOJA, HOJA_CLARA, HOJA_OSCURA])
        + rect(40, 232, 175, 10, TIERRA, 5)
        + trazo("M262 62 L322 150 M322 62 L262 150", "#6f7d78", 13)
        + circulo(292, 106, 7, CREMA)
        + trazo("M262 150 c-34 22 -22 62 4 44 c20 -14 8 -34 -4 -44 "
                "M322 150 c34 22 22 62 -4 44 c-20 -14 -8 -34 4 -44", BARRO, 10)
        + rect(255, 215, 78, 50, "#5f9184", 10)
        + trazo("M333 228 q36 4 0 30 M255 238 L218 208", "#5f9184", 9)
    )


def trasplante():
    return (
        forma("M95 92 H175 L162 160 H108 Z", TIERRA)
        + trazo("M112 160 q-6 14 2 24 M135 160 q4 16 -4 28 M155 160 q10 12 4 22", "#c9a672", 3)
        + hojas_en_rama(135, 95, 105, 35, 3, 17, HOJA)
        + hojas_en_rama(135, 95, 170, 38, 3, 17, HOJA_CLARA)
        + trazo("M195 95 q70 -30 82 60", AMARILLO, 8)
        + trazo("M258 142 L277 160 L292 138", AMARILLO, 8)
        + maceta(275, 195, 120, 75)
        + elipse(275, 183, 56, 6, TIERRA)
    )


PRODUCTOS = {
    "monstera-deliciosa": monstera, "sansevieria": sansevieria, "potus": potus,
    "espatifilo": espatifilo, "lavanda": lavanda, "buganvilla": buganvilla,
    "trio-suculentas": suculentas, "molle": molle, "tara": tara,
    "limon-sutil": limon, "lucuma": lucuma, "kit-aromaticas": aromaticas,
    "almacigos": almacigos, "maceta-barro": maceta_barro, "humus-lombriz": humus,
    "diseno-jardines": plano_jardin, "mantenimiento": mantenimiento,
    "trasplante": trasplante,
}
FONDOS = ("#e6efdf", "#f4e8da", "#e2ecea", "#f1ecd8")


# --- Composiciones -----------------------------------------------------------

def svg(ancho, alto, contenido):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" '
            f'width="{ancho}" height="{alto}">{contenido}</svg>\n')


def colocar(dibujo, x, y, escala):
    return f'<g transform="translate({x} {y}) scale({escala})">{dibujo()}</g>'


def portada():
    return svg(800, 640, (
        rect(0, 0, 800, 640, "#e6efdf", 24)
        + circulo(620, 150, 85, "#f2d98d")
        + elipse(400, 660, 560, 130, "#d3c3a0")
        + colocar(molle, 150, 40, 1.65)
        + colocar(sansevieria, -40, 300, 1.05)
        + colocar(lavanda, 450, 310, 1.02)
        + colocar(espatifilo, 215, 345, 0.9)
    ))


def vivero():
    arcos = "".join(trazo(f"M{x} 330 V170 Q{x + 90} 40 {x + 180} 170 V330", "#8a9a8f", 7)
                    for x in (40, 220, 400, 580))
    return svg(800, 500, (
        rect(0, 0, 800, 500, "#e2ecea", 24)
        + arcos + trazo("M40 170 H760", "#8a9a8f", 5)
        + rect(0, 390, 800, 110, "#d3c3a0")
        + rect(40, 330, 720, 14, TRONCO, 4)
        + trazo("M80 344 V440 M400 344 V440 M720 344 V440", TRONCO, 12)
        + "".join(colocar(d, x, 155, 0.65) for d, x in
                  ((potus, 30), (monstera, 190), (suculentas, 350), (lavanda, 510)))
        + colocar(limon, -20, 260, 0.75) + colocar(sansevieria, 540, 270, 0.72)
    ))


def mapa():
    return svg(800, 450, (
        rect(0, 0, 800, 450, "#eef0e2", 24)
        + trazo("M-20 90 C200 60 380 150 820 100", "#a9cddb", 34)
        + trazo("M-20 300 H820", "#ffffff", 30) + trazo("M250 -20 V470", "#ffffff", 22)
        + trazo("M560 300 L650 470", "#ffffff", 18)
        + "".join(rect(x, y, w, h, "#d6e2c8", 8) for x, y, w, h in
                  ((40, 160, 160, 100), (300, 340, 200, 75), (620, 160, 130, 100), (50, 345, 150, 70)))
        + forma("M430 285 C385 230 375 215 375 192 A55 55 0 0 1 485 192 "
                "C485 215 475 230 430 285 Z", BARRO)
        + circulo(430, 192, 24, CREMA)
        + elipse(421, 192, 12, 7, HOJA, 35) + elipse(439, 188, 12, 7, HOJA_CLARA, -35)
        + '<g font-family="system-ui, sans-serif" font-size="19" fill="#33453a">'
        + '<text x="500" y="195" font-weight="700">Molle &amp; Tara</text>'
        + '<text x="40" y="291">Av. Los Huarangos</text>'
        + '<text x="600" y="75">Río Lurín</text></g>'
    ))


def logo():
    return svg(64, 64, (
        circulo(32, 32, 32, HOJA_OSCURA)
        + trazo("M32 52 V28", CREMA, 4)
        + elipse(22, 27, 13, 7, "#a9c79a", 35)
        + elipse(42, 21, 13, 7, AMARILLO, -35)
    ))


def tarjeta_social():
    """Base para og-portada.png (1200x630)."""
    return svg(1200, 630, (
        rect(0, 0, 1200, 630, HOJA_OSCURA)
        + circulo(930, 315, 245, "#e6efdf")
        + colocar(molle, 692, 85, 1.22) + colocar(lavanda, 862, 262, 0.82)
        + '<g font-family="Georgia, serif" fill="#faf7f0">'
        + '<text x="80" y="265" font-size="82" font-weight="700">Molle &amp; Tara</text>'
        + '<text x="82" y="345" font-size="38">Vivero en Pachacámac, Lima</text></g>'
        + '<text x="82" y="425" font-family="Arial, sans-serif" font-size="28" fill="#cfe0c4">'
          'Plantas, frutales, huerto y jardinería</text>'
    ))


def guardar(ruta: Path, contenido: str) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8", newline="\n")


def main() -> None:
    for i, (nombre, dibujo) in enumerate(PRODUCTOS.items()):
        fondo = rect(0, 0, 400, 300, FONDOS[i % len(FONDOS)])
        sombra = elipse(200, 276, 150, 9, "#00000014")
        guardar(DESTINO / "productos" / f"{nombre}.svg", svg(400, 300, fondo + sombra + dibujo()))
    guardar(DESTINO / "portada.svg", portada())
    guardar(DESTINO / "vivero.svg", vivero())
    guardar(DESTINO / "mapa.svg", mapa())
    guardar(DESTINO / "og-portada.svg", tarjeta_social())
    guardar(DESTINO.parent / "favicon.svg", logo())
    print(f"Ilustraciones generadas en {DESTINO}")


if __name__ == "__main__":
    main()
