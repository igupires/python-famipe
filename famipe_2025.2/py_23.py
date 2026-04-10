# Uma lista de strings
convidados = ["Alice", "Beto", "Carla"]

# Uma lista de números
notas = [9.5, 7.0, 8.2, 6.5]

# Uma lista vazia para ser preenchida depois
tarefas = []

primeiro_convidado = convidados[0] # Pega o item no índice 0
segunda_nota = notas[1]         # Pega o item no índice 1

print(f"O primeiro convidado é: {primeiro_convidado}") # Saída: Alice

ultimo_convidado = convidados[-1] # Pega o último item
print(f"O último convidado é: {ultimo_convidado}") # Saída: Carla

print(f"Lista original: {convidados}")
convidados[1] = "Bruno" # Substitui "Beto" por "Bruno" no índice 1
print(f"Lista modificada: {convidados}")