class SetVel2:
    def __init__(self, left_vel, right_vel):
        self.command_id = 0x08            # VEL2 komutu
        self.header = [0xFA, 0xFB]
        self.left_vel = left_vel
        self.right_vel = right_vel
        self.packet = []

    def int16_to_little_endian(self, value):
        """16-bit signed integer (int16) little endian"""
        return [
            value & 0xFF,
            (value >> 8) & 0xFF
        ]

    def calculate_checksum(self, data_bytes):
        checksum = sum(data_bytes) & 0xFFFF
        return [(checksum >> 8) & 0xFF, checksum & 0xFF]

    def build_packet(self):
        left_bytes = self.int16_to_little_endian(self.left_vel)
        right_bytes = self.int16_to_little_endian(self.right_vel)
        data = left_bytes + right_bytes

        length = [0x05]  # 1 (command) + 4 (data)
        body = [self.command_id] + data
        checksum = self.calculate_checksum(body)

        self.packet = self.header + length + body + checksum
        return self.packet

    def get_packet(self):
        if not self.packet:
            return self.build_packet()
        return self.packet
