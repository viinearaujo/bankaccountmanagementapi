from datetime import date
from pydantic import BaseModel
from fastapi import FastAPI


class Pessoa(BaseModel):
    nome: str
    cpf: str
    data_nascimento: date

    class Config():
        orm_mode = True

class ShowPessoa(Pessoa):
    id_pessoa: int

class Conta(BaseModel):
    id_pessoa: int
    saldo: float
    limite_saque_diario: float
    flag_ativo: bool
    tipo_conta: int

    class Config():
        orm_mode = True

class ShowConta(Conta):
    id_conta: int

class Transacao(BaseModel):
    id_conta: int
    valor: float
    data_transacao: date

    class Config():
        orm_mode = True

class ShowTransacao(Transacao):
    id_transacao: int
    tipo_transacao: str
    saldo_anterior: float
    saldo_atual: float