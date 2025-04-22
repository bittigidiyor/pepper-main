import serial
import time
from setvel2 import SetVel2
from heartbeat import Heartbeat

# --- Ubuntu için seri port ayarı ---
# Gerekirse 'ls /dev/tty*' ile doğru portu bul
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# --- Heartbeat başlat ---
hb = Heartbeat()
ser.write(bytearray(hb.get_packet()))
print("Başlangıç heartbeat gönderildi")

# --- İleri yönde hareket verelim (her iki motor) ---
vel2 = SetVel2(150, 150)  # Sol ve sağ motor: 150 mm/s
ser.write(bytearray(vel2.get_packet()))
print("Robot ileri gidiyor")

# --- 2 saniye hareket ve heartbeat ---
for _ in range(2):
    ser.write(bytearray(hb.get_packet()))
    time.sleep(1)

# --- Robotu durdur ---
stop = SetVel2(0, 0)
ser.write(bytearray(stop.get_packet()))
print("Robot durduruldu")

# --- Heartbeat döngüsü ---
while True:
    ser.write(bytearray(hb.get_packet()))
    print("Heartbeat gönderildi")
    time.sleep(1)
