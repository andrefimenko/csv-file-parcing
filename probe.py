import pandas
import re

table = pandas.read_csv('test_data.csv')

names = open("Names.txt")
x = names.read().lower()
names_lst = list(x.split(', '))

new_col_insight = 'insight'
table[new_col_insight] = ''

table.to_csv('new.csv', index=False)
count = len(table)
dlg_count = table.iloc[count - 1]['dlg_id'] + 1

dlg_id_list = list(range(dlg_count))
greetings = []
farewells = []
managers = set()
companies = set()


def pars_a(row, dlg_id):
    if row < count and table.iloc[row]['dlg_id'] == dlg_id and table.iloc[row]['role'] == 'manager'\
            and re.search(r"([Дд]обр.*)|([Зз]дра.*)", table.iloc[row]['text']):
        table._set_value(row, 'insight', 'greeting')
        print(f'a. Реплика с приветствием – где менеджер поздоровался: "{table.iloc[row]["text"]}",'
              f' id диалога: {table.iloc[row]["dlg_id"]}, строка в таблице: {row + 2}')
        greetings.append(table.iloc[row]['dlg_id'])
        pars_a(row + 1, dlg_id + 1)
    elif row < count:
        pars_a(row + 1, dlg_id)
    else:
        return


def pars_b(row, dlg_id):
    if row < count and table.iloc[row]['dlg_id'] == dlg_id and table.iloc[row]['role'] == 'manager'\
            and re.search(r"(([Мм]ен.+ [Зз]ов.+)|([Зз]ову.+ [Мм]ен.*))", table.iloc[row]['text']):
        table._set_value(row, 'insight', 'introducing')
        print(f'b. Реплика, где менеджер представил себя: "{table.iloc[row]["text"]}",'
              f' id диалога: {table.iloc[row]["dlg_id"]}, строка в таблице: {row + 2}')
        lst = list(table.iloc[row]["text"].split(' '))
        for i in lst:
            if i in names_lst:
                print(f'Имя менеджера: {i.capitalize()}')
                managers.add(i.capitalize())
                table._set_value(row + 1, 'insight', i.capitalize())
        pars_b(row + 1, dlg_id + 1)
    elif row < count:
        pars_b(row + 1, dlg_id)
    else:
        return
    return


def pars_c(list):
    print("c. Представившиеся менеджеры: ")
    for i in list:
        print(i)
    return


def pars_d(row, dlg_id):
    if row < count and table.iloc[row]['dlg_id'] == dlg_id and table.iloc[row]['role'] == 'manager'\
            and re.search(r"[Кк]омпани.*", table.iloc[row]['text']):
        # table._set_value(row, 'insight', 'company')
        print(f'd. Реплика с названием компании: "{table.iloc[row]["text"]}",'
              f' id диалога: {table.iloc[row]["dlg_id"]}, строка в таблице: {row + 2}')
        lst = list(table.iloc[row]["text"].split(' '))
        # print(lst)
        for i in lst:
            if i in names_lst:
                print(f"{(str(lst[(lst.index(i)) + 2]) + ' ' + lst[(lst.index(i)) + 3]).capitalize()}")
                companies.add((str(lst[(lst.index(i)) + 2] + ' ' + lst[(lst.index(i)) + 3]).capitalize()))
        pars_d(row + 1, dlg_id + 1)
    elif row < count:
        pars_d(row + 1, dlg_id)
    else:
        print()
        print(f"Упоминаемые компании:")
        for i in companies:
            print(i)
        return


def pars_e(row, dlg_id):
    if row < count and table.iloc[row]['dlg_id'] >= dlg_id and table.iloc[row]['role'] == 'manager'\
            and re.search(r"(([Дд]о свид.*)|([Пп]роща.*)|([Дд]о (скорой)? ?встречи)|(всего доброго))",
                          table.iloc[row]['text']):
        table._set_value(row, 'insight', 'farewell');
        print(f'e. Реплика, где менеджер попрощался: "{table.iloc[row]["text"]}",'
              f' id диалога: {table.iloc[row]["dlg_id"]}, строка в таблице: {row + 2}')
        farewells.append(table.iloc[row]['dlg_id'])
        pars_e(row + 1, dlg_id + 1)
    elif row < count:
        pars_e(row + 1, dlg_id)
    else:
        return
    return


def pars_f():
    for i in dlg_id_list:
        if i in greetings and i in farewells:
            print(f'f. Требование к менеджеру: «В каждом диалоге обязательно необходимо'
                  f' поздороваться и попрощаться с клиентом» - id диалога {i} - Выполнено')
        else:
            print(f'f. Требование к менеджеру: «В каждом диалоге обязательно необходимо'
                  f' поздороваться и попрощаться с клиентом» - id диалога {i} - Нарушено')
    return


pars_a(0, 0)
print()
pars_b(0, 0)
print()
pars_c(managers)
print()
pars_d(0, 0)
print()
pars_e(0, 0)
print()
pars_f()
print()
print("СОЗДАН НОВЫЙ CSV-ФАЙЛ С СООТВЕТСТВУЮЩИМИ ОТМЕТКАМИ")

table.to_csv('new.csv', index=False)
