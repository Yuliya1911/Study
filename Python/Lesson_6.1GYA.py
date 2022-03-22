"""1. Создать класс TrafficLight (светофор) и определить у него один атрибут color (цвет) и метод running (запуск).
Атрибут реализовать как приватный. В рамках метода реализовать переключение светофора в режимы:
красный, желтый, зеленый. Продолжительность первого состояния (красный) составляет 7 секунд,
второго (желтый) — 2 секунды, третьего (зеленый) — на ваше усмотрение.
Переключение между режимами должно осуществляться только в указанном порядке (красный, желтый, зеленый).
Проверить работу примера, создав экземпляр и вызвав описанный метод.
Задачу можно усложнить, реализовав проверку порядка режимов, и при его нарушении выводить соответствующее сообщение
и завершать скрипт."""
import itertools
from time import sleep


class TrafficLight:
    __color: list
    __iter: itertools.cycle

    def __init__(self):
        self.__color = ["Красный", "Желтый", "Зеленый"]

        self.__iter = itertools.cycle(self.__color)

    def next_color(self):
        return next(self.__iter)

    def running(self):
        while True:
            stop = ""
            cur_color = self.next_color()
            print(cur_color)
            if cur_color == "Красный":
                print("Пауза 7 секунд")
                sleep(7)
            elif cur_color == "Желтый":
                print("Пауза 2 секунды")
                sleep(2)
            else:
                sleep(1)
                stop = input("Введите \"Stop\" для выхода или \"Enter\" для продолжения")

            if stop.capitalize() == "Stop":
                break


a = TrafficLight()
a.running()
