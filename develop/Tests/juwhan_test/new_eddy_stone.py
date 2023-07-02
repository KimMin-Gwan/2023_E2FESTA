import bluetooth
import struct

def parse_eddystone(data):
    """
    Eddystone 데이터를 파싱하는 함수
    """
    frame_type = data[0]
    if frame_type == 0x00:  # Eddystone-UID 프레임
        namespace = ''.join('{:02x}'.format(byte) for byte in data[2:12])
        instance = ''.join('{:02x}'.format(byte) for byte in data[12:18])
        return f"Eddystone-UID: Namespace={namespace}, Instance={instance}"
    elif frame_type == 0x10:  # Eddystone-URL 프레임
        url_prefix = {
            0x00: "http://www.",
            0x01: "https://www.",
            0x02: "http://",
            0x03: "https://"
        }.get(data[2], "Unknown")
        url = url_prefix + data[3:].decode("utf-8")
        return f"Eddystone-URL: {url}"
    elif frame_type == 0x20:  # Eddystone-TLM 프레임
        voltage = struct.unpack(">H", data[2:4])[0]
        temperature = struct.unpack(">h", data[4:6])[0] / 256.0
        adv_count = struct.unpack(">I", data[6:10])[0]
        uptime = struct.unpack(">I", data[10:14])[0] / 10.0
        return f"Eddystone-TLM: Voltage={voltage} mV, Temperature={temperature} °C, AdvCount={adv_count}, Uptime={uptime} seconds"
    else:
        return "Unknown Eddystone frame type"

def receive_eddystone_data():
    """
    Eddystone 데이터 수신 함수
    """
    nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)
    for addr, name in nearby_devices:
        print(f"Device: {name} ({addr})")
        try:
            service_matches = bluetooth.find_service(address=addr)
            for service in service_matches:
                if service['name'] == 'Eddystone':
                    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    sock.connect((addr, service['port']))
                    data = sock.recv(1024)
                    print(parse_eddystone(data))
                    sock.close()
        except bluetooth.btcommon.BluetoothError as e:
            print(f"Bluetooth error occurred: {e}")
        print()

# Eddystone 데이터 수신 시작
receive_eddystone_data()
