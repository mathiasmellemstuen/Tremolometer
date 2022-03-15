import serial

connection = serial.Serial(port="/dev/cu.usbmodem21301")

print("Trying to read data")

bytes = connection.read(10 * 10)

for byte in bytes:
    print(bin(byte))

for i in range(0, 4):
    time = int.from_bytes(bytes[12 * i : 12 * i + 4], byteorder="little", signed=False)
    x = int.from_bytes(bytes[12 * i + 4 : 12 * i + 6], byteorder="little", signed=True)
    y = int.from_bytes(bytes[12 * i + 6 : 12 * i + 8], byteorder="little", signed=True)
    z = int.from_bytes(bytes[12 * i + 8 : 12 * i + 10], byteorder="little", signed=True)
    print(f'Data Time {time} x {x} y {y} z {z}')

print(bytes[29])