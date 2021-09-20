from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from sqlalchemy.orm import Session
from bankaccountmanagement import schemas
from bankaccountmanagement.database import get_db
from bankaccountmanagement.repository import account
from typing import List


router = APIRouter(
    prefix='/account',
    tags=['account']
)

@router.post('/', status_code= status.HTTP_201_CREATED)
def create_bank_account(request: schemas.Conta, db: Session= Depends(get_db)):
    """Criar conta no Sistema BAM"""
    return account.create_bank_account(request, db)

@router.get('/', response_model= List[schemas.ShowConta])
def retrieve_all_bank_accounts(db: Session= Depends(get_db)):
    """Retornar todas as contas do Sistema BAM"""
    return account.retrieve_all_bank_accounts(db)

@router.put('/{id_conta}')
def block_unblock_bank_account(id_conta: int, db: Session= Depends(get_db)):
    """Bloquear ou desbloquear conta específica no Sistema BAM."""
    return account.block_unblock_bank_account(id_conta, db)
