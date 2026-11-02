from src.domain.models.registro import Devolucao

def devolucao_serializer(adocao:Devolucao):
    return {
        "id": adocao.id,
        "animal": adocao.animal.to_dict(),
        "adotante": adocao.adotante.to_dict(),
        "motivo": adocao.motivo,
        "data": adocao.data.__str__()
    }
