from bankaccountmanagement.database import Base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy.orm import relationship


class Pessoa(Base):
    __tablename__ = 'pessoas'
    id_pessoa = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    cpf = Column(String)
    data_nascimento = Column(Date)

    contas = relationship("Conta", back_populates="pessoas")

class Conta(Base):
    __tablename__ = 'contas'
    id_conta = Column(Integer, primary_key=True, index=True)
    id_pessoa = Column(Integer, ForeignKey('pessoas.id_pessoa'), nullable=False)
    saldo = Column(Float)
    limite_saque_diario = Column(Float)
    flag_ativo = Column(Boolean)
    tipo_conta = Column(Integer)
    data_criacao = Column(Date)

    pessoas = relationship("Pessoa", back_populates="contas")
    transacoes = relationship("Transacao", back_populates="contas")

class Transacao(Base):
    __tablename__ = 'transacoes'
    id_transacao = Column(Integer, primary_key= True, index= True)
    id_conta = Column(Integer, ForeignKey('contas.id_conta'), nullable= False)
    tipo_transacao = Column(String)
    valor = Column(Float)
    saldo_anterior = Column(Float)
    saldo_atual = Column(Float)
    data_transacao = Column(Date)

    contas = relationship("Conta", back_populates="transacoes")
