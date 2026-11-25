"""Módulo de validaciones de datos de expedientes (mesa de partes digital)."""


def es_dni_valido(dni):
    """DNI peruano: exactamente 8 dígitos numéricos."""
    return len(dni) == 8 and dni.isdigit()


def es_bisiesto(anio):
    """Año bisiesto: divisible por 4 y (no por 100 o sí por 400)."""
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)


def dias_del_mes(mes, anio):
    """Devuelve los días del mes (0 si el mes no existe)."""
    if mes < 1 or mes > 12:
        return 0
    if mes == 2:
        return 29 if es_bisiesto(anio) else 28
    if mes in (4, 6, 9, 11):
        return 30
    return 31


def es_fecha_valida(texto):
    """Formato DD/MM/AAAA con fecha calendario real."""
    partes = texto.split("/")
    if len(partes) != 3:
        return False
    d, m, a = partes
    if not (d.isdigit() and m.isdigit() and a.isdigit()):
        return False
    if len(d) != 2 or len(m) != 2 or len(a) != 4:
        return False
    dia, mes, anio = int(d), int(m), int(a)
    return 1 <= dia <= dias_del_mes(mes, anio)


def es_nombre_valido(nombre):
    """Al menos dos palabras, solo letras y espacios, mínimo 5 caracteres."""
    nombre = nombre.strip()
    if len(nombre) < 5 or len(nombre.split()) < 2:
        return False
    for c in nombre:
        if not (c.isalpha() or c == " "):
            return False
    return True


def es_asunto_valido(asunto):
    """Asunto entre 5 y 120 caracteres, sin el separador de archivo '|'."""
    asunto = asunto.strip()
    return 5 <= len(asunto) <= 120 and "|" not in asunto


# Catálogo cerrado de tipos de trámite (no se aceptan tipos inexistentes)
TIPOS_TRAMITE = ["Licencia de funcionamiento", "Constancia", "Reclamo",
                 "Solicitud de información", "Pago de tributos", "Otros"]


def normalizar_tipo(tipo):
    """Devuelve el tipo del catálogo (con su escritura oficial) o '' si no existe."""
    t = tipo.strip().lower()
    for oficial in TIPOS_TRAMITE:
        if oficial.lower() == t:
            return oficial
    return ""


def es_tipo_valido(tipo):
    """Un tipo es válido solo si pertenece al catálogo cerrado."""
    return normalizar_tipo(tipo) != ""
