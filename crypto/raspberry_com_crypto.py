import board
import adafruit_dht
import RPi.GPIO as GPIO
import time
import json
import os
from crypto_temporario import criptografar_json_automatico

# --- CONFIGURAÇÃO DE PINOS ---
DHT_PIN = board.D4
TOUCH_PIN = 27
LUZ_PIN = 18
NOME_ARQUIVO = "dados_sensores_brutos.json"
WATTS_RASPBERRY_PI = 4.0

# --- INICIALIZAÇÃO ---
dht = adafruit_dht.DHT11(DHT_PIN)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TOUCH_PIN, GPIO.IN)
GPIO.setup(LUZ_PIN, GPIO.IN)

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return round(float(f.read()) / 1000.0, 2)
    except:
        return 0.0

def exportar_para_json(nova_leitura):
    dados_acumulados = []
    if os.path.exists(NOME_ARQUIVO):
        with open(NOME_ARQUIVO, "r") as f:
            try:
                dados_acumulados = json.load(f)
            except:
                dados_acumulados = []
    
    dados_acumulados.append(nova_leitura)
    
    with open(NOME_ARQUIVO, "w") as f:
        json.dump(dados_acumulados, f, indent=4)

# Controle de tempo
tempo_inicio = time.time()
ultima_leitura_dht = 0
estado_toque_anterior = None
contador_leituras = 0
LEITURAS_ANTES_CRIPTOGRAFAR = 6  # 6 leituras = 30 segundos

print(f"Sistema de Coleta Ativo. Gravando em: {NOME_ARQUIVO}")
print(f"Após {LEITURAS_ANTES_CRIPTOGRAFAR} leituras, os dados serão criptografados.\n")

try:
    while True:
        agora = time.time()

        # 1. LEITURA DE EVENTO: TOQUE
        estado_toque = GPIO.input(TOUCH_PIN)
        if estado_toque != estado_toque_anterior:
            print(f"Mudança detectada no toque: {estado_toque}")
            estado_toque_anterior = estado_toque

        # 2. LEITURA PERIÓDICA: SENSORES (A cada 5 segundos)
        if agora - ultima_leitura_dht > 5.0:
            try:
                # Coleta
                temp_ar = dht.temperature
                umid_ar = dht.humidity
                temp_cpu = get_cpu_temp()
                luz = GPIO.input(LUZ_PIN)
                uptime = round(agora - tempo_inicio, 2)

                # Estrutura de exportação
                leitura = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "uptime_segundos": uptime,
                    "sensores": {
                        "temperatura_ar": temp_ar,
                        "umidade_ar": umid_ar,
                        "luminosidade_digital": luz,
                        "toque_estado": estado_toque
                    },
                    "hardware": {
                        "temperatura_cpu": temp_cpu
                    },
                    "calculo_pegada_carbono": {
                        "descricao": "Dados necessários para calcular emissão de CO2",
                        "potencia_consumida_watts": WATTS_RASPBERRY_PI,
                        "unidade_potencia": "W (Watts)",
                        "tempo_operacao_segundos": uptime,
                        "unidade_tempo": "segundos",
                        "formula_kwh": "(potencia_consumida_watts * tempo_operacao_segundos) / 3600",
                        "formula_co2_kg": "kwh * fator_emissao_regional",
                        "fator_emissao_sugerido_brasil": 0.0917,
                        "unidade_fator_emissao": "kg CO2 por kWh"
                    }
                }

                exportar_para_json(leitura)
                contador_leituras += 1
                print(f"[{contador_leituras}/{LEITURAS_ANTES_CRIPTOGRAFAR}] Dados enviados para JSON -> Uptime: {uptime}s | Temp: {temp_ar}°C")

                # CRIPTOGRAFAR após N leituras
                if contador_leituras >= LEITURAS_ANTES_CRIPTOGRAFAR:
                    print("\n" + "="*60)
                    print("🔐 INICIANDO CRIPTOGRAFIA DOS DADOS")
                    print("="*60 + "\n")
                    
                    arquivo_cripto, senha = criptografar_json_automatico(NOME_ARQUIVO)
                    
                    print("📤 ARQUIVOS PARA ENVIAR AO OUTRO GRUPO:")
                    print(f"   1. {arquivo_cripto}")
                    print(f"   2. salt.bin")
                    print(f"   3. SENHA_PARA_GRUPO_[timestamp].txt\n")
                    
                    print("✅ Processo concluído! Encerrando coleta...")
                    break

            except RuntimeError:
                pass
            
            ultima_leitura_dht = agora

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nColeta interrompida pelo usuário.")
finally:
    dht.exit()
    GPIO.cleanup()
