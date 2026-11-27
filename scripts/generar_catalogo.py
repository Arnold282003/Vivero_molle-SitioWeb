#!/usr/bin/env python3
"""Valida data/productos.csv y genera el JSON del catálogo que consume Astro.

Uso:
    python scripts/generar_catalogo.py
    python scripts/generar_catalogo.py --entrada otro.csv --salida otro.json
    python scripts/generar_catalogo.py --solo-validar
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA = RAIZ / "data" / "productos.csv"
SALIDA = RAIZ / "src" / "data" / "catalogo.json"
IMAGENES = RAIZ / "public" / "img" / "productos"

COLUMNAS = (
    "id", "nombre", "categoria", "tipo", "precio", "unidad", "descripcion",
    "luz", "riego", "disponible", "destacado", "imagen", "alt",
)
OPCIONALES = {"luz", "riego"}
# El orden de esta tupla es el orden de los filtros en la web.
CATEGORIAS = (
    "Plantas de interior",
    "Plantas de exterior",
    "Árboles y frutales",
    "Huerto en casa",
    "Macetas y sustratos",
    "Servicios",
)
TIPOS = ("producto", "servicio")
LONGITUDES = {
    "nombre": (3, 60),
    "unidad": (3, 40),
    "descripcion": (20, 220),
    "alt": (10, 140),
}
PATRON_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
PATRON_PRECIO = re.compile(r"\d{1,5}(?:\.\d{1,2})?")
PATRON_IMAGEN = re.compile(r"[a-z0-9-]+\.(?:svg|webp|png|jpg)")


class ErrorCatalogo(Exception):
    """Reúne todos los problemas encontrados en el CSV."""

    def __init__(self, errores: list[str]):
        super().__init__("\n".join(errores))
        self.errores = errores


def leer_booleano(valor: str) -> bool | None:
    return {"si": True, "sí": True, "no": False}.get(valor.lower())


def validar_fila(fila: dict[str, str], carpeta_imagenes: Path) -> list[str]:
    errores = []

    for columna in COLUMNAS:
        if columna not in OPCIONALES and not fila[columna]:
            errores.append(f"la columna '{columna}' está vacía")
    if errores:
        return errores

    if not PATRON_ID.fullmatch(fila["id"]):
        errores.append(f"id '{fila['id']}' solo admite minúsculas, números y guiones")
    if fila["categoria"] not in CATEGORIAS:
        errores.append(f"categoría desconocida: '{fila['categoria']}'")
    if fila["tipo"] not in TIPOS:
        errores.append(f"tipo debe ser {' o '.join(TIPOS)}")
    elif (fila["tipo"] == "servicio") != (fila["categoria"] == "Servicios"):
        errores.append("el tipo 'servicio' va solo en la categoría 'Servicios'")

    for columna, (minimo, maximo) in LONGITUDES.items():
        if not minimo <= len(fila[columna]) <= maximo:
            errores.append(f"'{columna}' debe tener entre {minimo} y {maximo} caracteres")

    for columna, valor in fila.items():
        if "<" in valor or ">" in valor:
            errores.append(f"'{columna}' no puede contener etiquetas HTML")

    try:
        if not PATRON_PRECIO.fullmatch(fila["precio"]) or Decimal(fila["precio"]) <= 0:
            raise InvalidOperation
    except InvalidOperation:
        errores.append(f"precio inválido: '{fila['precio']}' (ejemplo válido: 35.50)")

    for columna in ("disponible", "destacado"):
        if leer_booleano(fila[columna]) is None:
            errores.append(f"'{columna}' debe ser si o no")

    if not PATRON_IMAGEN.fullmatch(fila["imagen"]):
        errores.append(f"nombre de imagen inválido: '{fila['imagen']}'")
    elif not (carpeta_imagenes / fila["imagen"]).is_file():
        errores.append(f"no existe la imagen '{fila['imagen']}'")

    return errores


def convertir(fila: dict[str, str]) -> dict:
    return {
        **fila,
        "precio": float(Decimal(fila["precio"])),
        "disponible": leer_booleano(fila["disponible"]),
        "destacado": leer_booleano(fila["destacado"]),
    }


def cargar_catalogo(ruta: Path, carpeta_imagenes: Path = IMAGENES) -> list[dict]:
    """Devuelve los ítems del CSV o lanza ErrorCatalogo con todos los fallos."""
    errores: list[str] = []
    items: list[dict] = []
    ids: dict[str, int] = {}

    try:
        # utf-8-sig tolera el BOM que agrega Excel.
        with ruta.open(encoding="utf-8-sig", newline="") as archivo:
            lector = csv.DictReader(archivo, strict=True)
            encabezado = [c.strip() for c in lector.fieldnames or []]
            if sorted(encabezado) != sorted(COLUMNAS):
                faltan = [c for c in COLUMNAS if c not in encabezado]
                sobran = [c for c in encabezado if c not in COLUMNAS]
                raise ErrorCatalogo([
                    "encabezado incorrecto. "
                    f"Faltan: {faltan or 'ninguna'}. Sobran: {sobran or 'ninguna'}."
                ])
            lector.fieldnames = encabezado

            for cruda in lector:
                linea = lector.line_num
                if None in cruda or None in cruda.values():
                    errores.append(f"línea {linea}: número de columnas incorrecto")
                    continue
                fila = {c: cruda[c].strip() for c in COLUMNAS}
                problemas = validar_fila(fila, carpeta_imagenes)
                if fila["id"] in ids:
                    problemas.append(f"id repetido (ya usado en la línea {ids[fila['id']]})")
                ids.setdefault(fila["id"], linea)

                if problemas:
                    errores.extend(f"línea {linea}: {p}" for p in problemas)
                else:
                    items.append(convertir(fila))
    except FileNotFoundError:
        raise ErrorCatalogo([f"no se encontró el archivo {ruta}"]) from None
    except UnicodeDecodeError:
        raise ErrorCatalogo(["el CSV debe estar guardado en UTF-8"]) from None
    except csv.Error as error:
        raise ErrorCatalogo([f"CSV mal formado: {error}"]) from None

    if not errores and not items:
        errores.append("el CSV no contiene productos")
    if errores:
        raise ErrorCatalogo(errores)
    return items


def guardar_json(items: list[dict], ruta: Path) -> None:
    usadas = {item["categoria"] for item in items}
    contenido = {
        "categorias": [c for c in CATEGORIAS if c in usadas],
        "items": items,
    }
    ruta.parent.mkdir(parents=True, exist_ok=True)
    # Se escribe en un temporal para no dejar un JSON a medias.
    temporal = ruta.with_name(ruta.name + ".tmp")
    with temporal.open("w", encoding="utf-8", newline="\n") as archivo:
        json.dump(contenido, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")
    os.replace(temporal, ruta)


def main() -> int:
    analizador = argparse.ArgumentParser(description="Genera el catálogo en JSON.")
    analizador.add_argument("--entrada", type=Path, default=ENTRADA, help="CSV de origen")
    analizador.add_argument("--salida", type=Path, default=SALIDA, help="JSON de destino")
    analizador.add_argument("--solo-validar", action="store_true", help="no escribe el JSON")
    opciones = analizador.parse_args()

    # Evita errores de acentos en consolas de Windows.
    for flujo in (sys.stdout, sys.stderr):
        flujo.reconfigure(errors="replace")

    try:
        items = cargar_catalogo(opciones.entrada)
    except ErrorCatalogo as fallo:
        print(f"Se encontraron {len(fallo.errores)} error(es):", file=sys.stderr)
        for error in fallo.errores:
            print(f"  - {error}", file=sys.stderr)
        return 1

    if opciones.solo_validar:
        print(f"CSV válido: {len(items)} ítems.")
        return 0

    guardar_json(items, opciones.salida)
    print(f"Catálogo generado: {len(items)} ítems en {opciones.salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
