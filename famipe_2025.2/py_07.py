tenhoRoupa = input("Tenho roupa lavada? (sim/não): ").strip().lower() == "sim"
temCulto = input("Tem culto hoje? (sim/não): ").strip().lower() == "sim"

print("Tenho roupa lavada : ", tenhoRoupa)
print("Tem culto hoje : ", temCulto)

print(type(tenhoRoupa))
print(type(temCulto))

if tenhoRoupa:
    if temCulto:
        print("Vou ao culto")
    else:
        print("Fico em casa")
else:
    print("Lavo roupa")
    print("Fico em casa")
