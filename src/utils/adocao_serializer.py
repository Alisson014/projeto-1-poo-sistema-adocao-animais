from src.domain.models.registro import Adocao

def adocao_serializer(adocao:Adocao):
    return {
        "id": adocao.id,
        "animal": adocao.animal.to_dict(),
        "adotante": adocao.adotante.to_dict(),
        "taxa": adocao.taxa,
        "pago": adocao.pago,
        "data": adocao.data.__str__()
    }
