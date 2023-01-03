# micropython
# mail: goctaprog@gmail.com
# MIT license


# Please read this before use!: https://www.nxp.com/part/PCF8574T
from machine import I2C, Pin
import pcf8574mod
import time
from sensor_pack.bus_service import I2cAdapter

if __name__ == '__main__':
    # пожалуйста установите выводы scl и sda в конструкторе для вашей платы, иначе ничего не заработает!
    # please set scl and sda pins for your board, otherwise nothing will work!
    # https://docs.micropython.org/en/latest/library/machine.I2C.html#machine-i2c
    # i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=400_000) № для примера
    # bus =  I2C(scl=Pin(4), sda=Pin(5), freq=100000)   # на esp8266    !
    # Внимание!!!
    # Замените id=1 на id=0, если пользуетесь первым портом I2C !!!
    # Warning!!!
    # Replace id=1 with id=0 if you are using the first I2C port !!!
    i2c = I2C(id=1, scl=Pin(27), sda=Pin(26), freq=400_000)  # on Arduino Nano RP2040 Connect tested
    adapter = I2cAdapter(i2c)
    io_expander = pcf8574mod.PCF8574(adapter=adapter, address=0x20)

    values = 0xF0, 0xF1, 0xF3, 0xF7, 0xFF
    index = 0
    while True:
        io_expander.write(values[index])
        time.sleep_ms(250)
        index += 1
        if index == len(values):
            index = 0
        print(index, hex(values[index]))

    # for value in io_expander:
    #    print(f"Read value: 0x{value:x}\t0b{value:8b}")
    #    time.sleep_ms(50)
