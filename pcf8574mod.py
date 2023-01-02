# micropython
# MIT license
# Copyright (c) 2023 Roman Shevchik   goctaprog@gmail.com
from sensor_pack import bus_service
from sensor_pack.base_sensor import Device, Iterator, check_value


# Please read this before use!: https://www.nxp.com/part/PCF8574T
class PCF8574(Device, Iterator):

    def __init__(self, adapter: bus_service.BusAdapter, address: int):
        s0 = f"Invalid address value: 0x{address:x}!"
        if address < 0x38:  # PCF8574
            check_value(address, range(0x20, 0x28), s0)
        else:   # PCF8574A
            check_value(address, range(0x38, 0x40), s0)
        super().__init__(adapter, address, True)
        self.write()

    def _read(self) -> int:
        """считывает значение на линиях P0..P7."""
        b = self.adapter.read(device_addr=self.address, n_bytes=1)
        bo = self._get_byteorder_as_str()[0]
        return int.from_bytes(b, bo)

        # BaseSensor
    def _write(self, value: int) -> int:
        """записывает значения на линии P0..P7."""
        if value < 0 or value > 0xFF:
            raise ValueError(f"The value must contain no more than 8 significant bits!")
        bo = self._get_byteorder_as_str()[0]
        return self.adapter.write(device_addr=self.address, buf=value.to_bytes(1, bo))

    def write(self, value: int = 0xFF):
        """Настройка портов на ввод/вывод. По умолчанию выводы P0..P7 настраиваются как входы!
        Если бит установлен в ноль, то происходит "подтяжка" вывода порта P0..P7 к земле через внутренний транзистор!
        Если бит установлен в единицу, вывод порта P0..P7 будет подтянут к питанию через источник тока в 100 uA!

        Поэтому:
            * если вы подключаете к выводу порта P0..P7 кнопку, то записывайте в соотв. бит ЕДИНИЦУ и потом читайте
              состояние, а кнопку подключайте между выводом порта и ЗЕМЛЕЙ(VSS)!!!
            * если вы подключаете к выводу порта P0..P7 нагрузку, то подавать напряжение на нее нужно записью в
              соответствующий бит НУЛЯ, а нагрузку подключайте между +Питание(VDD) и выводом порта P0..P7!!!"""
        self._write(value)

    def __call__(self):
        """Чтение состояния линий портов P0..P7"""
        return self._read()

    def __iter__(self):
        return self

    def __next__(self) -> int:
        """Можно использовать как итератор (чтение в цикле for)"""
        return self._read()
