# Procurando o primeiro número maior que 10
numeros = [2, 4, 6, 8, 12, 14, 16]

for num in numeros:
    print(f"Analisando o número {num}...")
    if num > 10:
        print("Encontrei o que procurava!")
        break  # O laço para aqui. O resto da lista não é percorrido.

print("Busca finalizada.") # O código pula para esta linha