# PCF8574(A)
Модуль MicroPython для работы с 8-битным расширителем ввода/вывода PCF8574(A) I2C от NXP.

Просто подключите плату PCF8574(A) к Arduino, ESP или любой другой плате с прошивкой MicroPython.

Напряжение питания PCF8574(A) 3,3-5,0 Вольт!
1. VCC
2. GND
3. SDA
4. SCL
5. ~INT (подключение необязательно)

Загрузите прошивку MicroPython в плату Pico, Nano (ESP и т. д.), затем скопируйте два файла: main.py, pcf8574mod.py и всю папку sensor_pack.
Затем откройте файл main.py в вашей среде IDE и запустите его.

# Картинки

## Среда разработки
![alt text](https://github.com/octaprog7/pcf8574/blob/master/ide8574.png)
## Макетная плата
![alt text](https://github.com/octaprog7/pcf8574/blob/master/bb8574.jpg)
## Схема подключения
![alt text](https://github.com/octaprog7/pcf8574/blob/master/conn8574.png)
## Обработка прерывания
![alt text](https://github.com/octaprog7/pcf8574/blob/master/pcf8574_irq.png)
## Подключение для обработки прерываний от PCF8574
![alt text](https://github.com/octaprog7/pcf8574/blob/master/conn_irq.png)
## Видео
Cсылка: https://youtu.be/61_FNGSfh-4
