from ..schemas import QuarentenaResponseSchema, QuarentenaCreateSchema
from ...services import QuarentenaService
from ..paths import QuarentenaPath, AnimalPath
from ...domain.exceptions import TipagemError, NaoCadastradoError, JaCadastradoError, NaoEncontradoError, AnimalIndisponível


from fastapi import APIRouter, HTTPException, status
from typing import Literal

# Paths dos arquivos de persistência
quarentena_path = QuarentenaPath()
animal_path = AnimalPath()

router = APIRouter(prefix="/quarentena", tags=["Quarentena"])

quarentena_service = QuarentenaService(quarentena_path.cachorro, quarentena_path.calopsita, quarentena_path.coelho, quarentena_path.gato, animal_path.cachorro, animal_path.calopsita, animal_path.coelho, animal_path.gato)


@router.post("/{type_animal}", response_model=QuarentenaResponseSchema, status_code=status.HTTP_201_CREATED)
def create(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    payload: QuarentenaCreateSchema
):
    try:
        quarentena_data = payload.model_dump()

        quarentena = quarentena_service.create(type_animal, quarentena_data)
        
        return quarentena

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
    
    except AnimalIndisponível as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    
    except TipagemError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.get("/", response_model=list[QuarentenaResponseSchema], status_code=status.HTTP_201_CREATED)
def get_all():
    try:
        quarentenas = quarentena_service.get_all()
        
        return quarentenas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.get("/{type_animal}", response_model=list[QuarentenaResponseSchema], status_code=status.HTTP_201_CREATED)
def get_all_type_animal(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]
):
    try:
        quarentenas = quarentena_service.get_all_type_animal(type_animal)
        
        return quarentenas

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.get("/{type_animal}/{id}", response_model=list[QuarentenaResponseSchema], status_code=status.HTTP_201_CREATED)
def get_by_id(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id: int
):
    try:
        quarentena = quarentena_service.get_by_id(type_animal, id)
        
        return quarentena
    
    except NaoCadastradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except NaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.put("/{type_animal}/{id}", response_model=QuarentenaResponseSchema, status_code=status.HTTP_201_CREATED)
def update(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id: int,
    payload: QuarentenaCreateSchema
):
    try:
        quarentena_data = payload.model_dump()
        if quarentena_data.get("id"):
            quarentena_data.pop("id")
            
        quarentena = quarentena_service.update(type_animal, quarentena_data, id)
        
        return quarentena

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

    except AnimalIndisponível as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    
    except TipagemError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.delete("/{type_animal}", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_type_animal(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]
):
    try:
        quarentena_service.delete_all(type_animal)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.delete("/{type_animal}/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id: int
):
    try:
        quarentena_service.delete_by_id(type_animal, id)
    
    except NaoCadastradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except NaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )
