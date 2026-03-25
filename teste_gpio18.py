#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

LUZ_PIN = 18

print("=== TESTE DO PINO GPIO 18 ===\n")

# Teste 1: Configurar como OUTPUT e alternar
print("1. Testando GPIO 18 como SAÍDA (OUTPUT):")
print("   Conecte um LED ou multímetro no pino físico 12\n")

GPIO.setmode(GPIO.BCM)
GPIO.setup(LUZ_PIN, GPIO.OUT)

for i in range(5):
    GPIO.output(LUZ_PIN, GPIO.HIGH)
    print(f"   {i+1}. Pino em HIGH (3.3V)")
    time.sleep(1)
    GPIO.output(LUZ_PIN, GPIO.LOW)
    print(f"   {i+1}. Pino em LOW (0V)")
    time.sleep(1)

GPIO.cleanup()

# Teste 2: Ler o pino flutuante
print("\n2. Testando GPIO 18 como ENTRADA (INPUT) - Pino flutuante:")
print("   Desconecte o sensor\n")

GPIO.setmode(GPIO.BCM)
GPIO.setup(LUZ_PIN, GPIO.IN)

for i in range(10):
    valor = GPIO.input(LUZ_PIN)
    print(f"   Leitura {i+1}: {valor}")
    time.sleep(0.3)

GPIO.cleanup()

# Teste 3: Forçar com pull-up
print("\n3. Testando com PULL-UP interno (deve ler 1):")
GPIO.setmode(GPIO.BCM)
GPIO.setup(LUZ_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for i in range(5):
    valor = GPIO.input(LUZ_PIN)
    print(f"   Leitura {i+1}: {valor} (esperado: 1)")
    time.sleep(0.3)

GPIO.cleanup()

# Teste 4: Forçar com pull-down
print("\n4. Testando com PULL-DOWN interno (deve ler 0):")
GPIO.setmode(GPIO.BCM)
GPIO.setup(LUZ_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for i in range(5):
    valor = GPIO.input(LUZ_PIN)
    print(f"   Leitura {i+1}: {valor} (esperado: 0)")
    time.sleep(0.3)

GPIO.cleanup()

# Teste 5: Teste manual
print("\n5. TESTE MANUAL:")
print("   Conecte o pino GPIO 18 (físico 12) ao:")
print("   - 3.3V (pino físico 1) -> deve ler 1")
print("   - GND (pino físico 6) -> deve ler 0")
print("\n   Pressione Enter para começar...")
input()

GPIO.setmode(GPIO.BCM)
GPIO.setup(LUZ_PIN, GPIO.IN)

print("\n   Lendo continuamente (Ctrl+C para sair):")
try:
    while True:
        valor = GPIO.input(LUZ_PIN)
        print(f"   Valor: {valor}", end='\r')
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nTeste finalizado")
    GPIO.cleanup()

print("\n=== DIAGNÓSTICO ===")
print("Se todos os testes retornaram 0:")
print("  ❌ Pino GPIO 18 pode estar danificado")
print("  ❌ Problema no Raspberry Pi")
print("\nSe pull-up mostrou 1 e pull-down mostrou 0:")
print("  ✅ Pino GPIO 18 está funcionando")
print("  ❌ Problema no sensor ou conexão")
