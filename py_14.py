# Laço externo: define o número da tabuada (n)
for n in range(1, 6):
    print(f"====== Tabuada do {n} ======")
    
    # Laço interno: define o multiplicador (i)
    for i in range(1, 11):
        resultado = n * i
        print(f"{n} x {i} = {resultado}")
    
    print() # Adiciona uma linha em branco para separar as tabuadas