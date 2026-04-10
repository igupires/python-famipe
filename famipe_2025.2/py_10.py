# Imprimir apenas os números ímpares de 1 a 10
for i in range(1, 11):
    if i % 2 == 0:  # Se o número for par...
        continue    # ...ignore o resto do código e vá para o próximo 'i'

    # Este print() só é executado se o 'continue' não for acionado
    print(f"Este é um número ímpar: {i}")