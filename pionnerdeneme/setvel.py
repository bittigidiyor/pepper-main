class SetVel:
    def __init__(self, vel):
        self.command_id = 0x03          # ARCOS VEL komutu
        self.header = [0xFA, 0xFB]
        self.velocity = vel             # mm/s cinsinden hız
        self.packet = []

    def int_to_little_endian_bytes(self, value):
        """Velocity'i 4 byte little-endian olarak döndür"""
        return [
            value & 0xFF,
            (value >> 8) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 24) & 0xFF
        ]

    def calculate_checksum(self, data_bytes):
        """Checksum: komut ve veri byte'larının toplamı, 2 byte (big-endian)"""
        checksum = sum(data_bytes) & 0xFFFF
        return [(checksum >> 8) & 0xFF, checksum & 0xFF]

    def build_packet(self):
        # Veriyi hazırla (4 byte velocity)
        data = self.int_to_little_endian_bytes(self.velocity)

        # Paket uzunluğu: 1 (komut) + 4 (veri)
        length = [0x05]

        # Komut + veri
        body = [self.command_id] + data

        # Checksum hesapla
        checksum = self.calculate_checksum(body)

        # Final paket
        self.packet = self.header + length + body + checksum
        return self.packet

    def get_packet(self):
        if not self.packet:
            return self.build_packet()
        return self.packet
