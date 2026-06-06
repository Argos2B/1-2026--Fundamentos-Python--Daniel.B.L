# ==========================================
# SISTEMA DE VENTAS DE SUPERMERCADO
# ==========================================

productos = {
    # Frutas
    "Manzana": 0.50,
    "Banano": 0.30,
    "Naranja": 0.40,
    "Pera": 0.60,
    "Uva": 2.50,
    "Sandia": 5.00,
    "Melon": 3.50,
    "Piña": 2.75,
    "Mango": 0.80,
    "Papaya": 2.20,
    "Fresa": 2.80,
    "Kiwi": 0.90,
    "Limon": 0.20,
    "Mandarina": 0.35,
    "Coco": 2.00,

    # Verduras
    "Papa": 0.40,
    "Tomate": 0.50,
    "Cebolla": 0.45,
    "Zanahoria": 0.35,
    "Lechuga": 1.00,
    "Pepino": 0.60,
    "Chayote": 0.55,
    "Brocoli": 1.50,
    "Coliflor": 1.60,
    "Chile Dulce": 0.70,
    "Ajo": 0.25,
    "Apio": 0.80,
    "Espinaca": 1.20,
    "Repollo": 1.10,
    "Yuca": 0.75,

    # Carnes
    "Pollo": 4.50,
    "Carne Res": 7.50,
    "Carne Cerdo": 5.80,
    "Pechuga Pollo": 5.20,
    "Costilla Cerdo": 6.50,
    "Salchicha": 3.50,
    "Jamon": 2.80,
    "Mortadela": 2.20,
    "Chorizo": 4.00,
    "Tocino": 4.50,

    # Lácteos
    "Leche": 1.50,
    "Queso": 4.20,
    "Mantequilla": 2.50,
    "Yogurt": 2.00,
    "Crema": 1.80,
    "Helado": 4.50,
    "Leche Condensada": 2.30,
    "Leche Evaporada": 2.10,
    "Queso Crema": 2.80,
    "Huevos": 3.50,

    # Granos y básicos
    "Arroz": 2.50,
    "Frijoles": 2.00,
    "Azucar": 1.80,
    "Sal": 0.90,
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
print("SUPERMERCADO")
print("=" * 60)

carrito = []
total_compra = 0

while True:
    nombre = input(
        "\nIngrese el nombre del producto "
        "(o 'fin' para terminar): "
    ).title()

    if nombre == "Fin":
        break

    if nombre not in productos:
        print("Producto no encontrado.")
        continue

    cantidad = int(input("Cantidad: "))

    precio = productos[nombre]
    subtotal = precio * cantidad

    carrito.append([nombre, precio, cantidad, subtotal])
    total_compra += subtotal

    print(f"Precio unitario: ${precio:.2f}")
    print(f"Subtotal: ${subtotal:.2f}")

print("\nFACTURA")
print("-" * 60)
print(f"{'Producto':20}{'Precio':10}{'Cant.':10}{'Subtotal':10}")

for item in carrito:
    print(
        f"{item[0]:20}"
        f"${item[1]:<9.2f}"
        f"{item[2]:<10}"
        f"${item[3]:.2f}"
    )

print("-" * 60)
print(f"TOTAL A PAGAR: ${total_compra:.2f}")