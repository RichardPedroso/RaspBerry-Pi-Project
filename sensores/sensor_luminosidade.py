import RPi.GPIO as GPIO

LUZ_PIN = 18
inicializado = False

def inicializar():
    global inicializado
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(LUZ_PIN, GPIO.IN)
        inicializado = True
        return True
    except Exception as e:
        print(f"Erro ao inicializar sensor de luminosidade: {e}")
        return False

def ler_dados():
    if not inicializado:
        return None
    
    try:
        luz = GPIO.input(LUZ_PIN)
        return {"luminosidade_digital": luz}
    except Exception as e:
        print(f"Erro ao ler sensor de luminosidade: {e}")
        return None

def finalizar():
    if inicializado:
        try:
            GPIO.cleanup()
        except:
            pass
