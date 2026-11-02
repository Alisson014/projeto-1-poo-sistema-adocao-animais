from ..schemas import FilaEsperaSchema, EntradaFilaSchema
from ...services import FilaEsperaService
from ..paths import FilaEsperaPath, PessoaPath, PoliticaPath, AnimalPath
from ...domain import Cachorro, Calopsita, Coelho, Gato
from ...domain.exceptions import TipagemError, NaoEncontradoError, NaoCadastradoError

from fastapi import APIRouter, HTTPException, status
from typing import Literal

# Paths dos arquivos de persistência
fila_espera_path = FilaEsperaPath()
pessoa_path = PessoaPath()
politica_path = PoliticaPath()
animal_path = AnimalPath()

# Mapeamento dos services
SERVICE_MAP: dict[str, FilaEsperaService] = {
    "Cachorro": FilaEsperaService(fila_espera_path.fila_cachorro_path, Cachorro, animal_path.cachorro, pessoa_path.adotante, politica_path.path),
    "Calopsita": FilaEsperaService(fila_espera_path.fila_calopsita_path, Calopsita, animal_path.calopsita, pessoa_path.adotante, politica_path.path),
    "Coelho": FilaEsperaService(fila_espera_path.fila_coelho_path, Coelho, animal_path.coelho, pessoa_path.adotante, politica_path.path),
    "Gato": FilaEsperaService(fila_espera_path.fila_gato_path, Gato, animal_path.gato, pessoa_path.adotante, politica_path.path)
}


router = APIRouter(prefix="/fila-espera", tags=["Fila Espera"])

@router.post("/{type_animal}/{id_animal}", response_model=FilaEsperaSchema, status_code=status.HTTP_201_CREATED)
def create(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id_animal: int
):
    try:
        service = SERVICE_MAP.get(type_animal)

        if service is None:
            raise ValueError("Tipo de animal inválido")

        fila = service.create(id_animal)

        return fila

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
    except NaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
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
            detail=str(e)
        )

@router.get("/", response_model=list[FilaEsperaSchema], status_code=status.HTTP_200_OK)
def get_all():
    try:
        filas = []

        for service in SERVICE_MAP.values():
            filas.extend( service.get_all() )

        return filas
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.get("/{type_animal}", response_model=list[FilaEsperaSchema], status_code=status.HTTP_200_OK)
def get_all_type_animal(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]
):
    try:
        service = SERVICE_MAP.get(type_animal)

        if service is None:
            raise ValueError("Tipo de animal inválido")

        filas = service.get_all()

        return filas
    
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

@router.get("/{type_animal}/{id_animal}", response_model=FilaEsperaSchema, status_code=status.HTTP_200_OK)
def get_by_id(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id_animal: int
):
    try:
        service = SERVICE_MAP.get(type_animal)

        if service is None:
            raise ValueError("Tipo de animal inválido")

        fila = service.get_by_animal_id(id_animal)

        return fila
    
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
    except NaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.get("/proximo-fila/{type_animal}/{id_animal}", response_model=EntradaFilaSchema, status_code=status.HTTP_200_OK)
def proximo(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id_animal: int
):
    try:
        service = SERVICE_MAP.get(type_animal)

        if service is None:
            raise ValueError("Tipo de animal inválido")

        proximo = service.proximo(id_animal)

        if proximo is None:
            raise NaoEncontradoError("Não existem entradas cadastradas")

        return proximo
    
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
    except NaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.put("/add-adotante/{type_animal}/{id_animal}/{adotante_email}", response_model=FilaEsperaSchema, status_code=status.HTTP_200_OK)
def add_adotante(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id_animal: int,
    adotante_email: str
):
    try:
        service = SERVICE_MAP.get(type_animal)

        if service is None:
            raise ValueError("Tipo de animal inválido")

        fila = service.add_adotante(id_animal, adotante_email)

        return fila

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
    except NaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
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
            detail=str(e)
        )

@router.put("/remove-adotante/{type_animal}/{id_animal}/{adotante_email}", response_model=FilaEsperaSchema, status_code=status.HTTP_200_OK)
def remove_adotante(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id_animal: int,
    adotante_email: str
):
    try:
        service = SERVICE_MAP.get(type_animal)

        if service is None:
            raise ValueError("Tipo de animal inválido")

        fila = service.remove_adotante(id_animal, adotante_email)

        return fila

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
    except NaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
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
            detail=str(e)
        )

@router.delete("/{type_animal}", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_type_animal(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"]
):
    try:
        service = SERVICE_MAP.get(type_animal)

        if service is None:
            raise ValueError("Tipo de animal inválido")

        service.delete_all()
    
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

@router.delete("/{type_animal}/{id_animal}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(
    type_animal: Literal["Cachorro", "Calopsita", "Coelho", "Gato"],
    id_animal: int
):
    try:
        service = SERVICE_MAP.get(type_animal)

        if service is None:
            raise ValueError("Tipo de animal inválido")

        service.delete_by_animal_id(id_animal)
    
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
    except NaoEncontradoError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
