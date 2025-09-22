# Uma matriz 3x3 representada como uma lista de listas
matriz = [
    [1, 2, 3],  # linha 0
    [4, 5, 6],  # linha 1
    [7, 8, 9]   # linha 2
]

# Laço externo: percorre cada linha da matriz
for linha in matriz:
    print(f"Processando a linha: {linha}")
    
    # Laço interno: percorre cada elemento DENTRO da linha atual
    for elemento in linha:
        print(f"  > Valor do elemento: {elemento}")