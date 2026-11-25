"""Módulo de lógica de expedientes: registrar, buscar y ordenar."""
from validaciones import (es_dni_valido, es_fecha_valida, es_nombre_valido,
                          es_asunto_valido, normalizar_tipo)


def generar_codigo(base, anio):
    """Código correlativo EXP-AAAA-NNNN (toma el mayor número existente + 1)."""
    mayor = 0
    prefijo = "EXP-" + str(anio) + "-"
    for cod in base["codigos"]:
        if cod.startswith(prefijo) and cod[-4:].isdigit():
            mayor = max(mayor, int(cod[-4:]))
    return prefijo + str(mayor + 1).zfill(4)


def registrar(base, dni, nombre, tipo, asunto, fecha):
    """Valida y registra. Devuelve (ok, mensaje, codigo)."""
    dni, nombre, asunto, fecha = dni.strip(), nombre.strip(), asunto.strip(), fecha.strip()
    tipo = normalizar_tipo(tipo)
    if not es_dni_valido(dni):
        return False, "DNI inválido: deben ser 8 dígitos.", ""
    if not es_nombre_valido(nombre):
        return False, "Nombre inválido: mínimo dos palabras, solo letras.", ""
    if tipo == "":
        return False, "Tipo de trámite inexistente: elija uno del catálogo.", ""
    if not es_asunto_valido(asunto):
        return False, "Asunto inválido: 5 a 120 caracteres, sin '|'.", ""
    if not es_fecha_valida(fecha):
        return False, "Fecha inválida: use DD/MM/AAAA real.", ""
    for i in range(len(base["codigos"])):
        if (base["dnis"][i] == dni and base["asuntos"][i].lower() == asunto.lower()
                and base["fechas"][i] == fecha):
            return False, "Expediente duplicado.", base["codigos"][i]
    codigo = generar_codigo(base, int(fecha[-4:]))
    base["codigos"].append(codigo)
    base["dnis"].append(dni)
    base["nombres"].append(nombre.upper())
    base["tipos"].append(tipo)
    base["asuntos"].append(asunto)
    base["fechas"].append(fecha)
    return True, "Expediente registrado.", codigo


def buscar_secuencial(base, codigo):
    """Búsqueda lineal O(n); devuelve posición o -1."""
    for i in range(len(base["codigos"])):
        if base["codigos"][i] == codigo:
            return i
    return -1


def buscar_por_dni(base, dni):
    """Búsqueda lineal O(n) por DNI; devuelve la lista de posiciones (puede ser vacía)."""
    posiciones = []
    for i in range(len(base["dnis"])):
        if base["dnis"][i] == dni:
            posiciones.append(i)
    return posiciones


def ordenar_por_codigo(base):
    """Ordenamiento por inserción O(n^2) sobre arreglos paralelos."""
    n = len(base["codigos"])
    for i in range(1, n):
        reg = {k: base[k][i] for k in base}
        j = i - 1
        while j >= 0 and base["codigos"][j] > reg["codigos"]:
            for k in base:
                base[k][j + 1] = base[k][j]
            j -= 1
        for k in base:
            base[k][j + 1] = reg[k]


def buscar_binaria(base, codigo):
    """Búsqueda binaria O(log n); requiere la base ordenada."""
    inicio, fin = 0, len(base["codigos"]) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if base["codigos"][medio] == codigo:
            return medio
        if base["codigos"][medio] < codigo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return -1


def formatear(base, i):
    return (base["codigos"][i] + " | " + base["fechas"][i] + " | DNI " + base["dnis"][i]
            + " | " + base["nombres"][i] + " | " + base["tipos"][i] + " | " + base["asuntos"][i])
