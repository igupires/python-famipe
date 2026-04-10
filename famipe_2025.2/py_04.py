possoSair = True
saldoBancario = 11

print(possoSair)
print(type(possoSair))

print(saldoBancario)
print(type(saldoBancario))

if possoSair and saldoBancario > 50:
    print("Vou a praia")
elif possoSair and saldoBancario > 20:
    print("Vou ao cinema")
elif possoSair and saldoBancario > 15:
    print("Vou almoçar fora")
elif possoSair and saldoBancario > 10:
    print("Vou pedir um lanche")
else:
    print("Fico em casa e vou comer em casa")

match saldoBancario:
    case 0:
        print("Não tenho dinheiro")
    case 20:
        print("Tenho 20 reais")
    case 40:
        print("Tenho 40 reais")
    case _:
        print("Tenho mais de 40 reais")
