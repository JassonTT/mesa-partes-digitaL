"""Mesa de Partes Digital - prototipo de consola (CIIN1205P)."""
from persistencia import cargar, guardar
from validaciones import TIPOS_TRAMITE
from expedientes import (registrar, buscar_binaria, buscar_por_dni,
                         ordenar_por_codigo, formatear)

RUTA = "expedientes.txt"


def mostrar_menu():
    print("\n=== MESA DE PARTES DIGITAL ===")
    print("1. Registrar expediente\n2. Buscar por código\n3. Buscar por DNI")
    print("4. Listar ordenado por código\n5. Salir")


def main():
    base, omitidas = cargar(RUTA)
    if omitidas:
        print("Aviso:", omitidas, "línea(s) corrupta(s) omitida(s).")
    opcion = ""
    while opcion != "5":
        mostrar_menu()
        opcion = input("Opción: ").strip()
        if opcion == "1":
            print("Tipos de trámite:", ", ".join(TIPOS_TRAMITE))
            ok, msg, cod = registrar(base, input("DNI: "), input("Nombre completo: "),
                                     input("Tipo de trámite: "), input("Asunto: "),
                                     input("Fecha (DD/MM/AAAA): "))
            print(msg, cod)
            if ok:
                guardar(base, RUTA)
        elif opcion == "2":
            ordenar_por_codigo(base)
            pos = buscar_binaria(base, input("Código: ").strip().upper())
            print(formatear(base, pos) if pos >= 0 else "No encontrado.")
        elif opcion == "3":
            posiciones = buscar_por_dni(base, input("DNI: ").strip())
            for i in posiciones:
                print(formatear(base, i))
            if not posiciones:
                print("No se encontraron expedientes para ese DNI.")
        elif opcion == "4":
            ordenar_por_codigo(base)
            for i in range(len(base["codigos"])):
                print(formatear(base, i))
        elif opcion != "5":
            print("Opción no válida.")


if __name__ == "__main__":
    main()
