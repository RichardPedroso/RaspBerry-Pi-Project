#!/usr/bin/env python3
import hashlib
import sys
import os

def calcular_hash_arquivo(arquivo):
    """Calcula hash SHA256 de um arquivo"""
    with open(arquivo, "rb") as f:
        conteudo = f.read()
        return hashlib.sha256(conteudo).hexdigest()

def validar_hash(arquivo_json, arquivo_hash):
    """Valida se o hash do JSON corresponde ao hash no arquivo .txt"""
    
    if not os.path.exists(arquivo_json):
        print(f"❌ Arquivo não encontrado: {arquivo_json}")
        return False
    
    if not os.path.exists(arquivo_hash):
        print(f"❌ Arquivo de hash não encontrado: {arquivo_hash}")
        return False
    
    # Calcular hash do arquivo JSON
    hash_calculado = calcular_hash_arquivo(arquivo_json)
    
    # Ler hash do arquivo .txt
    with open(arquivo_hash, "r") as f:
        hash_original = f.read().strip()
    
    if not hash_original:
        print("❌ Hash não encontrado no arquivo .txt")
        return False
    
    # Comparar hashes
    print(f"Hash Original:  {hash_original}")
    print(f"Hash Calculado: {hash_calculado}")
    
    if hash_calculado == hash_original:
        print("\n✅ VALIDAÇÃO APROVADA: Os dados NÃO foram alterados!")
        return True
    else:
        print("\n❌ VALIDAÇÃO FALHOU: Os dados FORAM ALTERADOS!")
        return False

if __name__ == "__main__":
    print("=== VALIDADOR DE INTEGRIDADE DE DADOS ===\n")
    
    if len(sys.argv) < 2:
        print("Uso: python3 validar_hash.py <arquivo.json>")
        print("Exemplo: python3 validar_hash.py dados_sensores.json")
        sys.exit(1)
    
    arquivo_json = sys.argv[1]
    arquivo_hash = arquivo_json.replace(".json", "_hash.txt")
    
    validar_hash(arquivo_json, arquivo_hash)
