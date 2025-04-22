import serial
import time
from setvel import SetVel
from heartbeat import Heartbeat

# --- Seri port ayarı ---
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# --- Heartbeat objesi oluştur ---
hb = Heartbeat()
ser.write(bytearray(hb.get_packet()))
print("[→] Heartbeat gönderildi")

# --- Cevap bekleyelim (ilk cevap 1-2 byte olabilir) ---
time.sleep(0.5)
if ser.in_waiting:
    response = ser.read(ser.in_waiting)
    print("[←] Robot yanıt verdi:", [hex(b) for b in response])
else:
    print("[!] Robot yanıt vermedi (şimdilik)")

# --- Robotu ileri gönderelim ---
vel_cmd = SetVel(150)
ser.write(bytearray(vel_cmd.get_packet()))
print("[→] setVel(150) gönderildi")

# --- 2 saniye boyunca heartbeat + cevap dinleme ---
for i in range(2):
    ser.write(bytearray(hb.get_packet()))
    print("[→] Heartbeat gönderildi")

    time.sleep(0.5)

    if ser.in_waiting:
        response = ser.read(ser.in_waiting)
        print("[←] Robot yanıt verdi:", [hex(b) for b in response])
    else:
        print("[…] Henüz yanıt yok")

    time.sleep(0.5)

# --- Robotu durdur ---
stop_cmd = SetVel(0)
ser.write(bytearray(stop_cmd.get_packet()))
print("[→] setVel(0) (dur) gönderildi")

# --- Kapanış heartbeat + cevap ---
ser.write(bytearray(hb.get_packet()))
time.sleep(0.5)
if ser.in_waiting:
    response = ser.read(ser.in_waiting)
    print("[←] Robot son yanıtı:", [hex(b) for b in response])
else:
    print("[!] Son paket yanıtı alınamadı")
