import RPi.GPIO as GPIO
import time

# Lista dos GPIO mais usados (modo BCM)
gpio_list = [2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26, 14, 15, 18, 23, 24, 25]

GPIO.setmode(GPIO.BCM)

for pin in gpio_list:
    GPIO.setup(pin, GPIO.IN)

print("=== Detector de GPIO ===")
print("Coloque a mão no sensor e observe qual GPIO muda.\n")

try:
    while True:
        for pin in gpio_list:
            estado = GPIO.input(pin)
            print(f"GPIO {pin}: {estado}", end=" | ")
        print("\n------------------------------")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()