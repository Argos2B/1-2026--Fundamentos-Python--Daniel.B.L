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
    "Harina": 1.60,
    "Maiz": 1.40,
    "Avena": 2.10,
    "Lentejas": 2.20,
    "Garbanzos": 2.30,

    # Bebidas
    "Agua": 1.00,
    "Gaseosa": 2.75,
    "Jugo Naranja": 2.50,
    "Jugo Manzana": 2.40,
    "Té Frio": 1.80,
    "Bebida Energetica": 2.90,
    "Cafe Frio": 2.20,
    "Chocolate Liquido": 2.60,
    "Agua Mineral": 1.30,
    "Batido": 3.00,

    # Panadería
    "Pan Blanco": 1.20,
    "Pan Integral": 1.50,
    "Galletas": 1.80,
    "Queque": 4.00,
    "Croissant": 1.50,
    "Donas": 1.20,
    "Tortillas": 2.00,
    "Pan Hamburguesa": 1.80,
    "Pan Hot Dog": 1.70,
    "Pastel": 8.00,

    # Limpieza
    "Jabon": 1.50,
    "Detergente": 4.50,
    "Cloro": 2.00,
    "Suavizante": 3.50,
    "Esponja": 1.00,
    "Papel Higienico": 5.00,
    "Servilletas": 1.80,
    "Limpiador Piso": 3.20,
    "Desinfectante": 2.90,
    "Bolsa Basura": 2.50,

    # Higiene personal
    "Shampoo": 4.50,
    "Acondicionador": 4.30,
    "Pasta Dental": 2.50,
    "Cepillo Dental": 1.80,
    "Jabon Bano": 1.20,
    "Desodorante": 3.50,
    "Papel Facial": 2.00,
    "Crema Corporal": 4.00,
    "Rastrillo": 2.50,
    "Enjuague Bucal": 3.80
}

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
