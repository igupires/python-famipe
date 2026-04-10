emails = ["contato@site.com", "spam", "usuario@site.com"]
for email in emails:
    if "@" not in email:
        continue # Pula o email inválido
    print(f"Enviando para: {email}")