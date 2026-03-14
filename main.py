import time
import subprocess
import os
import logging
from utils.data_handler import DataHandler

# Importar sensores (comente a linha para desabilitar um sensor)
from sensores import sensor_umid_temp
from sensores import sensor_de_presenca
from sensores import sensor_luminosidade

# Configurações
INTERVALO_LEITURA = 5  # segundos
TOTAL_LEITURAS = 6
INTERVALO_ENTRE_CICLOS = 60  # 1 minuto
SCP_DESTINO = "aluno@192.168.0.2:/home/aluno/Desktop/projeto/"

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[logging.FileHandler('envios.log')]
)

def coletar_e_enviar():
    """Executa um ciclo completo de coleta e envio"""
    sensores_ativos = []
    data_handler = None
    
    if sensor_umid_temp.inicializar():
        sensores_ativos.append(("Umidade/Temperatura", sensor_umid_temp))
    
    if sensor_de_presenca.inicializar():
        sensores_ativos.append(("Presença", sensor_de_presenca))
    
    if sensor_luminosidade.inicializar():
        sensores_ativos.append(("Luminosidade", sensor_luminosidade))
    
    if not sensores_ativos:
        logging.error("Nenhum sensor inicializado")
        print("❌ Nenhum sensor inicializado")
        return
    
    print(f"{len(sensores_ativos)} sensor(es) ativo(s)")
    
    data_handler = DataHandler()
    data_handler.iniciar_tracker()
    contador_leituras = 0
    
    try:
        while True:
            print(f"Leitura {contador_leituras + 1}/{TOTAL_LEITURAS}")
            
            for nome, sensor in sensores_ativos:
                dados = sensor.ler_dados()
                if dados:
                    for chave, valor in dados.items():
                        data_handler.adicionar_sensor(chave, valor)
            
            emissions = data_handler.parar_tracker()
            data_handler.iniciar_tracker()
            data_handler.salvar_json(emissions)
            
            contador_leituras += 1
            
            if contador_leituras >= TOTAL_LEITURAS:
                print("✅ Coleta concluída")
                
                hash_arquivo = data_handler.gerar_hash_arquivo()
                data_handler.salvar_hash(hash_arquivo)
                
                arquivo_json = os.path.abspath(data_handler.arquivo)
                arquivo_hash = arquivo_json.replace(".json", "_hash.txt")
                
                print("📤 Enviando arquivos...")
                
                try:
                    logging.info(f"Enviando: {arquivo_json} -> {SCP_DESTINO}")
                    resultado_json = subprocess.run(
                        ["scp", arquivo_json, SCP_DESTINO],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if resultado_json.returncode == 0:
                        logging.info(f"✓ JSON enviado")
                        print("✅ JSON enviado")
                    else:
                        logging.error(f"Erro JSON: {resultado_json.stderr}")
                except Exception as e:
                    logging.error(f"Falha JSON: {e}")
                
                try:
                    logging.info(f"Enviando: {arquivo_hash} -> {SCP_DESTINO}")
                    resultado_hash = subprocess.run(
                        ["scp", arquivo_hash, SCP_DESTINO],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if resultado_hash.returncode == 0:
                        logging.info(f"✓ Hash enviado")
                        print("✅ Hash enviado")
                    else:
                        logging.error(f"Erro Hash: {resultado_hash.stderr}")
                except Exception as e:
                    logging.error(f"Falha Hash: {e}")
                
                data_handler.limpar_arquivo_json()
                logging.info("Ciclo concluído")
                break
            
            data_handler.limpar_dados()
            time.sleep(INTERVALO_LEITURA)
    
    except KeyboardInterrupt:
        print("\n⚠️ Interrompido")
    
    finally:
        if data_handler:
            data_handler.parar_tracker()
        for nome, sensor in sensores_ativos:
            sensor.finalizar()

if __name__ == "__main__":
    logging.info("Sistema iniciado")
    print("=== SISTEMA DE COLETA CONTÍNUA ===")
    print(f"Intervalo: {INTERVALO_ENTRE_CICLOS}s\n")
    
    ciclo = 1
    try:
        while True:
            print(f"[CICLO {ciclo}]")
            logging.info(f"Ciclo {ciclo} iniciado")
            
            coletar_e_enviar()
            
            print(f"\n⏳ Aguardando {INTERVALO_ENTRE_CICLOS}s...\n")
            time.sleep(INTERVALO_ENTRE_CICLOS)
            
            ciclo += 1
    
    except KeyboardInterrupt:
        print("\n✓ Encerrado")
        logging.info("Sistema encerrado")
