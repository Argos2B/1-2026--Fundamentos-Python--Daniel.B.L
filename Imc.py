# Actividad 2: Calculadora IMC

# Datos Personales
nombre = "Daniel"
edad = 17
peso = 79
estatura = 1.15

# Calculadora IMC
imc = peso / (estatura ** 2)

# Clasificación IMC
if imc < 18.5:
    clasificacion = "Bajo peso"

elif imc >= 18.5 and imc <= 24.9:
    clasificacion = "Peso normal"

elif imc >= 25 and imc <= 29.9:
    clasificacion = "Sobrepeso"

else:
    clasificacion = "Obesidad"

# Mostrar Resultados
print("----- Resultados -----")
print("Nombre:", nombre)
print("Edad:", edad)
print("Peso:", peso, "kg")
print("Estatura:", estatura, "m")
print("IMC calculado:", round(imc, 2))
print("Clasificación:", clasificacion)

# Resultado adicional
if imc >= 30:
    print("Resultado adicional: debe consultar a un especialista.")
else:
    print("Resultado adicional: mantenga hábitos saludables.")