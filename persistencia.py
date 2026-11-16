"""Módulo de persistencia: lectura/escritura en archivo de texto plano."""
import os

SEP = "|"


def nueva_base():
    """Arreglos paralelos: la posición i describe un mismo expediente."""
    return {"codigos": [], "dnis": [], "nombres": [], "asuntos": [], "fechas": []}


def guardar(base, ruta):
    """Guarda cada expediente como una línea CODIGO|DNI|NOMBRE|ASUNTO|FECHA."""
    with open(ruta, "w", encoding="utf-8") as f:
        for i in range(len(base["codigos"])):
            campos = [base["codigos"][i], base["dnis"][i], base["nombres"][i],
                      base["asuntos"][i], base["fechas"][i]]
            f.write(SEP.join(campos) + "\n")


def cargar(ruta):
    """Carga el archivo; ignora líneas corruptas y devuelve (base, omitidas)."""
    base = nueva_base()
    omitidas = 0
    if not os.path.exists(ruta):
        return base, 0
    with open(ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.rstrip("\n")
            if linea == "":
                continue
            campos = linea.split(SEP)
            if len(campos) != 5:
                omitidas += 1
                continue
            for clave, valor in zip(base.keys(), campos):
                base[clave].append(valor)
    return base, omitidas
