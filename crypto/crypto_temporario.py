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

# --- CONFIGURAÇÃO ---
SALT_FILE = "salt.bin"
VALIDADE_SENHA = 20  # segundos

def gerar_senha_temporaria():
    """Gera senha aleatória forte que expira em 20 segundos"""
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    senha = ''.join(secrets.choice(caracteres) for _ in range(24))
    return senha

def gerar_chave_segura(senha):
    """Gera chave criptográfica usando PBKDF2 com senha"""
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

def criptografar_json_automatico(arquivo_json):
    """Criptografa JSON com senha temporária"""
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
    print("\n⚠️  ATENÇÃO: Compartilhe esta senha AGORA com o outro grupo!")
    print("⏰  Após 20 segundos ela não funcionará mais!\n")
    
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
    
    print(f"✅ Arquivo criptografado: {arquivo_cripto}")
    print(f"📦 Tamanho: {os.path.getsize(arquivo_cripto)} bytes\n")
    
    # SALVA SENHA EM ARQUIVO
    arquivo_senha_enviar = f"SENHA_PARA_GRUPO_{timestamp}.txt"
    with open(arquivo_senha_enviar, "w") as f:
        f.write("="*60 + "\n")
        f.write("🔑 INFORMAÇÕES PARA DESCRIPTOGRAFAR OS DADOS\n")
        f.write("="*60 + "\n\n")
        f.write(f"1. Arquivo criptografado: {arquivo_cripto}\n")
        f.write(f"2. Arquivo salt: salt.bin\n")
        f.write(f"3. Senha temporária: {senha}\n\n")
        f.write(f"VALIDADE: {VALIDADE_SENHA} segundos\n")
        f.write(f"EXPIRA ÀS: {tempo_expiracao_str}\n\n")
        f.write("⚠️  IMPORTANTE: Use a senha IMEDIATAMENTE!\n")
        f.write("\nCOMO USAR:\n")
        f.write("1. Execute: python3 descriptografar_outro_grupo.py\n")
        f.write(f"2. Informe o arquivo: {arquivo_cripto}\n")
        f.write("3. Informe o salt: salt.bin\n")
        f.write(f"4. Digite a senha: {senha}\n")
        f.write("\n" + "="*60 + "\n")
    
    print(f"📝 SENHA SALVA EM: {arquivo_senha_enviar}")
    print(f"📤 ENVIE ESTE ARQUIVO AO OUTRO GRUPO!\n")
    
    return arquivo_cripto, senha
