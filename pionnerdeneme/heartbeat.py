class Heartbeat:
    def __init__(self):
        self.command_id = 0x0B           # HEARTBEAT
        self.header = [0xFA, 0xFB]
        self.packet = []

    def calculate_checksum(self, data_bytes):
        checksum = sum(data_bytes) & 0xFFFF
        return [(checksum >> 8) & 0xFF, checksum & 0xFF]

    def build_packet(self):
        # No data, sadece komut byte'ı var
        length = [0x01]                  # command (1)
        body = [self.command_id]
        checksum = self.calculate_checksum(body)
        self.packet = self.header + length + body + checksum
        return self.packet

    def get_packet(self):
        if not self.packet:
            return self.build_packet()
        return self.packet
