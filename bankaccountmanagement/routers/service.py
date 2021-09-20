from bankaccountmanagement import schemas
from bankaccountmanagement.repository import service
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from bankaccountmanagement.database import get_db
from bankaccountmanagement.repository.account import get_acc_by_id
from datetime import date
from typing import List

router = APIRouter(
    prefix='/service',
    tags = ['service']
)

@router.get('/balance/{id_conta}')
def get_balance(id_conta: int, db: Session= Depends(get_db)):
    """Retornar saldo de conta específica do Sistema BAM"""
    return service.get_balance(id_conta, db)

@router.put('/deposit')
def make_deposit(request: schemas.Transacao, db: Session= Depends(get_db)):
    """Realizar depósito em conta bancária específica no Sistema BAM."""
    return service.make_deposit(request, db)

@router.put('/withdraw')
def withdraw(request: schemas.Transacao, db:Session= Depends(get_db)):
    """Realizar saque em conta bancária específica no Sistema BAM."""
    return service.withdraw(request, db)

@router.get('/statement/{id_conta}', response_model=List[schemas.ShowTransacao])
def get_statement(id_conta: int, dt_inicio: date= None, 
        dt_fim: date= None, db: Session= Depends(get_db)):
    """Retornar extrato bancário de conta específica do Sistema BAM."""
    return service.get_statement(id_conta, db, dt_inicio, dt_fim)
