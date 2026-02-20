import board
import adafruit_dht

# GPIO 4
DHT_PIN = board.D4

dht = adafruit_dht.DHT11(DHT_PIN)

def get_cpu_temperature():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return round(float(f.read()) / 1000.0, 2)
    except:
        return None

try:
    umidade = dht.humidity
    cpu_temp = get_cpu_temperature()

    print(f"Umidade do ar: {umidade}% | Temperatura CPU: {cpu_temp}°C")

except Exception as e:
    print("Erro ao ler sensores:", e)

finally:
    dht.exit()