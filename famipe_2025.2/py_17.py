precos_carrinho = [19.99, 45.50, 12.75, 5.00]
total_da_compra = 0.0 # 1. Inicialização

for preco in precos_carrinho:
    total_da_compra += preco # 2. Atualização (soma o preço do item)

# 3. Resultado
print(f"O valor total da compra é: R$ {total_da_compra:.2f}")