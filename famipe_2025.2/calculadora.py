# Ferramentas que podem ser reutilizadas
def somar(a, b):
    return a + b

def subtrair(a, b):
    return a - b

# Ponto de entrada para testar o módulo
if __name__ == "__main__":
    print("Testando o módulo calculadora...")
    # Este código só roda quando executamos 'python calculadora.py'
    soma_teste = somar(10, 5)
    sub_teste = subtrair(10, 5)
    print(f"Teste de soma: {soma_teste}")
    print(f"Teste de subtração: {sub_teste}")