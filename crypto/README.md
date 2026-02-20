# Sistema de Criptografia - Raspberry Pi 3

## 📚 Documentação do Projeto

### 📄 Arquivos do Sistema:

1. **raspberry_com_crypto.py** - Programa principal para Raspberry Pi
2. **crypto_temporario.py** - Biblioteca de funções de criptografia
3. **descriptografar_outro_grupo.py** - Programa para descriptografar (outro grupo)
4. **requirements.txt** - Dependências necessárias
5. **ESPECIFICACAO_CRIPTOGRAFIA.txt** - Documentação técnica completa

---

## 🚀 Como Usar no Raspberry Pi

### 1️⃣ Instalar Dependências:

```bash
cd crypto
pip3 install -r requirements.txt
```

Ou no Raspberry Pi:
```bash
sudo apt-get install python3-cryptography
```

### 2️⃣ Executar o Programa:

```bash
python3 raspberry_com_crypto.py
```

### 3️⃣ O que o programa faz:

- Coleta dados dos sensores por 30 segundos (6 leituras)
- Criptografa automaticamente os dados
- Gera senha temporária válida por 20 segundos
- Cria arquivo com senha e instruções

### 4️⃣ Arquivos Gerados:

- `dados_criptografados_[timestamp].bin` - Dados criptografados
- `salt.bin` - Salt para descriptografia
- `SENHA_PARA_GRUPO_[timestamp].txt` - Senha e instruções

### 5️⃣ Enviar ao Outro Grupo:

1. Arquivo `.bin` criptografado
2. Arquivo `salt.bin`
3. Arquivo `SENHA_PARA_GRUPO_[timestamp].txt`

---

## 🔓 Como o Outro Grupo Descriptografa

### 1️⃣ Instalar Dependências:

```bash
pip3 install cryptography
```

### 2️⃣ Executar o Descriptografador:

```bash
python3 descriptografar_outro_grupo.py
```

### 3️⃣ Informar:

- Nome do arquivo criptografado (.bin)
- Nome do arquivo salt (salt.bin)
- Senha temporária (usar em até 20 segundos)

### 4️⃣ Resultado:

- Arquivo `dados_descriptografados.json` com todos os dados

---

## 🔐 Criptografia Utilizada

**Algoritmo:** AES-256 (Fernet)  
**Derivação de Chave:** PBKDF2-HMAC-SHA256  
**Iterações:** 100.000  
**Senha Temporária:** 20 segundos  

Veja detalhes completos em: `ESPECIFICACAO_CRIPTOGRAFIA.txt`

---

## ⚠️ Importante

- A senha expira em 20 segundos
- Compartilhe a senha IMEDIATAMENTE com o outro grupo
- O outro grupo deve usar a senha RAPIDAMENTE
- Envie o arquivo `salt.bin` junto com o arquivo criptografado

---

## 📊 Dados Coletados

O sistema coleta e criptografa:

- Temperatura do ar (°C)
- Umidade do ar (%)
- Luminosidade (digital)
- Estado do sensor de toque
- Temperatura da CPU (°C)
- Dados para cálculo de pegada de carbono

---

## 🛡️ Segurança

- Padrão militar (AES-256)
- Praticamente impossível de quebrar sem a senha
- Senha temporária adiciona camada extra de segurança
- Levaria milhões de anos para quebrar com força bruta
