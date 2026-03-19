import board
import adafruit_dht

DHT_PIN = board.D22
dht = None

def inicializar():
    global dht
    try:
        dht = adafruit_dht.DHT11(DHT_PIN)
        return True
    except Exception as e:
        print(f"Erro ao inicializar sensor umidade/temperatura: {e}")
        return False

def ler_dados():
    if dht is None:
        return None
    
    try:
        umidade = dht.humidity
        temperatura = dht.temperature
        
        if umidade is not None and temperatura is not None:
            return {
                "umidade_ar": umidade,
                "temperatura": temperatura
            }
    except RuntimeError:
        pass
    except Exception as e:
        print(f"Erro ao ler sensor umidade/temperatura: {e}")
    
    return None

def finalizar():
    global dht
    if dht:
        try:
            dht.exit()
        except:
            pass
