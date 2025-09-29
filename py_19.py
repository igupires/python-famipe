# Exercício 08

produtos = [
    {"nome": "Smartphone Z", "categoria": "Eletrônicos", "estoque": 15},
    {"nome": "Notebook Pro", "categoria": "Eletrônicos", "estoque": 25},
    {"nome": "Cadeira Gamer", "categoria": "Móveis", "estoque": 30},
    {"nome": "Fone Bluetooth", "categoria": "Eletrônicos", "estoque": 50},
    {"nome": "Monitor 4K", "categoria": "Eletrônicos", "estoque": 10},
]

print([produto["nome"] for produto in produtos])