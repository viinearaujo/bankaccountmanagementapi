from bankaccountmanagement.models import Pessoa
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from sqlalchemy.orm import Session
from bankaccountmanagement.database import get_db
from bankaccountmanagement import schemas
from bankaccountmanagement.repository import user
from typing import List


router = APIRouter(
    prefix='/user',
    tags = ['user']
)

@router.post('/', status_code= status.HTTP_201_CREATED, \
    response_model= schemas.ShowPessoa)
def create_user(request: schemas.Pessoa, db: Session= Depends(get_db)):
    """Criar usuário no Sistema BAM"""
    return user.create_user(request, db)

@router.get('/', response_model= List[schemas.ShowPessoa])
def retrieve_all_users(db: Session= Depends(get_db)):
    """Retornar todos usuários do Sistema BAM"""
    return user.retrieve_all_users(db)