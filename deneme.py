import serial
import time

def send_packet(ser, packet):
    ser.write(bytearray(packet))
    time.sleep(0.1)

def calc_checksum(packet_body):
    checksum = sum(packet_body) & 0xFFFF
    return [(checksum >> 8) & 0xFF, checksum & 0xFF]

def main():
    # Open serial connection
    ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, timeout=1)

    # --- SYNC Sequence ---
    sync_packets = [
        [250, 251, 3, 0, 0, 0],
        [250, 251, 3, 1, 0, 1],
        [250, 251, 3, 2, 0, 2]
    ]
    for packet in sync_packets:
        send_packet(ser, packet)

    # --- OPEN Server (command #1 again, for open) ---
    open_cmd = [250, 251, 3, 1, 0, 1]
    send_packet(ser, open_cmd)

    # --- ENABLE Motors (command #4, int argument 1) ---
    enable_cmd = [250, 251, 5, 4, 1, 0, 5]
    send_packet(ser, enable_cmd)

    # --- MOVE Command (command #1) ---
    translational_velocity = 200   # mm/s
    rotational_velocity = 0        # deg/s

    # Convert to bytes
    trans_bytes = translational_velocity.to_bytes(2, byteorder='big', signed=True)
    rot_bytes = rotational_velocity.to_bytes(2, byteorder='big', signed=True)

    cmd_body = [1, 2]  # command #1, 2 args
    cmd_body.extend(trans_bytes)
    cmd_body.extend(rot_bytes)
    checksum = calc_checksum(cmd_body)

    move_packet = [250, 251]
    move_packet.append(len(cmd_body) + 2)  # total length = command bytes + checksum
    move_packet.extend(cmd_body)
    move_packet.extend(checksum)

    send_packet(ser, move_packet)

    # Let robot move for 2 seconds
    time.sleep(2)

    # --- Stop movement (send 0 velocities) ---
    trans_bytes = (0).to_bytes(2, byteorder='big', signed=True)
    rot_bytes = (0).to_bytes(2, byteorder='big', signed=True)
    stop_body = [1, 2] + list(trans_bytes) + list(rot_bytes)
    stop_packet = [250, 251, len(stop_body) + 2] + stop_body + calc_checksum(stop_body)

    send_packet(ser, stop_packet)

    ser.close()

if __name__ == "__main__":
    main()
