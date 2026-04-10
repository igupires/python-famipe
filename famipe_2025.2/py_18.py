vendas_do_dia = [150.00, 25.50, 32.75, 450.20, 12.00]

# 1. Inicialização de AMBOS
numero_de_vendas = 0
total_arrecadado = 0.0

for venda in vendas_do_dia:
    # Atualiza o Contador
    numero_de_vendas += 1
    
    # Atualiza o Acumulador
    total_arrecadado += venda

print(f"Hoje foram realizadas {numero_de_vendas} vendas.")
print(f"O total arrecadado foi de R$ {total_arrecadado:.2f}.")