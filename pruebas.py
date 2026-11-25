"""Casos de prueba automáticos con datos ficticios de la estructura observada (informe, sección 7)."""
import os
from validaciones import *
from expedientes import *
from persistencia import *

RUTA = "prueba_tmp.txt"
resultados = []


def caso(n, desc, obtenido, esperado):
    ok = obtenido == esperado
    resultados.append(ok)
    print("C%02d | %-52s | esp=%-6s obt=%-6s | %s" % (n, desc, esperado, obtenido, "OK" if ok else "FALLA"))


b = nueva_base()
caso(1, "DNI válido 45872136", es_dni_valido("45872136"), True)
caso(2, "DNI con 7 dígitos", es_dni_valido("4587213"), False)
caso(3, "DNI con letras", es_dni_valido("4587A136"), False)
caso(4, "Fecha 15/10/2026", es_fecha_valida("15/10/2026"), True)
caso(5, "Fecha 30/02/2026 (no existe)", es_fecha_valida("30/02/2026"), False)
caso(6, "Fecha 29/02/2024 (bisiesto)", es_fecha_valida("29/02/2024"), True)
caso(7, "Fecha 29/02/2025 (no bisiesto)", es_fecha_valida("29/02/2025"), False)
caso(8, "Fecha 1/1/2026 (formato incorrecto)", es_fecha_valida("1/1/2026"), False)
caso(9, "Nombre de una sola palabra", es_nombre_valido("Rosa"), False)
caso(10, "Nombre con números", es_nombre_valido("Rosa Q4 Lopez"), False)
caso(11, "Registro válido 1", registrar(b, "45872136", "Rosa Quispe Lopez", "Licencia de funcionamiento", "Solicitud de licencia de funcionamiento", "15/10/2026")[2], "EXP-2026-0001")
caso(12, "Registro válido 2", registrar(b, "70123456", "Luis Paredes Ruiz", "Reclamo", "Reclamo por recojo de residuos", "16/10/2026")[2], "EXP-2026-0002")
caso(13, "Registro válido 3", registrar(b, "08765432", "Ana Mendoza Cruz", "Constancia", "Constancia de posesión", "02/11/2026")[2], "EXP-2026-0003")
caso(14, "Registro con DNI inválido rechazado", registrar(b, "123", "Luis Paredes Ruiz", "Reclamo", "Asunto valido", "16/10/2026")[0], False)
caso(15, "Duplicado rechazado", registrar(b, "70123456", "Luis Paredes Ruiz", "Reclamo", "reclamo por recojo de residuos", "16/10/2026")[0], False)
caso(16, "Asunto con separador '|' rechazado", registrar(b, "70123456", "Luis Paredes Ruiz", "Reclamo", "Queja | grave", "17/10/2026")[0], False)
caso(17, "Total de expedientes tras 3 válidos", len(b["codigos"]), 3)
caso(18, "Búsqueda secuencial de EXP-2026-0002", buscar_secuencial(b, "EXP-2026-0002"), 1)
caso(19, "Búsqueda de código inexistente", buscar_secuencial(b, "EXP-2026-0999"), -1)
# Orden: insertar en desorden
d = nueva_base()
for k, c in enumerate(["EXP-2026-0003", "EXP-2026-0001", "EXP-2026-0002"]):
    for clave, v in zip(d, [c, "1000000" + str(k), "Nombre Apellido", "Reclamo", "Asunto de prueba", "01/01/2026"]):
        d[clave].append(v)
ordenar_por_codigo(d)
caso(20, "Ordenamiento por código", d["codigos"], ["EXP-2026-0001", "EXP-2026-0002", "EXP-2026-0003"])
caso(21, "Arreglos paralelos coherentes tras ordenar", d["dnis"], ["10000001", "10000002", "10000000"])
caso(22, "Búsqueda binaria de EXP-2026-0003", buscar_binaria(d, "EXP-2026-0003"), 2)
caso(23, "Búsqueda binaria en base vacía", buscar_binaria(nueva_base(), "X"), -1)
guardar(b, RUTA)
c, om = cargar(RUTA)
caso(24, "Persistencia: guardar y cargar idéntico", c == b, True)
with open(RUTA, "a", encoding="utf-8") as f:
    f.write("LINEA|CORRUPTA\n")
c2, om2 = cargar(RUTA)
caso(25, "Línea corrupta omitida (1) y datos intactos", (om2, len(c2["codigos"])), (1, 3))
caso(26, "Archivo inexistente devuelve base vacía", len(cargar("no_existe.txt")[0]["codigos"]), 0)
caso(27, "Correlativo continúa tras cargar", registrar(c, "11223344", "Pedro Salas Vega", "Pago de tributos", "Pago de arbitrios", "03/11/2026")[2], "EXP-2026-0004")
# Tipo de trámite (catálogo cerrado) y búsqueda por DNI
caso(28, "Tipo válido del catálogo: Constancia", es_tipo_valido("Constancia"), True)
caso(29, "Tipo en minúsculas se normaliza", normalizar_tipo("  reclamo "), "Reclamo")
caso(30, "Tipo inexistente no es válido", es_tipo_valido("Tramite inventado"), False)
caso(31, "Registro con tipo inexistente rechazado", registrar(c, "11223344", "Pedro Salas Vega", "Tramite inventado", "Asunto valido", "04/11/2026")[0], False)
caso(32, "Búsqueda por DNI 70123456", buscar_por_dni(c, "70123456"), [1])
caso(33, "Búsqueda por DNI sin expedientes", buscar_por_dni(c, "99999999"), [])
registrar(c, "45872136", "Rosa Quispe Lopez", "Constancia", "Constancia de domicilio", "05/11/2026")
caso(34, "DNI con dos expedientes devuelve ambas posiciones", buscar_por_dni(c, "45872136"), [0, 4])
guardar(c, RUTA)
caso(35, "Persistencia conserva el tipo de trámite", cargar(RUTA)[0]["tipos"] == c["tipos"], True)
os.remove(RUTA)
print("\nResumen: %d/%d casos aprobados" % (sum(resultados), len(resultados)))
