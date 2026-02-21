import time
from utils.data_handler import DataHandler
from utils.crypto_handler import criptografar_json

# Importar sensores (comente a linha para desabilitar um sensor)
from sensores import sensor_umid_temp
from sensores import sensor_de_presenca
from sensores import sensor_luminosidade

# Configurações
INTERVALO_LEITURA = 5  # segundos
LEITURAS_ANTES_CRIPTOGRAFAR = 6

def main():
    print("=== Sistema de Coleta de Sensores ===\n")
    
    # Inicializar sensores
    sensores_ativos = []
    
    if sensor_umid_temp.inicializar():
        sensores_ativos.append(("Umidade/Temperatura", sensor_umid_temp))
        print("✓ Sensor Umidade/Temperatura inicializado")
    
    if sensor_de_presenca.inicializar():
        sensores_ativos.append(("Presença", sensor_de_presenca))
        print("✓ Sensor Presença inicializado")
    
    if sensor_luminosidade.inicializar():
        sensores_ativos.append(("Luminosidade", sensor_luminosidade))
        print("✓ Sensor Luminosidade inicializado")
    
    if not sensores_ativos:
        print("\n❌ Nenhum sensor foi inicializado. Encerrando...")
        return
    
    print(f"\n{len(sensores_ativos)} sensor(es) ativo(s)\n")
    
    # Inicializar gerenciador de dados
    data_handler = DataHandler()
    contador_leituras = 0
    
    try:
        while True:
            print(f"[Leitura {contador_leituras + 1}/{LEITURAS_ANTES_CRIPTOGRAFAR}]")
            
            # Coletar dados de todos os sensores ativos
            for nome, sensor in sensores_ativos:
                dados = sensor.ler_dados()
                if dados:
                    for chave, valor in dados.items():
                        data_handler.adicionar_sensor(chave, valor)
                        print(f"  {chave}: {valor}")
            
            # Salvar JSON
            dados_salvos = data_handler.salvar_json()
            print(f"✓ Dados salvos em JSON\n")
            
            contador_leituras += 1
            
            # Criptografar após N leituras
            if contador_leituras >= LEITURAS_ANTES_CRIPTOGRAFAR:
                print("="*60)
                print("🔐 INICIANDO CRIPTOGRAFIA DOS DADOS")
                print("="*60)
                
                criptografar_json(data_handler.arquivo)
                
                print("✅ Processo concluído!")
                break
            
            # Limpar dados para próxima leitura
            data_handler.limpar_dados()
            
            # Aguardar próxima leitura
            time.sleep(INTERVALO_LEITURA)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Coleta interrompida pelo usuário")
    
    finally:
        # Finalizar sensores
        print("\nFinalizando sensores...")
        for nome, sensor in sensores_ativos:
            sensor.finalizar()
        print("✓ Sistema encerrado\n")

if __name__ == "__main__":
    main()
