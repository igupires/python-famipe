# Simulação de um sistema de login simples
usuario_correto = "admin"
senha_correta = "1234"

usuario_digitado = "admin"
senha_digitada = "senha_errada"

# 1. Verifica o usuário primeiro
if usuario_digitado == usuario_correto:
    print("Usuário correto. Verificando a senha...")

    # 2. Se o usuário estiver correto, aninha a verificação da senha
    if senha_digitada == senha_correta:
        print("Login bem-sucedido! Acesso concedido.")
    else:
        print("Senha incorreta! Acesso negado.")
else:
    print("Usuário não encontrado!")

# Simulação de um sistema de acesso com múltiplas condições
usuario_ativo = True
tem_permissao = True
horario_comercial = True
feriado = False
sistema_online = True

if usuario_ativo:
    if tem_permissao:
        if horario_comercial:
            if not feriado:
                if sistema_online:
                    print("Acesso permitido!")
                    
                    
# Versão limpa e legível
if (usuario_ativo and
    tem_permissao and
    horario_comercial and
    not feriado and
    sistema_online):
    print("Acesso permitido!")
else:
    print("Acesso negado por alguma razão.")