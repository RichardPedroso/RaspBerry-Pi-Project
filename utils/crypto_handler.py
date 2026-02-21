from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import json
import base64
import os
import time
import secrets
import string

SALT_FILE = "salt.bin"
VALIDADE_SENHA = 30

def gerar_senha_temporaria():
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    senha = ''.join(secrets.choice(caracteres) for _ in range(24))
    return senha

def gerar_chave_segura(senha):
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, "rb") as f:
            salt = f.read()
    else:
        salt = os.urandom(16)
        with open(SALT_FILE, "wb") as f:
            f.write(salt)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    chave = base64.urlsafe_b64encode(kdf.derive(senha.encode()))
    return chave

def criptografar_json(arquivo_json):
    senha = gerar_senha_temporaria()
    expiracao = time.time() + VALIDADE_SENHA
    tempo_expiracao_str = time.strftime("%H:%M:%S", time.localtime(expiracao))
    
    print("\n" + "="*60)
    print("🔐 SENHA TEMPORÁRIA GERADA")
    print("="*60)
    print(f"Senha: {senha}")
    print(f"Validade: {VALIDADE_SENHA} segundos")
    print(f"Expira às: {tempo_expiracao_str}")
    print("="*60)
    
    chave = gerar_chave_segura(senha)
    
    with open(arquivo_json, "r") as f:
        dados = json.load(f)
    
    dados_str = json.dumps(dados, ensure_ascii=False)
    
    fernet = Fernet(chave)
    dados_criptografados = fernet.encrypt(dados_str.encode())
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    arquivo_cripto = f"dados_criptografados_{timestamp}.bin"
    with open(arquivo_cripto, "wb") as f:
        f.write(dados_criptografados)
    
    print(f"\n✅ Arquivo criptografado: {arquivo_cripto}")
    
    arquivo_senha = f"SENHA_PARA_GRUPO_{timestamp}.txt"
    with open(arquivo_senha, "w") as f:
        f.write(f"Arquivo: {arquivo_cripto}\n")
        f.write(f"Salt: salt.bin\n")
        f.write(f"Senha: {senha}\n")
        f.write(f"Validade: {VALIDADE_SENHA}s\n")
    
    print(f"📝 Senha salva em: {arquivo_senha}\n")
    
    return arquivo_cripto, senha
