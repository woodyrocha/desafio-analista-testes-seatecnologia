import random
import string
from datetime import date


def gerar_cpf_fake():
    """Gera um CPF fake (apenas números)."""
    return "".join([str(random.randint(0, 9)) for _ in range(11)])


def gerar_rg_fake():
    """Gera um RG fake (9 dígitos)."""
    return "".join([str(random.randint(0, 9)) for _ in range(9)])


def gerar_nome():
    """Gera um nome fake para testes."""
    return "Teste " + "".join(random.choice(string.ascii_letters) for _ in range(6))


def gerar_data_nascimento(anos=30):
    """Gera uma data de nascimento no formato DD/MM/AAAA."""
    today = date.today()
    ano = today.year - anos
    return f"01/01/{ano}"


def gerar_dados_funcionario():
    """
    Gera um dicionário completo com dados fake de um funcionário.

    Returns:
        dict: Dados do funcionário incluindo nome, sexo, CPF, data, RG
    """
    return {
        "nome": gerar_nome(),
        "sexo": random.choice(['M', 'F']),
        "cpf": gerar_cpf_fake(),
        "data_nascimento": gerar_data_nascimento(),
        "rg": gerar_rg_fake(),  # ← ADICIONAR ESTA LINHA
    }