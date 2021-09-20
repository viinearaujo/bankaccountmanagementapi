import sqlalchemy
from sqlalchemy.orm import Session
from fastapi import HTTPException
from fastapi import status
from datetime import date
from sqlalchemy.orm import Query
from bankaccountmanagement import schemas
from bankaccountmanagement import models


def create_bank_account(request: schemas.Conta, db: Session):
    new_conta = models.Conta(
        id_pessoa = request.id_pessoa,
        saldo = request.saldo,
        limite_saque_diario = request.limite_saque_diario,
        flag_ativo = request.flag_ativo,
        tipo_conta = request.tipo_conta,
        data_criacao = date.today()
    )
    try:
        db.add(new_conta)
        db.commit()
        db.refresh(new_conta)
        return new_conta
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'O id_conta informado não foi encontrada no Sistema BAM.'
        )

def retrieve_all_bank_accounts(db: Session):
    contas = db.query(models.Conta).all()
    return contas

def block_unblock_bank_account(id_conta: int, db: Session):
    conta = get_acc_by_id(id_conta, db).first()
    acao: str
    if conta.flag_ativo:
        conta.flag_ativo = False
        acao = 'bloqueada'
    else:
        conta.flag_ativo = True
        acao = 'desbloqueada'
    db.add(conta)
    db.commit()
    return {'msg': f'Operação realizada com sucesso. A conta foi {acao}.'}

def get_acc_by_id(id_conta: int, db: Session) -> Query:
    conta = db.query(models.Conta).filter(models.Conta.id_conta == id_conta)
    if not conta.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'A conta informada não foi encontrada no Sistema BAM.'
        )
    return conta