from ..schemas import CachorroCreateSchema, CachorroResponseSchema, CalopsitaCreateSchema, CalopsitaResponseSchema, CoelhoResponseSchema, CoelhoCreateSchema, GatoResponseSchema, GatoCreateSchema, AnimalResponseUnion
from ...services import AnimalService
from ..paths import AnimalPath
from ...domain.exceptions import NaoCadastradoError, JaCadastradoError, TipagemError, ValorForaDoIntervaloError

from fastapi import APIRouter, HTTPException, status
from typing import Literal

# Paths dos arquivos de persistência
animal_path = AnimalPath()
router = APIRouter(prefix="/animal", tags=["Animal"])

animal_service = AnimalService(animal_path.cachorro, animal_path.calopsita, animal_path.coelho, animal_path.gato)

@router.post("/{type_animal}", response_model=CachorroResponseSchema | CalopsitaResponseSchema | CoelhoResponseSchema | GatoResponseSchema, status_code=status.HTTP_201_CREATED)
def create(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    payload: CachorroCreateSchema | CalopsitaCreateSchema | CoelhoCreateSchema | GatoCreateSchema
):
    try:
        animal_data = payload.model_dump()

        animal = animal_service.create(type_animal, animal_data)
        
        return animal

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
    
    except TipagemError as e:
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


@router.get("/", response_model=list[AnimalResponseUnion], status_code=status.HTTP_200_OK)
def get_all():
    try:
        animais = animal_service.get_all()
        return animais

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
    
    except TipagemError as e:
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

@router.get("/{type_animal}", response_model=list[CachorroResponseSchema | CalopsitaResponseSchema | CoelhoResponseSchema | GatoResponseSchema], status_code=status.HTTP_200_OK)
def get_all_type_animal(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]
):
    try:
        animais = animal_service.get_all_type_animal(type_animal)
        return animais

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
    
    except TipagemError as e:
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

@router.get("/{type_animal}/{id}", response_model=CachorroResponseSchema | CalopsitaResponseSchema | CoelhoResponseSchema | GatoResponseSchema, status_code=status.HTTP_200_OK)
def get_by_id(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id: int
):
    try:
        animal = animal_service.get_by_id(type_animal, id)
        return animal

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
    
    except TipagemError as e:
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

@router.put("/{type_animal}/{id}", response_model=CachorroResponseSchema | CalopsitaResponseSchema | CoelhoResponseSchema | GatoResponseSchema, status_code=status.HTTP_201_CREATED)
def update(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    payload: CachorroCreateSchema | CalopsitaCreateSchema | CoelhoCreateSchema | GatoCreateSchema,
    id: int
):
    try:
        animal_data = payload.model_dump()

        animal = animal_service.update(type_animal, animal_data, id)
        
        return animal

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
    
    except TipagemError as e:
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

@router.delete("/{type_animal}/{id}", status_code=status.HTTP_200_OK)
def delete_by_id(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id: int
):
    try:
        animal_service.delete_by_id(type_animal, id)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except NaoCadastradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.delete("/{type_animal}", status_code=status.HTTP_200_OK)
def delete_all_type_animal(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]
):
    try:
        animal_service.delete_all(type_animal)

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

