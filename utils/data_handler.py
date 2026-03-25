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
        self.tracker = None
        self.sensor_ids = {}
        self.contador_coleta = 0
    
    def iniciar_tracker(self):
        """Inicializa o tracker de emissões"""
        if self.tracker is None:
            self.tracker = EmissionsTracker(save_to_file=False, log_level="error")
        self.tracker.start()
    
    def parar_tracker(self):
        """Para o tracker e retorna as emissões"""
        if self.tracker:
            return self.tracker.stop()
        return 0
    
    def adicionar_sensor(self, nome_sensor, valor):
        if nome_sensor not in self.sensor_ids:
            self.sensor_ids[nome_sensor] = f"{nome_sensor}_{len(self.sensor_ids) + 1}"
        self.dados_sensores[nome_sensor] = {"sensor_id": self.sensor_ids[nome_sensor], "valor": valor}
    
    def gerar_json(self, emissions):
        self.contador_coleta += 1
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        uptime = round(time.time() - self.tempo_inicio, 2)
        
        id_coleta = f"coleta_{self.contador_coleta}"
        
        dados_completos = {
            id_coleta: {
                "timestamp": timestamp,
                "uptime_segundos": uptime,
                "sensores": self.dados_sensores,
                "pegada_carbono_gramas": round(emissions * 1000, 6) if emissions else 0
            }
        }
        
        return dados_completos
    
    def salvar_json(self, emissions=0):
        dados = self.gerar_json(emissions)
        
        dados_acumulados = {}
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r") as f:
                try:
                    dados_acumulados = json.load(f)
                except:
                    dados_acumulados = {}
        
        dados_acumulados.update(dados)
        
        with open(self.arquivo, "w") as f:
            json.dump(dados_acumulados, f, indent=4)
        
        return dados, None
    
    def limpar_arquivo_json(self):
        """Limpa o arquivo JSON para iniciar novo ciclo"""
        if os.path.exists(self.arquivo):
            os.remove(self.arquivo)
        arquivo_hash = self.arquivo.replace(".json", "_hash.txt")
        if os.path.exists(arquivo_hash):
            os.remove(arquivo_hash)
        self.contador_coleta = 0
    
    def gerar_hash_arquivo(self):
        """Gera hash SHA256 do arquivo JSON completo"""
        with open(self.arquivo, "rb") as f:
            conteudo = f.read()
            return hashlib.sha256(conteudo).hexdigest()
    
    def salvar_hash(self, hash_valor):
        """Salva o hash em arquivo .txt separado"""
        arquivo_hash = self.arquivo.replace(".json", "_hash.txt")
        
        try:
            # Remover arquivo existente se houver problema de permissão
            if os.path.exists(arquivo_hash):
                os.chmod(arquivo_hash, 0o666)
            
            with open(arquivo_hash, "w") as f:
                f.write(hash_valor)
            
            return arquivo_hash
        except PermissionError:
            # Tentar em diretório temporário
            arquivo_hash = f"/tmp/{os.path.basename(arquivo_hash)}"
            with open(arquivo_hash, "w") as f:
                f.write(hash_valor)
            return arquivo_hash
    
    def limpar_dados(self):
        self.dados_sensores = {}
