import serial
import time
from setvel import SetVel
from heartbeat import Heartbeat

baud_rates = [9600, 19200, 38400, 57600, 115200]  # Sırayla denenecek baudlar
port = "/dev/ttyUSB0"  # Portunu kendine göre değiştir

for baud in baud_rates:
    print(f"\n=== Baudrate: {baud} ===")

    try:
        ser = serial.Serial(port, baudrate=baud, timeout=2)
        time.sleep(1)

        # Heartbeat gönder
        hb = Heartbeat()
        ser.write(bytearray(hb.get_packet()))
        print("[→] Heartbeat gönderildi")

        # Cevap var mı kontrol et
        time.sleep(0.5)
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print("[←] Robot cevap verdi:", [hex(b) for b in response])
        else:
            print("[…] Robot cevap vermedi")

        # İleri komut gönder
        vel = SetVel(150)
        ser.write(bytearray(vel.get_packet()))
        print("[→] setVel(150) gönderildi")

        time.sleep(1)

        # Durdur
        stop = SetVel(0)
        ser.write(bytearray(stop.get_packet()))
        print("[→] setVel(0) (dur) gönderildi")

        # Son cevap kontrolü
        time.sleep(0.5)
        if ser.in_waiting:
            response = ser.read(ser.in_waiting)
            print("[←] Son yanıt:", [hex(b) for b in response])
        else:
            print("[…] Son yanıt yok")

        # Eğer burada cevap aldıysan, döngüyü kır
        if ser.in_waiting > 0:
            print(f"✅ Doğru baudrate bulundu: {baud}")
            break

        ser.close()

    except Exception as e:
        print(f"[X] {baud} baudrate ile bağlantı hatası: {e}")
