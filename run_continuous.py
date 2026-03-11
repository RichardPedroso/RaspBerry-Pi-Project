import time
import subprocess
import sys

INTERVALO_ENTRE_EXECUCOES = 60  # 1 minuto

def executar_ciclo():
    print("="*60)
    print("🔄 INICIANDO NOVO CICLO DE COLETA")
    print("="*60 + "\n")
    
    try:
        resultado = subprocess.run(
            [sys.executable, "main.py"],
            cwd="/home/aluno/RaspBerry-Pi-Project",
            capture_output=False
        )
        
        if resultado.returncode == 0:
            print("\n✅ Ciclo concluído com sucesso!")
        else:
            print(f"\n⚠️ Ciclo finalizado com código: {resultado.returncode}")
    
    except Exception as e:
        print(f"\n❌ Erro na execução: {e}")

if __name__ == "__main__":
    print("=== SISTEMA DE COLETA CONTÍNUA ===")
    print(f"Intervalo entre execuções: {INTERVALO_ENTRE_EXECUCOES}s\n")
    
    ciclo = 1
    try:
        while True:
            print(f"\n[CICLO {ciclo}]")
            executar_ciclo()
            
            print(f"\n⏳ Aguardando {INTERVALO_ENTRE_EXECUCOES}s para próximo ciclo...\n")
            time.sleep(INTERVALO_ENTRE_EXECUCOES)
            
            ciclo += 1
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Sistema interrompido pelo usuário")
        print("✓ Encerrado\n")
