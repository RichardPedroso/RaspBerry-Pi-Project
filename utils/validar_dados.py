import json
import hashlib

def validar_hash(dados_json):
    """Valida se o hash dos dados corresponde ao hash_validacao"""
    if "hash_validacao" not in dados_json:
        return False, "Hash de validação não encontrado"
    
    hash_recebido = dados_json["hash_validacao"]
    sensores = dados_json.get("sensores", {})
    
    dados_str = json.dumps(sensores, sort_keys=True)
    hash_calculado = hashlib.sha256(dados_str.encode()).hexdigest()
    
    if hash_recebido == hash_calculado:
        return True, "Dados íntegros e válidos"
    else:
        return False, "Dados foram alterados ou corrompidos"

def validar_arquivo(arquivo_json):
    """Valida todos os registros de um arquivo JSON"""
    with open(arquivo_json, "r") as f:
        dados = json.load(f)
    
    if isinstance(dados, list):
        resultados = []
        for i, registro in enumerate(dados):
            valido, msg = validar_hash(registro)
            resultados.append((i, valido, msg))
        return resultados
    else:
        return [validar_hash(dados)]
