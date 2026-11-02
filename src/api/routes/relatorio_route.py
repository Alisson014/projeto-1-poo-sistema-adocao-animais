from ..schemas import Top5MaisAdotaveisCreateSchema, TaxaAdocaoCreateSchema, TaxaDevolucoesCreateSchema, RelatorioResponseUnion
from ...services import Top5MaisAdotaveisService, TaxaAdocaoService, TaxaDevolucoesService
from ..paths import RelatorioPath, PoliticaPath
from ...domain import TaxaAdocaoEspecies, TaxaAdocaoPorte, TaxaDevolucoes, TaxaTempoMedioEntradaAdocao
from ...domain.exceptions import RelatorioNaoGeradoError, NaoCadastradoError

from fastapi import APIRouter, HTTPException, status
from typing import Literal


# Paths dos arquivos de persistência
relatorio_path = RelatorioPath()
politica_path = PoliticaPath()

# Mapeamento dos services
SERVICE_MAP: dict[str, Top5MaisAdotaveisService | TaxaAdocaoService | TaxaDevolucoesService] = {
    "Top5MaisAdotaveis": Top5MaisAdotaveisService(relatorio_path.top5_mais_adotaveis, politica_path.path),
    "TaxaAdocaoEspecies": TaxaAdocaoService(relatorio_path.taxa_adocao_especies, TaxaAdocaoEspecies),
    "TaxaAdocaoPorte": TaxaAdocaoService(relatorio_path.taxa_adocao_porte, TaxaAdocaoPorte),
    "TaxaDevolucoes": TaxaDevolucoesService(relatorio_path.taxa_devolucoes),
    "TaxaTempoMedioEntradaAdocao": TaxaAdocaoService(relatorio_path.taxa_tempo_medio_entrada_adocao, TaxaTempoMedioEntradaAdocao)
}

router = APIRouter(prefix="/relatorio", tags=["Relatorio"])


@router.post("/{type_relatorio}", response_model=RelatorioResponseUnion, status_code=status.HTTP_201_CREATED)
def create(
    type_relatorio: Literal["Top5MaisAdotaveis", "TaxaAdocaoEspecies", "TaxaAdocaoPorte", "TaxaDevolucoes", "TaxaTempoMedioEntradaAdocao"],
    payload: Top5MaisAdotaveisCreateSchema | TaxaAdocaoCreateSchema | TaxaDevolucoesCreateSchema
):
    try:
        service = SERVICE_MAP.get(type_relatorio)

        if service is None:
            raise ValueError("Tipo de relatório inválido")
        
        relatorio_data = payload.model_dump()
        
        relatorio = service.create(relatorio_data)

        return relatorio

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except RelatorioNaoGeradoError as e:
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
            detail=str(e)
        )

@router.get("/", response_model=list[RelatorioResponseUnion], status_code=status.HTTP_200_OK)
def get_all():
    try:
        relatorios = []

        for service in SERVICE_MAP.values():
            relatorios.extend(service.get_all())

        return relatorios

    except RelatorioNaoGeradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.get("/{type_relatorio}", response_model=list[RelatorioResponseUnion], status_code=status.HTTP_200_OK)
def get_all_type_relatorio(
    type_relatorio: Literal["Top5MaisAdotaveis", "TaxaAdocaoEspecies", "TaxaAdocaoPorte", "TaxaDevolucoes", "TaxaTempoMedioEntradaAdocao"],
):
    try:
        service = SERVICE_MAP.get(type_relatorio)

        if service is None:
            raise ValueError("Tipo de relatório inválido")
        
        relatorios = service.get_all()

        return relatorios

    except RelatorioNaoGeradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.get("/{type_relatorio}/{id}", response_model=RelatorioResponseUnion, status_code=status.HTTP_200_OK)
def get_by_id(
    type_relatorio: Literal["Top5MaisAdotaveis", "TaxaAdocaoEspecies", "TaxaAdocaoPorte", "TaxaDevolucoes", "TaxaTempoMedioEntradaAdocao"],
    id: int
):
    try:
        service = SERVICE_MAP.get(type_relatorio)

        if service is None:
            raise ValueError("Tipo de relatório inválido")

        relatorio = service.get_by_id(id)

        return relatorio

    except RelatorioNaoGeradoError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.put("/{type_relatorio}/{id}", response_model=RelatorioResponseUnion, status_code=status.HTTP_200_OK)
def update(
    type_relatorio: Literal["Top5MaisAdotaveis", "TaxaAdocaoEspecies", "TaxaAdocaoPorte", "TaxaDevolucoes", "TaxaTempoMedioEntradaAdocao"],
    id: int,
    payload: Top5MaisAdotaveisCreateSchema | TaxaAdocaoCreateSchema | TaxaDevolucoesCreateSchema
):
    try:
        service = SERVICE_MAP.get(type_relatorio)

        if service is None:
            raise ValueError("Tipo de relatório inválido")
        
        relatorio_data = payload.model_dump()
        
        relatorio = service.update(relatorio_data, id)

        return relatorio

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, 
            detail=str(e)
        )
    except RelatorioNaoGeradoError as e:
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
            detail=str(e)
        )

@router.delete("/{type_relatorio}", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_type_relatorio(
    type_relatorio: Literal["Top5MaisAdotaveis", "TaxaAdocaoEspecies", "TaxaAdocaoPorte", "TaxaDevolucoes", "TaxaTempoMedioEntradaAdocao"],
):
    try:
        service = SERVICE_MAP.get(type_relatorio)

        if service is None:
            raise ValueError("Tipo de relatório inválido")
        
        service.delete_all()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )

@router.delete("/{type_relatorio}/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(
    type_relatorio: Literal["Top5MaisAdotaveis", "TaxaAdocaoEspecies", "TaxaAdocaoPorte", "TaxaDevolucoes", "TaxaTempoMedioEntradaAdocao"],
    id: int
):
    try:
        service = SERVICE_MAP.get(type_relatorio)

        if service is None:
            raise ValueError("Tipo de relatório inválido")

        service.delete_by_id(id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )
