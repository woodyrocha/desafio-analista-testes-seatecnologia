import random
import string
from datetime import date


def gerar_cpf_fake():
    return "".join([str(random.randint(0, 9)) for _ in range(11)])


def gerar_nome():
    return "Teste " + "".join(random.choice(string.ascii_letters) for _ in range(6))


def gerar_data_nascimento(anos=30):
    today = date.today()
    ano = today.year - anos
    return f"01/01/{ano}"


def gerar_dados_funcionario():
    return {
        "nome": gerar_nome(),
        "sexo": random.choice(['M', 'F']),  # ← ADICIONAR ESTA LINHA
        "cpf": gerar_cpf_fake(),
        "data_nascimento": gerar_data_nascimento(),
    }