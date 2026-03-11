#!/usr/bin/env python3
from crontab import CronTab
import os
import sys

def configurar_crontab():
    # Obter usuário atual
    cron = CronTab(user=True)
    
    # Remover jobs anteriores do projeto (evitar duplicatas)
    cron.remove_all(comment='RaspBerry-Pi-Project')
    
    # Caminho absoluto do projeto e do Python
    projeto_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main_path = os.path.join(projeto_path, 'main.py')
    python_path = sys.executable
    
    # Criar novo job
    job = cron.new(command=f'cd {projeto_path} && {python_path} {main_path}', comment='RaspBerry-Pi-Project')
    
    # Executar a cada 1 minuto
    job.minute.every(1)
    
    # Salvar no crontab
    cron.write()
    
    print("✅ Crontab configurado com sucesso!")
    print(f"📁 Projeto: {projeto_path}")
    print(f"🐍 Python: {python_path}")
    print(f"⏰ Frequência: A cada 1 minuto")
    print(f"\n📋 Job criado: {job}")
    print("\n💡 Para verificar: crontab -l")
    print("💡 Para remover: crontab -r")

def remover_crontab():
    cron = CronTab(user=True)
    removidos = cron.remove_all(comment='RaspBerry-Pi-Project')
    cron.write()
    print(f"✅ {removidos} job(s) removido(s) do crontab")

if __name__ == "__main__":
    print("=== CONFIGURADOR DE CRONTAB ===\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == "remover":
        remover_crontab()
    else:
        configurar_crontab()
