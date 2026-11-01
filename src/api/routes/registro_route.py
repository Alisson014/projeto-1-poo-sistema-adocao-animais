from ..schemas import AdocaoCreateSchema, DevolucaoCreateSchema, ReservaCreateSchema, RegistroResponseUnion
from ...services import RegistroService
from ..paths import RegistroPath, AnimalPath, PessoaPath, PoliticaPath
from ...domain.exceptions import TipagemError, NaoCadastradoError, JaCadastradoError, PoliticaError, TransicaoDeEstadoInvalidaError, AnimalIndisponível

from fastapi import APIRouter, HTTPException, status
from typing import Literal

# Paths dos arquivos de persistência
registro_path = RegistroPath()
animal_path = AnimalPath()
pessoa_path = PessoaPath()
politica_path = PoliticaPath()

router = APIRouter(prefix="/registro", tags=["Registro"])

registro_service = RegistroService(
    # Reserva
    registro_path.r_cachorro,
    registro_path.r_calopsita,
    registro_path.r_coelho,
    registro_path.r_gato,

    # Devolução
    registro_path.d_cachorro,
    registro_path.d_calopsita,
    registro_path.d_coelho,
    registro_path.d_gato,

    # Adoção
    registro_path.a_cachorro,
    registro_path.a_calopsita,
    registro_path.a_coelho,
    registro_path.a_gato,

    # Animal
    animal_path.cachorro,
    animal_path.calopsita,
    animal_path.coelho,
    animal_path.gato,

    # Pessoa
    pessoa_path.adotante,

    # Politica
    politica_path.path
)


@router.post("/{type_registro}/{type_animal}", response_model=RegistroResponseUnion, status_code=status.HTTP_201_CREATED)
def create(
    type_registro: Literal["Adocao", "Devolucao", "Reserva"],
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    paylaod: AdocaoCreateSchema | DevolucaoCreateSchema | ReservaCreateSchema
):
    try:
        registro_data = paylaod.model_dump()

        registro = registro_service.create(type_registro, type_animal, registro_data)

        return registro

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
    except PoliticaError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except TransicaoDeEstadoInvalidaError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail="Animal indisponível para essa operação"
        )
    
    except AnimalIndisponível as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail="Animal indisponível para essa operação"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.get("/", response_model=list[RegistroResponseUnion], status_code=status.HTTP_200_OK)
def get_all():
    try:
        registros = registro_service.get_all()

        return registros

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.get("/{type_registro}", response_model=list[RegistroResponseUnion], status_code=status.HTTP_200_OK)
def get_all_type_registro(
    type_registro: Literal["Adocao", "Devolucao", "Reserva"],
):
    try:
        registros = registro_service.get_all_type_registro(type_registro)

        return registros

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.get("/{type_registro}/{type_animal}", response_model=list[RegistroResponseUnion], status_code=status.HTTP_200_OK)
def get_all_type_registro_type_animal(
    type_registro: Literal["Adocao", "Devolucao", "Reserva"],
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
):
    try:
        registros = registro_service.get_all_type_registro_type_animal(type_registro, type_animal)

        return registros

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

@router.get("/{type_registro}/{type_animal}/{id}", response_model=RegistroResponseUnion, status_code=status.HTTP_200_OK)
def get_by_id(
    type_registro: Literal["Adocao", "Devolucao", "Reserva"],
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id: int
):
    try:
        registro = registro_service.get_by_id(type_registro, type_animal, id)

        return registro

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

@router.put("/{type_registro}/{type_animal}/{id}", response_model=RegistroResponseUnion, status_code=status.HTTP_201_CREATED)
def update(
    type_registro: Literal["Adocao", "Devolucao", "Reserva"],
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    paylaod: AdocaoCreateSchema | DevolucaoCreateSchema | ReservaCreateSchema,
    id: int
):
    try:
        registro_data = paylaod.model_dump()

        registro = registro_service.update(type_registro, type_animal, registro_data, id)

        return registro

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
    except PoliticaError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except TransicaoDeEstadoInvalidaError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail="Animal indisponível para essa operação"
        )
    
    except AnimalIndisponível as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail="Animal indisponível para essa operação"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_all():
    try:
        registro_service.delete_all()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )


@router.delete("/{type_registro}", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_type_registro(
    type_registro: Literal["Adocao", "Devolucao", "Reserva"],
):
    try:
        registro_service.delete_all_registro(type_registro)

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


@router.delete("/{type_registro}/{type_animal}/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(
    type_registro: Literal["Adocao", "Devolucao", "Reserva"],
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id: int
):
    try:
        registro_service.delete_by_id(type_registro, type_animal, id)

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
