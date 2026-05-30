# ==========================================
# SISTEMA DE INVENTARIO DE SUPERMERCADO
# ==========================================

productos = {
    "Arroz": 2.50,
    "Frijoles": 2.00,
    "Azucar": 1.80,
    "Sal": 0.90,
    "Leche": 1.50,
    "Pan": 1.20,
    "Huevos": 3.50,
    "Aceite": 4.25,
    "Cafe": 5.00,
    "Gaseosa": 2.75
}

inventario = []

print("=" * 60)
print("     INVENTARIO DE SUPERMERCADO")
print("=" * 60)

for nombre, precio in productos.items():
    while True:
        try:
            cantidad = int(input(f"Ingrese la cantidad de {nombre} (${precio:.2f}): "))
            if cantidad >= 0:
                break
            print("La cantidad no puede ser negativa.")
        except ValueError:
            print("Ingrese un número válido.")

    valor_total = precio * cantidad

    inventario.append({
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad,
        "valor_total": valor_total
    })

print("\n")
print("=" * 75)
print(f"{'PRODUCTO':20} {'PRECIO':10} {'CANTIDAD':10} {'VALOR TOTAL':15}")
print("=" * 75)

total_general = 0

for producto in inventario:
    print(
        f"{producto['nombre']:20}"
        f"${producto['precio']:<9.2f}"
        f"{producto['cantidad']:<10}"
        f"${producto['valor_total']:<14.2f}"
    )
    total_general += producto["valor_total"]

print("=" * 75)
print(f"VALOR TOTAL DEL INVENTARIO: ${total_general:.2f}")
print("=" * 75) 
print("¡Inventario registrado exitosamente!") 
