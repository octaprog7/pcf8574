# micropython
# mail: goctaprog@gmail.com
# MIT license


# Please read this before use!: https://www.nxp.com/part/PCF8574T
import micropython
from machine import I2C, Pin
import pcf8574mod
import time
from sensor_pack.bus_service import I2cAdapter

# Если в обработчике прерывания возникнет ошибка, MicroPython не сможет создать сообщение о ней!
# Cоздаю специальный буфер для этой цели!
micropython.alloc_emergency_exception_buf(100)
# interrupt counter, один байт
irq_cnt = bytearray(1)


def irq_handler(p: Pin):
    """Пожалуйста прочитай это: http://docs.micropython.org/en/latest/reference/isr_rules.html#isr-rules"""
    global irq_cnt
    irq_cnt[0] += 1


if __name__ == '__main__':
    # пожалуйста установите выводы scl и sda в конструкторе для вашей платы, иначе ничего не заработает!
    # please set scl and sda pins for your board, otherwise nothing will work!
    # https://docs.micropython.org/en/latest/library/machine.I2C.html#machine-i2c
    # i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=400_000) # для примера
    # bus =  I2C(scl=Pin(4), sda=Pin(5), freq=100000)   # на esp8266    !
    # Внимание!!!
    # Замените id=1 на id=0, если пользуетесь первым портом I2C !!!
    # Warning!!!
    # Replace id=1 with id=0 if you are using the first I2C port !!!
    # i2c = I2C(0, scl=Pin(13), sda=Pin(12), freq=400_000) # для примера

    # Вывод GPIO21 настроен как ВХОД без подтягивающего резистора (я установил внешний резистор 4К7 подтягивающий к VCC)
    p_irq = Pin(21, Pin.IN, pull=None)
    # функции irq_handler будет передаваться управление, когда один из выводов P0..P7, настроенных, как ВХОД,
    # изменит состояние! Вы можете подключить к выводу GPIO21 провод и подключать его к GND,
    # чтобы прерывание возникло!
    # Не забудьте подключить вывод INT PCF8574 к выводу GPIO21 платы Arduino Nano RP2040 Connect with RP2040 !!!
    # Внешний подтягивающий вывод INT PCF8574 резистор к VCC необязателен. Вместо него можно использовать внутренний
    # подтягивающий резистор. Вместо pull=None напишите pull=Pin.PULL_UP !
    p_irq.irq(handler=irq_handler, trigger=Pin.IRQ_FALLING)

    i2c = I2C(id=1, scl=Pin(27), sda=Pin(26), freq=400_000)  # on Arduino Nano RP2040 Connect tested
    adapter = I2cAdapter(i2c)
    io_expander = pcf8574mod.PCF8574(adapter=adapter, address=0x20)

    values = 0xF0, 0xF1, 0xF3, 0xF7, 0xFF
    index = 0
    while True:
        io_expander.write(values[index])
        print(f"{hex(io_expander())}\tirq counter: {irq_cnt[0]}")
        time.sleep_ms(250)
        index += 1
        if index == len(values):
            index = 0
        # print(index, hex(values[index]))
        
    # for value in io_expander:
    #    print(f"Read value: 0x{value:x}\t0b{value:8b}")
    #    time.sleep_ms(50)
