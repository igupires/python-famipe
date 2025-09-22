# Laço externo (horas)
for hora in range(1, 3): # Vamos simular 2 horas
    print(f"--- A HORA AGORA É {hora} ---")
    
    # Laço interno (minutos)
    for minuto in range(1, 4): # Vamos simular 3 minutos por hora
        print(f"  Hora: {hora}, Minuto: {minuto}")