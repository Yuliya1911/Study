"""7. Создать вручную и заполнить несколькими строками текстовый файл, в котором каждая строка должна
содержать данные о фирме: название, форма собственности, выручка, издержки.
Пример строки файла: firm_1 ООО 10000 5000.

Необходимо построчно прочитать файл, вычислить прибыль каждой компании, а также среднюю прибыль.
Если фирма получила убытки, в расчет средней прибыли ее не включать.
Далее реализовать список. Он должен содержать словарь с фирмами и их прибылями, а также словарь со средней прибылью.
Если фирма получила убытки, также добавить ее в словарь (со значением убытков).
Пример списка: [{“firm_1”: 5000, “firm_2”: 3000, “firm_3”: 1000}, {“average_profit”: 2000}].

Итоговый список сохранить в виде json-объекта в соответствующий файл.


Пример json-объекта:

[{"firm_1": 5000, "firm_2": 3000, "firm_3": 1000}, {"average_profit": 2000}]

Подсказка: использовать менеджер контекста."""
import json

# считали исходный файл
l_file = open('Text_7.txt', 'r', encoding='utf-8')
l_text = l_file.readlines()
l_file.close()

dict_profit = {}
dict_avg = {"average_profit": 0}
dict_loss = {}

for elem in l_text:
    name, tp, proceeds, costs = elem.split(" ")
    profit = int(proceeds) - int(costs)
    if profit >= 0:
        # формируем словарь с фирмами с прибылью, считаем общую прибыль
        dict_profit[name] = profit
        dict_avg["average_profit"] = dict_avg["average_profit"] + profit
    else:
        # формируем словарь с фирмами с убытками (вынесла в отдельный словарь,
        # т.к. из условия не поняла куда их записывать)
        dict_loss[name] = profit

# рассчитываем среднюю прибыль
dict_avg["average_profit"] = round(dict_avg["average_profit"] / len(dict_profit))

# формируем список из словарей согласно условию задачи
list_comp = [dict_profit, dict_loss, dict_avg]
print(f"Список для сохранения в json: {list_comp}")

# сохранение списка в виде json-объекта
with open('Text_7.json', 'w', encoding='utf-8') as js_comp_w:
    json.dump(list_comp, js_comp_w, ensure_ascii=False)

# чтение json-объекта для проверки
with open('Text_7.json', 'r', encoding='utf-8') as js_comp_r:
    print(f"Список, прочитанный из json:{json.load(js_comp_r)}")
