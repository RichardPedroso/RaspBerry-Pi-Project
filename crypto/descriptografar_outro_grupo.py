from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import json
import base64
import os

print("\n" + "="*70)
print("🔓 DESCRIPTOGRAFADOR DE DADOS - GRUPO DE CÁLCULO DE CARBONO")
print("="*70)
print("\n📋 INSTRUÇÕES:")
print("   1. Você recebeu um arquivo .bin criptografado")
print("   2. Você recebeu uma senha temporária (válida por 20 segundos)")
print("   3. Você também precisa do arquivo 'salt.bin'")
print("\n⚠️  IMPORTANTE: Use a senha IMEDIATAMENTE após receber!")
print("="*70 + "\n")

def gerar_chave_segura(senha, salt):
    """Gera chave criptográfica usando PBKDF2 com senha"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    chave = base64.urlsafe_b64encode(kdf.derive(senha.encode()))
    return chave

def descriptografar_dados(arquivo_cripto, senha, arquivo_salt):
    """Descriptografa os dados usando a senha temporária"""
    try:
        with open(arquivo_salt, "rb") as f:
            salt = f.read()
        
        chave = gerar_chave_segura(senha, salt)
        
        with open(arquivo_cripto, "rb") as f:
            dados_criptografados = f.read()
        
        fernet = Fernet(chave)
        dados_str = fernet.decrypt(dados_criptografados).decode()
        
        dados = json.loads(dados_str)
        
        return dados, True
    
    except Exception as e:
        return str(e), False

if __name__ == "__main__":
    print("🔐 Iniciando descriptografia...\n")
    
    arquivo_criptografado = input("📁 Nome do arquivo criptografado (.bin): ").strip()
    arquivo_salt = input("📁 Nome do arquivo salt (salt.bin): ").strip()
    senha_temporaria = input("🔑 Digite a senha temporária: ").strip()
    
    print("\n⏳ Descriptografando...\n")
    
    dados, sucesso = descriptografar_dados(arquivo_criptografado, senha_temporaria, arquivo_salt)
    
    if sucesso:
        print("✅ DESCRIPTOGRAFIA BEM-SUCEDIDA!\n")
        print(f"📊 Total de registros: {len(dados)}")
        
        arquivo_saida = "dados_descriptografados.json"
        with open(arquivo_saida, "w") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        
        print(f"💾 Dados salvos em: {arquivo_saida}")
        
        if len(dados) > 0:
            print("\n📋 Exemplo do primeiro registro:")
            print(json.dumps(dados[0], indent=2, ensure_ascii=False))
            
            if "calculo_pegada_carbono" in dados[0]:
                print("\n🌱 Dados para cálculo de carbono encontrados:")
                carbono = dados[0]["calculo_pegada_carbono"]
                print(f"   Potência: {carbono['potencia_consumida_watts']} W")
                print(f"   Tempo: {carbono['tempo_operacao_segundos']} segundos")
                print(f"   Fórmula kWh: {carbono['formula_kwh']}")
                print(f"   Fórmula CO2: {carbono['formula_co2_kg']}")
    else:
        print("❌ ERRO NA DESCRIPTOGRAFIA!")
        print(f"   Motivo: {dados}")
        print("\n💡 Possíveis causas:")
        print("   - Senha incorreta")
        print("   - Senha expirada (mais de 20 segundos)")
        print("   - Arquivo salt.bin incorreto")
        print("   - Arquivo criptografado corrompido")

print("\n" + "="*70)
