import bluetooth

bd_addr = "5C:01:3B:96:8C:22"  # MAC-адрес устройства ESP32
port = 1  # обычно для ESP32 и HC-05 используется порт 1

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    print("Подключение к устройству...")
    sock.connect((bd_addr, port))
    print("Успешно подключено!")

    while True:
        message = input("Введите команду (например, 150l): ")
        if message == "exit":
            break
        sock.send(message)
        print("Отправлено:", message)

except bluetooth.btcommon.BluetoothError as err:
    print("Ошибка подключения:", err)

finally:
    sock.close()
    print("Соединение закрыто.")
