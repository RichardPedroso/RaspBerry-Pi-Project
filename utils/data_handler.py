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
        
        return dados
    
    def limpar_dados(self):
        self.dados_sensores = {}
