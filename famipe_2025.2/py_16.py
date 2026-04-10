numeros = [1, 2, 3, 4, 5, 6, 7, 8]
contador_de_pares = 0 # 1. Inicialização

for numero in numeros:
    if numero % 2 == 0:
        contador_de_pares += 1 # 2. Incremento (+1)

# 3. Resultado
print(f"A lista possui {contador_de_pares} números pares.")