from bankaccountmanagement import models
from bankaccountmanagement import schemas
from sqlalchemy.orm import Session

def create_user(request: schemas.Pessoa, db: Session):
    new_pessoa = models.Pessoa(
        nome = request.nome,
        cpf = request.cpf,
        data_nascimento = request.data_nascimento  
    )
    db.add(new_pessoa)
    db.commit()
    db.refresh(new_pessoa)
    return new_pessoa

def retrieve_all_users(db: Session):
    pessoas = db.query(models.Pessoa).all()
    return pessoas