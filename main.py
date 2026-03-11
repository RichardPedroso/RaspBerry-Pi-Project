import time
import subprocess
import os
from utils.data_handler import DataHandler

# Importar sensores (comente a linha para desabilitar um sensor)
from sensores import sensor_umid_temp
from sensores import sensor_de_presenca
from sensores import sensor_luminosidade

# Configurações
INTERVALO_LEITURA = 5  # segundos
TOTAL_LEITURAS = 6
SCP_DESTINO = "aluno@192.168.0.2:/home/aluno/Desktop/projeto"

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
    data_handler.tracker.start()
    contador_leituras = 0
    
    try:
        while True:
            print(f"[Leitura {contador_leituras + 1}/{TOTAL_LEITURAS}]")
            
            # Coletar dados de todos os sensores ativos
            for nome, sensor in sensores_ativos:
                dados = sensor.ler_dados()
                if dados:
                    for chave, valor in dados.items():
                        data_handler.adicionar_sensor(chave, valor)
                        print(f"  {chave}: {valor}")
            
            # Salvar JSON
            emissions = data_handler.tracker.stop()
            data_handler.tracker.start()
            dados_salvos = data_handler.salvar_json(emissions)
            print(f"✓ Dados salvos em JSON\n")
            
            contador_leituras += 1
            
            # Finalizar após N leituras
            if contador_leituras >= TOTAL_LEITURAS:
                print("✅ Processo concluído!")
                
                # Enviar JSON via SCP
                arquivo_path = os.path.abspath(data_handler.arquivo)
                print(f"\n📤 Enviando {data_handler.arquivo} via SCP...")
                try:
                    resultado = subprocess.run(
                        ["scp", arquivo_path, SCP_DESTINO],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if resultado.returncode == 0:
                        print("✅ Arquivo enviado com sucesso!")
                    else:
                        print(f"❌ Erro ao enviar: {resultado.stderr}")
                except Exception as e:
                    print(f"❌ Falha no envio: {e}")
                
                break
            
            # Limpar dados para próxima leitura
            data_handler.limpar_dados()
            
            # Aguardar próxima leitura
            time.sleep(INTERVALO_LEITURA)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Coleta interrompida pelo usuário")
    
    finally:
        data_handler.tracker.stop()
        # Finalizar sensores
        print("\nFinalizando sensores...")
        for nome, sensor in sensores_ativos:
            sensor.finalizar()
        print("✓ Sistema encerrado\n")

if __name__ == "__main__":
    # Configurar crontab para execução automática
    print("=== CONFIGURANDO EXECUÇÃO AUTOMÁTICA ===\n")
    try:
        from utils.setup_crontab import configurar_crontab
        configurar_crontab()
        print("\n" + "="*60)
        print("✅ Sistema configurado!")
        print("O main.py será executado automaticamente a cada 1 minuto.")
        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Erro ao configurar crontab: {e}")
        print("Executando coleta única...\n")
        main()
