tarefas = []
tarefas.append("Lavar a louça")
tarefas.append("Estudar Python")
print(tarefas)

tarefas.insert(0, "Arrumar a cama")
print(tarefas)

tarefa_removida = tarefas.pop(1)
print(f"Tarefa removida: {tarefa_removida}")
print(tarefas)

tarefas.remove("Estudar Python")
print(tarefas)