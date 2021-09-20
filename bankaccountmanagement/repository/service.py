from bankaccountmanagement import schemas
from sqlalchemy.orm import Session
from bankaccountmanagement import models
from bankaccountmanagement.repository.account import get_acc_by_id
from fastapi import HTTPException
from fastapi import status
from datetime import date
from sqlalchemy.orm import Query
from sqlalchemy.sql.functions import sum


def get_balance(id_conta: int, db: Session):
    conta = get_acc_by_id(id_conta, db).first()
    return {'saldo': conta.saldo}

def make_deposit(request: schemas.Transacao, db: Session):
    if request.valor <= 0:
        raise HTTPException(
            status_code = status.HTTP_412_PRECONDITION_FAILED,
            detail = ('Para efetuar um depósito, o valor informado '
                f'deve ser positivo.')
        )
    conta = get_acc_by_id(request.id_conta, db)
    check_active(request.id_conta, db)
    novo_saldo = conta.first().saldo + request.valor
    nova_transacao = models.Transacao(
        id_conta = request.id_conta,
        tipo_transacao = 'deposit',
        valor = request.valor,
        saldo_anterior = conta.first().saldo,
        saldo_atual = novo_saldo,
        data_transacao = request.data_transacao
    )
    conta.update({'saldo': novo_saldo}, synchronize_session= False)
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return {'msg': 'Operação efetuada com sucesso.',
        'saldo': novo_saldo}

def withdraw(request: schemas.Transacao, db:Session):
    if request.valor <= 0:
        raise HTTPException(
            status_code = status.HTTP_412_PRECONDITION_FAILED,
            detail = ('Para efetuar um saque, o valor informado '
                f'deve ser positivo.')
        )
    conta = get_acc_by_id(request.id_conta, db)
    check_active(request.id_conta, db)
    novo_saldo = conta.first().saldo - request.valor
    check_withdrawal_limit(conta.first(), request.valor, db)
    if novo_saldo < 0:
        raise HTTPException(
            status_code = status.HTTP_412_PRECONDITION_FAILED,
            detail = ('Impossível seguir a operação com o valor enviado.'
                'Valor do saque maior que o saldo atual.'
                f'O saldo é de R${conta.first().saldo}.')
        )
    nova_transacao = models.Transacao(
        id_conta = request.id_conta,
        tipo_transacao = 'withdraw',
        valor = request.valor,
        saldo_anterior = conta.first().saldo,
        saldo_atual = novo_saldo,
        data_transacao = request.data_transacao
    )
    conta.update({'saldo': novo_saldo}, synchronize_session= False)
    db.add(nova_transacao)
    db.commit()
    db.refresh(nova_transacao)
    return {'msg': 'Operação efetuada com sucesso.',
        'saldo': novo_saldo}

def get_statement(id_conta: int, db: Session, 
        dt_inicio: date= None, dt_fim: date= None,):
    if dt_inicio and dt_fim:
        statement = get_statement_by_id(id_conta, db).\
            filter(models.Transacao.data_transacao >= dt_inicio).\
            filter(models.Transacao.data_transacao <= dt_fim).all()
    else:        
        statement = get_statement_by_id(id_conta, db).all()
    return statement

def get_statement_by_id(id_conta: int, db: Session) -> Query:
    statement = db.query(models.Transacao).\
        filter(models.Transacao.id_conta == id_conta)
    if not statement.first():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = ('Não foram encontradas transações efetuadas pela '
                'conta especificada no Sistema BAM.')
        )
    return statement

def check_active(id_conta: int, db: Session) -> None:
    conta = get_acc_by_id(id_conta, db).first()
    if not conta.flag_ativo:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = 'A conta informada está bloqueada no Sistema BAM.'
        )
    return None

def check_withdrawal_limit(conta: models.Conta, valor: float, 
        db: Session) -> None:
    daily_withdraw = db.query\
        (sum(models.Transacao.saldo_atual-models.Transacao.saldo_anterior).\
        filter(models.Transacao.id_conta == conta.id_conta).\
        filter(models.Transacao.data_transacao == date.today()).\
        filter(models.Transacao.tipo_transacao == 'withdraw')).\
        scalar()
    if daily_withdraw:
        daily_withdraw = daily_withdraw *-1
        desired_withdraw = daily_withdraw + valor
        if desired_withdraw > conta.limite_saque_diario:
            raise HTTPException(
                status_code = status.HTTP_403_FORBIDDEN,
                detail = (f'Impossível efetuar saque de R${valor}. '
                f'Hoje você já sacou R${daily_withdraw} e seu limite de '
                f'saque diário é de {conta.limite_saque_diario}.')
            )
    elif valor > conta.limite_saque_diario:
        raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = (f'Impossível efetuar saque de R${valor}. '
            f'Seu limite de saque diário é de {conta.limite_saque_diario}.')
    )
    return None

def raise_invalid_withdraw(conta: models.Conta, valor: float, 
        daily_withdraw: float):
    raise HTTPException(
        status_code = status.HTTP_403_FORBIDDEN,
        detail = (f'Impossível efetuar saque de R${valor}.'
            f'Hoje você já sacou R${daily_withdraw} e seu limite de '
            f'saque diário é de {conta.limite_saque_diario}.')
    )
