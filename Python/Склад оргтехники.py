"""4. Начните работу над проектом «Склад оргтехники». Создайте класс, описывающий склад.
А также класс «Оргтехника», который будет базовым для классов-наследников.
Эти классы — конкретные типы оргтехники (принтер, сканер, ксерокс).
В базовом классе определить параметры, общие для приведенных типов.
В классах-наследниках реализовать параметры, уникальные для каждого типа оргтехники.

5. Продолжить работу над первым заданием. Разработать методы, отвечающие за приём оргтехники на склад и
передачу в определенное подразделение компании. Для хранения данных о наименовании и количестве единиц оргтехники,
а также других данных, можно использовать любую подходящую структуру, например словарь.

6. Продолжить работу над вторым заданием. Реализуйте механизм валидации вводимых пользователем данных.
Например, для указания количества принтеров, отправленных на склад, нельзя использовать строковый тип данных.
Подсказка: постарайтесь по возможности реализовать в проекте «Склад оргтехники» максимум возможностей,
изученных на уроках по ООП."""

from abc import ABC, abstractmethod
from random import randint


###############################################################################
class Storage:
    _name_storage: str
    __max_count: int
    __dict_equipments: dict

    def __init__(self, i_nameStorage="Склад оргтехники", i_count=10):
        self._name_storage = i_nameStorage
        self.__max_count = i_count
        self.__dict_equipments = {}

    @property
    def nameStorage(self):
        return self._name_storage

    # добавляем товар на склад
    def add(self, i_officeEquipment, i_cntEquipment=1):
        # проверка количества добавляемых товаров и наличия свободных мест на складе
        if type(i_cntEquipment) != int:
            raise exCnt(i_cntEquipment, i_officeEquipment)
        elif i_cntEquipment < 1:
            raise exCnt(i_cntEquipment, i_officeEquipment)
        elif self.balance(False) + i_cntEquipment > self.__max_count:
            raise exNoPlace(self, i_officeEquipment, i_cntEquipment - (self.__max_count - self.balance(False)))
        # добавление товара на склад
        name_class = type(i_officeEquipment).__name__
        if name_class in self.__dict_equipments:
            self.__dict_equipments[name_class].extend([i_officeEquipment]*i_cntEquipment)
        else:
            self.__dict_equipments[name_class] = [i_officeEquipment]*i_cntEquipment

    # получаем товар со склада (на вход тип товара, который нужно отдать со склада)
    def get(self, i_typeEquipment: str):
        if i_typeEquipment in self.__dict_equipments:
            if len(self.__dict_equipments[i_typeEquipment]) < 1:
                raise StorageException(f"Товар {i_typeEquipment} закончился в/на {self._name_storage}!")
            return self.__dict_equipments[i_typeEquipment].pop()
        else:
            raise StorageException(f"товар {i_typeEquipment} отсутствует в/на {self._name_storage}!")

    # выводим наименование и все позиции
    def balance(self, i_print=True):
        cnt = 0
        if not self.__dict_equipments and i_print:
            print(f"{self._name_storage} не содержит товаров")
            return 0
        # if i_print:
        #     print("-"*15)
        for key, value in self.__dict_equipments.items():
            cnt += len(value)
            if i_print:
                for elem in value:
                    print(f"Получатель оргтехники: {self._name_storage}. "
                          f"Категория товара: {key}, "
                          f"наименование товара {elem}")
        # if i_print:
        #     print("-"*15)
        return cnt
###############################################################################


###############################################################################
class exNoPlace(Exception):
    def __init__(self, i_storage, i_officeEquipment, i_needCnt):
        self.__storage = i_storage
        self.__officeEquipment = i_officeEquipment
        self.__needCnt = i_needCnt

    def __str__(self):
        return f"Нет места для размещения {self.__officeEquipment} в/на '{self.__storage.nameStorage}'. " \
               f"Не хватает мест - {self.__needCnt} "
###############################################################################


###############################################################################
class exCnt(Exception):
    def __init__(self, i_cntEquipment, i_officeEquipment):
        self.__cntEquipment = i_cntEquipment
        self.__officeEquipment = i_officeEquipment

    def __str__(self):
        return f"Невозможно разместить {self.__officeEquipment}  в количестве '{self.__cntEquipment}', " \
               f"{type(self.__cntEquipment).__name__}"
###############################################################################


###############################################################################
class StorageException(Exception):
    def __init__(self, i_txt):
        self.__txt = i_txt

    def __str__(self):
        return f"Ошибка хранения: {self.__txt}"
###############################################################################


###############################################################################
class OfficeEquipment(ABC):
    _model: str
    speed: int

    def __init__(self, i_model, i_speed):
        self._model = i_model
        self.speed = i_speed

    @abstractmethod
    def info(self):
        pass

    @property
    def model(self):
        return self._model

    def __str__(self):
        return self._model

    def __repr__(self):
        return self._model
###############################################################################


###############################################################################
# Класс Принтер. Атрибуты: модель, скорость, технология печати
class Printer(OfficeEquipment):
    # _model: str
    # speed: int
    printing_technology: str

    def __init__(self, i_model, i_speed, i_printing_technology):
        super().__init__(i_model, i_speed)
        self.printing_technology = i_printing_technology

    def info(self):
        return f"Принтер: модель {self._model}, технология печати: {self.printing_technology}, " \
               f"скорость печати: {self.speed} страниц в минуту"
###############################################################################


###############################################################################
# Класс Сканер. Атрибуты: модель, скорость, тип сканера, разрешение
class Scanner(OfficeEquipment):
    # _model: str
    # speed: int
    scanner_type: str
    permission: dict

    def __init__(self, i_model, i_speed, i_scanner_type, i_x, i_y):
        super().__init__(i_model, i_speed)
        self.scanner_type = i_scanner_type
        self.permission = {"x": i_x, "y": i_y}

    def info(self):
        return f"Сканер: модель {self._model}, тип: {self.scanner_type}, " \
               f"разрешение: {self.permission['x']}*{self.permission['y']} dpi, " \
               f"скорость сканирования: {self.speed} сек/стр."
###############################################################################


###############################################################################
# Класс Ксерокс. Атрибуты: модель, скорость, масштабирование, разрешение
class Xerox(OfficeEquipment):
    # _model: str
    # speed: int
    scaling: str
    permission: dict

    def __init__(self, i_model, i_speed, i_scaling, i_x, i_y):
        super().__init__(i_model, i_speed)
        self.scaling = i_scaling
        self.permission = {"x": i_x, "y": i_y}

    def info(self):
        return f"Ксерокс: модель {self._model}, масштабирование: {self.scaling}, " \
               f"разрешение: {self.permission['x']}*{self.permission['y']} dpi, скорость: {self.speed} страниц в минуту"
###############################################################################




# Создание склада и отделов, которые будут получать оборудование"
g_dict = {
    "Склад": Storage(),
    "Цех": Storage("Цех", 5),
    "Отдел КК": Storage("ОКК", 1)
}

print("----------Проверка баланса----------")
g_dict["Склад"].balance()
g_dict["Цех"].balance()
g_dict["Отдел КК"].balance()

print("\n----------Создание оргтехники для размещения на Складе----------")
g_listEquipments = [
    Printer("Canon-1", 50, "струйная печать"),
    Printer("Canon-2", 40, "светодиодная печать"),
    Printer("Canon-3", 30, "лазерная печать"),
    Scanner("Panasonic KV-1", 3, "планшетный", 600, 600),
    Scanner("Panasonic KV-2", 5, "планшетный", 500, 700),
    Scanner("Panasonic KV-3", 10, "планшетный", 800, 1200),
    Xerox("Xerox 1/DN", 20, "A3", 600, 600),
    Xerox("Xerox 2/DN", 20, "A4", 800, 1200),
    Xerox("Xerox 3/DN", 20, "A5", 500, 700)
]
print(g_listEquipments)

print("\n----------Размещение огртехники на Складе (каждой позиции рандомное количество от -3 до 3)----------")
for equipment in g_listEquipments:
    try:
        cnt = randint(-3, 3)
        g_dict["Склад"].add(equipment, cnt)
        print(f"Товар {equipment} добавлен на склад в количестве {cnt}")
    except Exception as Err:
        print(f"{Err}")
print(f"Итого: на складе размещено {g_dict['Склад'].balance(False)} наименований оборудования")

print("\n----------Проверка ввода товара с нечисловым количеством----------")
try:
    g_dict["Склад"].add(g_listEquipments[0], "два")
    print(f"Товар {g_listEquipments[0]} добавлен на склад")
except Exception as Err:
    print(f"{Err}")

print("\n----------Получение и размещение техники, по умолчанию 1 единица----------")
try:
    g_dict["Цех"].add(g_dict["Склад"].get("Printer"), 1)
    g_dict["Цех"].balance()
except Exception as Err:
    print(f"{Err}")

print("\n----------Перемещаем технику со склада в ОКК до тех пор, пока в ОКК не закончится место----------")
try:
    while True:
        g_dict["Отдел КК"].add(g_dict["Склад"].get("Printer"), 1)
        g_dict["Отдел КК"].balance()
except Exception as Err:
    print(f"{Err}")

print("\n----------Получение и размещение несуществуеющей техники в Цех----------")
try:
    g_dict["Цех"].add(g_dict["Склад"].get("МФУ"), 1)
except Exception as Err:
    print(f"{Err}")

print("\n----------Опустошение Склада оргтехники, до получения сообщения об отсутствии товара----------")
try:
    while True:
        scan = g_dict["Склад"].get("Scanner")
        print(scan.info())
except Exception as Err:
    print(f"{Err}")
