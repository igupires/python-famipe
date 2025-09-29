numeros = [10, 20, 30, 40, 50, 60]
# Índices:   0,  1,  2,  3,  4,  5

# Pega do índice 1 até o 3 (o 4 não entra)
fatia1 = numeros[1:4]
print(f"Fatia de 1 a 4: {fatia1}")

# Pega do início até o índice 2 (o 3 não entra)
fatia2 = numeros[:3]
print(f"Fatia do início a 3: {fatia2}")

# Pega do índice 3 até o final
fatia3 = numeros[3:]
print(f"Fatia de 3 ao fim: {fatia3}")

# Pega do índice 1 até o 3 (o 4 não entra) pulando de 2 em 2
fatia4 = numeros[1:4:2]
print(f"Fatia de 1 a 4 de 2 em 2: {fatia4}")