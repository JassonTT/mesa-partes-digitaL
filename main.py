"""Mesa de Partes Digital - prototipo de consola (CIIN1205P)."""
from persistencia import cargar, guardar
from expedientes import (registrar, buscar_binaria, ordenar_por_codigo, formatear)

RUTA = "expedientes.txt"


def mostrar_menu():
    print("\n=== MESA DE PARTES DIGITAL ===")
    print("1. Registrar expediente\n2. Buscar por código\n3. Listar ordenado por código\n4. Salir")


def main():
    base, omitidas = cargar(RUTA)
    if omitidas:
        print("Aviso:", omitidas, "línea(s) corrupta(s) omitida(s).")
    opcion = ""
    while opcion != "4":
        mostrar_menu()
        opcion = input("Opción: ").strip()
        if opcion == "1":
            ok, msg, cod = registrar(base, input("DNI: "), input("Nombre completo: "),
                                     input("Asunto: "), input("Fecha (DD/MM/AAAA): "))
            print(msg, cod)
            if ok:
                guardar(base, RUTA)
        elif opcion == "2":
            ordenar_por_codigo(base)
            pos = buscar_binaria(base, input("Código: ").strip().upper())
            print(formatear(base, pos) if pos >= 0 else "No encontrado.")
        elif opcion == "3":
            ordenar_por_codigo(base)
            for i in range(len(base["codigos"])):
                print(formatear(base, i))
        elif opcion != "4":
            print("Opción no válida.")


if __name__ == "__main__":
    main()
