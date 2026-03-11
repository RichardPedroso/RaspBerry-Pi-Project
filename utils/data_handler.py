import json
import os
import time
import hashlib
from codecarbon import EmissionsTracker

class DataHandler:
    def __init__(self, arquivo="dados_sensores.json"):
        self.arquivo = arquivo
        self.dados_sensores = {}
        self.tempo_inicio = time.time()
        self.tracker = EmissionsTracker(save_to_file=False, log_level="error")
        self.sensor_ids = {}
    
    def adicionar_sensor(self, nome_sensor, valor):
        if nome_sensor not in self.sensor_ids:
            self.sensor_ids[nome_sensor] = f"{nome_sensor}_{len(self.sensor_ids) + 1}"
        self.dados_sensores[nome_sensor] = {"sensor_id": self.sensor_ids[nome_sensor], "valor": valor}
    
    def calcular_hash(self, dados):
        dados_str = json.dumps(dados, sort_keys=True)
        return hashlib.sha256(dados_str.encode()).hexdigest()
    
    def gerar_json(self, emissions):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        uptime = round(time.time() - self.tempo_inicio, 2)
        
        dados_completos = {
            "timestamp": timestamp,
            "uptime_segundos": uptime,
            "sensores": self.dados_sensores,
            "pegada_carbono_gramas": round(emissions * 1000, 6) if emissions else 0
        }
        
        dados_completos["hash_validacao"] = self.calcular_hash(self.dados_sensores)
        
        return dados_completos
    
    def salvar_json(self, emissions=0):
        dados = self.gerar_json(emissions)
        
        dados_acumulados = []
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r") as f:
                try:
                    dados_acumulados = json.load(f)
                except:
                    dados_acumulados = []
        
        dados_acumulados.append(dados)
        
        with open(self.arquivo, "w") as f:
            json.dump(dados_acumulados, f, indent=4)
        
        # Gerar hash do arquivo JSON completo
        hash_arquivo = self.gerar_hash_arquivo()
        
        return dados, hash_arquivo
    
    def gerar_hash_arquivo(self):
        """Gera hash SHA256 do arquivo JSON completo"""
        with open(self.arquivo, "rb") as f:
            conteudo = f.read()
            return hashlib.sha256(conteudo).hexdigest()
    
    def salvar_hash(self, hash_valor):
        """Salva o hash em arquivo .txt separado"""
        arquivo_hash = self.arquivo.replace(".json", "_hash.txt")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        with open(arquivo_hash, "w") as f:
            f.write(f"Hash SHA256 do arquivo: {self.arquivo}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Hash: {hash_valor}\n")
        
        return arquivo_hash
    
    def limpar_dados(self):
        self.dados_sensores = {}
