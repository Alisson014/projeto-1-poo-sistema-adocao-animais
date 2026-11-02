from ..schemas import AdotanteSchema
from ...services import PessoaService
from ..paths import PessoaPath, PoliticaPath
from ...domain.exceptions import EmailInvalidoError, TipagemError, ValorForaDoIntervaloError, NaoCadastradoError, JaCadastradoError, PoliticaError

from fastapi import APIRouter, HTTPException, status
from typing import Literal

# Paths dos arquivos de persistência
pessoa_path = PessoaPath()

router = APIRouter(prefix="/pessoa", tags=["Pessoa"])

pessoa_service = PessoaService(pessoa_path.adotante, PoliticaPath.path)


@router.post("/{type_pessoa}", response_model=AdotanteSchema, status_code=status.HTTP_201_CREATED)
def create(
    type_pessoa: Literal["Adotante"],
    payload: AdotanteSchema
):
    try:
        pessoa_data = payload.model_dump()

        pessoa = pessoa_service.create(type_pessoa, pessoa_data)
        
        return pessoa

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except JaCadastradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except EmailInvalidoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except TipagemError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except PoliticaError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except ValorForaDoIntervaloError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.get("/", response_model=list[AdotanteSchema], status_code=status.HTTP_200_OK)
def get_all():
    try:
        pessoas = pessoa_service.get_all()
        
        return pessoas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.get("/{type_pessoa}/{email}", response_model=AdotanteSchema, status_code=status.HTTP_200_OK)
def get_by_email(
    type_pessoa: Literal["Adotante"],
    email: str
):
    try:
        pessoa = pessoa_service.get_by_email(type_pessoa, email)
        
        return pessoa
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except NaoCadastradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.put("/{type_pessoa}", response_model=AdotanteSchema, status_code=status.HTTP_200_OK)
def update(
    type_pessoa: Literal["Adotante"],
    payload: AdotanteSchema,
    email: str
):
    try:
        pessoa_data = payload.model_dump()

        pessoa = pessoa_service.update(type_pessoa, pessoa_data, email)
        
        return pessoa

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except NaoCadastradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except EmailInvalidoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except TipagemError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except PoliticaError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except ValorForaDoIntervaloError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.delete("/{type_pessoa}/{email}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_email(
    type_pessoa: Literal["Adotante"],
    email: str
):
    try:
        pessoa_service.delete_by_email(type_pessoa, email)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except NaoCadastradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.delete("/{type_pessoa}", status_code=status.HTTP_204_NO_CONTENT)
def delete_all(
    type_pessoa: Literal["Adotante"],
):
    try:
        pessoa_service.delete_all(type_pessoa)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )
