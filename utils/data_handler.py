import json
import os
import time
import hashlib

class DataHandler:
    def __init__(self, arquivo="dados_sensores.json"):
        self.arquivo = arquivo
        self.dados_sensores = {}
        self.tempo_inicio = time.time()
    
    def adicionar_sensor(self, nome_sensor, valor):
        self.dados_sensores[nome_sensor] = {"valor": valor}
    
    def calcular_hash(self, dados):
        dados_str = json.dumps(dados, sort_keys=True)
        return hashlib.sha256(dados_str.encode()).hexdigest()
    
    def gerar_json(self):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        uptime = round(time.time() - self.tempo_inicio, 2)
        
        dados_completos = {
            "timestamp": timestamp,
            "uptime_segundos": uptime,
            "sensores": self.dados_sensores
        }
        
        dados_completos["hash_validacao"] = self.calcular_hash(self.dados_sensores)
        
        return dados_completos
    
    def salvar_json(self):
        dados = self.gerar_json()
        
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
        
        return dados
    
    def limpar_dados(self):
        self.dados_sensores = {}
