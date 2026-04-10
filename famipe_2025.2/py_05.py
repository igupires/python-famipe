saldoBancario = 11
opcao = 2

print("Antes: ",saldoBancario)

match opcao:
    case 1: # praia - gasto 50 reais
        saldoBancario = saldoBancario - 50
    case 2: # cinema - gasto 20 reais
        saldoBancario = saldoBancario - 20
    case 3: # almoço - gasto 15 reais
        saldoBancario = saldoBancario - 15
    case 4: # lanche - gasto 10 reais
        saldoBancario = saldoBancario - 10
    case _: # default - Fico em casa
        saldoBancario = saldoBancario


print("Depois: ",saldoBancario)
print(type(saldoBancario))

print(opcao)
print(type(opcao))