from ..schemas import IdadeMinimaSchema, DuracaoReservaSchema, PorteXAreaSchema, PesosCompatibilidadeSchema, PoliticaUnion
from ...services import PoliticaService
from ..paths import PoliticaPath
from ...domain.exceptions import TipagemError, ValorForaDoIntervaloError, NaoCadastradoError, JaCadastradoError

from fastapi import APIRouter, HTTPException, status
from typing import Literal

# Paths dos arquivos de persistência
politica_path = PoliticaPath()

politica_service = PoliticaService(politica_path.path)

router = APIRouter(prefix="/politica", tags=["Politica"])


@router.post("/{type_politica}", response_model=PoliticaUnion, status_code=status.HTTP_201_CREATED)
def create(
    type_politica: Literal["IdadeMinima", "DuracaoReserva", "PesosCompatibilidade", "PorteXArea"],
    payload: IdadeMinimaSchema | DuracaoReservaSchema | PorteXAreaSchema | PesosCompatibilidadeSchema,
):
    try:
        politica_data = payload.model_dump()

        politica = politica_service.create(type_politica, politica_data)
        
        return politica

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

@router.get("/", response_model=list[PoliticaUnion], status_code=status.HTTP_200_OK)
def get_all():
    try:
        politicas = politica_service.get_all()
        return politicas
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )

@router.get("/politica/{name}", response_model=PoliticaUnion, status_code=status.HTTP_200_OK)
def get_by_name(
        name: Literal["IdadeMinima", "DuracaoReserva", "PesosCompatibilidade", "PorteXArea"],
    ):
    try:
        politica = politica_service.get_by_name(name)
        return politica
    
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

@router.put("/{type_politica}", response_model=PoliticaUnion, status_code=status.HTTP_200_OK)
def update(
    type_politica: Literal["IdadeMinima", "DuracaoReserva", "PesosCompatibilidade", "PorteXArea"],
    payload: PoliticaUnion,
):
    try:
        politica_data = payload.model_dump()

        politica = politica_service.update(type_politica, politica_data)
        
        return politica

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

@router.delete("/politica/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_name(
        name: Literal["IdadeMinima", "DuracaoReserva", "PesosCompatibilidade", "PorteXArea"],
    ):
    try:
        politica_service.delete_by_name(name)
    
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

@router.delete("/politica", status_code=status.HTTP_204_NO_CONTENT)
def delete_all():
    try:
        politica_service.delete_all()
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Erro interno ao processar o cadastro."
        )
