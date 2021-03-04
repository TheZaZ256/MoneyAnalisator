#!/usr/bin/python3

##############################################################3
try:
    import sys, os, pickle, datetime
    import os.path
    import sqlite3
    from sqlite3 import Error
except:
    print('Trouble with import')
################################################################
#БД
#########################
#Create connect
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
######################################33
#Работа с бд
Data_Base_sql = 'Data_Base_SQL_MoneyAnalisator.db'
connection = create_connection(Data_Base_sql)

############################################
#Принимает запрос
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

#######################################
#Запросы на создание таблиц
create_Spends_table = """
CREATE TABLE IF NOT EXISTS spends (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date_Spends INTEGER,
  name TEXT NOT NULL,
  summ INTEGER
);
"""
create_Income_table = """
CREATE TABLE IF NOT EXISTS incomes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date_Incomes INTEGER,
  name TEXT NOT NULL,
  summ INTEGER
);
"""
#########################################33
#Создаем таблицы
execute_query(connection, create_Spends_table)
execute_query(connection, create_Income_table)
#############################################################
All_data_Base = 'adb'
Data_Base = 'db'
try_set = 0
agree = ''
happy_input_income = None
happy = False
happy_input_spends = None
Add_Spends = None

Income_Categories ={}
Spends_Categories ={}

income_load = 0
spends_load = 0
############################################################
#Чтение бд
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

##############################################################
#Вывод
select_spends = "SELECT * from spends"
spends = execute_read_query(connection, select_spends)

print('You Spends is')
print(spends)

select_income = "SELECT * from incomes"
incomes = execute_read_query(connection, select_income)

print('You incomes is')
print(incomes)
######################################################
#Вывод всех расходов
select_summ_spends = "SELECT summ from spends"
summ_spends_print = execute_read_query(connection, select_summ_spends)

#########################################################
#Вывод суммы расходов
def spends_summ():
	numbers_in_Spends = len(summ_spends_print)
	spends_sum_tuple = tuple()

	for i in range(numbers_in_Spends):
	    spends_sum_tuple += summ_spends_print[i]
	    global sums_spendes
	    sums_spendes = sum(spends_sum_tuple)
	    

	print('ALL Spends is: ')
	print(sums_spendes)

spends_summ()

###########################################################
select_summ_incomes = "SELECT summ from incomes"
summ_incomes_print = execute_read_query(connection, select_summ_incomes)

#########################################################
#Вывод суммы доходов
def incomes_summ():
	numbers_in_Incomes = len(summ_incomes_print)
	incomes_sum_tuple = tuple()

	for i in range(numbers_in_Incomes):
	    incomes_sum_tuple += summ_incomes_print[i]
	    global sums_incomes
	    sums_incomes = sum(incomes_sum_tuple)
	    

	print('ALL Incomes is: ')
	print(sums_incomes)

incomes_summ()
#########################################################
#Вывод бюджета
print('You have is:')
print(sums_incomes - sums_spendes)


################################################################
#Подсчет всех расходов
#select_all_spendes = "SELECT "
#############################################################
#Открыть всю базу
with open(All_data_Base, "r") as f:
    All_Base_read = f.read()

#Открыть последние изменения в базе
with open(Data_Base, 'rb') as g:
    Data_Base_Load = pickle.load(g)

#############################################################
print('All times:')
try:
    print(All_Base_read)
except:
    print('All_data_Base don`t find')

print('Last time:')
print(Data_Base_Load)

###############################################################
Money = 0

for k in Data_Base_Load['Income'].values():
	income_load += int(k)
print('You last income is', income_load)
for s in Data_Base_Load['Spends'].values():
	spends_load += int(s)
print('You last Spends is', spends_load)
Money = income_load - spends_load
print('You last have is ' + str(Money))
#################################################################################
##############################################################################
#Функция вставки в базу данных

def insert_varible_into_table_spends(date_spends, name, summ):
    try:
        sqlite_connection = sqlite3.connect(Data_Base_sql)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = """INSERT INTO spends
                              (date_spends, name, summ)
                              VALUES (?, ?, ?);"""

        data_tuple = (date_spends, name, summ)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу spends")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def insert_varible_into_table_incomes(date_incomes, name, summ):
    try:
        sqlite_connection = sqlite3.connect(Data_Base_sql)
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_with_param = """INSERT INTO incomes
                              (date_incomes, name, summ)
                              VALUES (?, ?, ?);"""

        data_tuple = (date_incomes, name, summ)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Переменные Python успешно вставлены в таблицу incomes")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
#########################################################################################
###################################################################
#в зависимости от количества неудачных попыток, спрашивает пользователя и либо отключает его

def Check_try_set():
    if try_set == 3:
        print('Do you want use this program?(Yes\\No)')
        print('Input here:')
        global agree
        agree = input()
        if agree == 'Yes':
            print('OK, lets try this')
            return
            Input_Spends()
        elif agree == 'No':
            print('Goodbye =)')
            sys.exit()
        else:
            print('You was expected')
            Check_try_set()
    if try_set == 6:
        feedback()
        return

########################################################################

def feedback():
    print('what are you problem? We will fix this')
    print('Input here:')
    feedback = input()
    print('We are so sorry, but we make all in our oppotunity')
    print('Goodbye (=')
    sys.exit()

##########################################################################

def Check_My_Balance():
    print('You have:' + str(Money))

###############################################################################

def expected_redacted():
	print('You was expected. Do you want rerty?(Yes/No)')
	expected_try = input()
	if expected_try == 'Yes':
		happy_input_spends = False
		print('Ok')
		Check_My_Balance()
	elif expected_try == 'No':
		print('Goodbye =)')
		sys.exit()
	else:
		print('You was expected. Sorry')
		feedback()

############################################################################
#Ввод расходов
#############################################################################

def Input_Spends():
    Chickle_Input_Spends()
    Add_Spends()

#####################################################################
#цикл ввода
#####################################################################
def Chickle_Input_Spends():
    global try_set
    global happy_input_spends
    while(happy_input_spends != True and try_set < 6):
        if agree == 'No':
            return
        print('What did you spend your money on?')
        global Input_Categories_Spends
        Input_Categories_Spends = input()
        Input_Spends_Check = 'Input your spendes:'
        Check_Correctly(Input_Spends_Check)
        happy_input_spends = True
        global Spends_Categories
        Redacted_Spends()
######################################################################
#Вычет трат
######################################################################
def Minus_Money():
    global Money
    Money -= int(input_text_money)
    Check_My_Balance()

######################################################################
#Редактор ввода
#######################################################################                

def Redacted_Spends():
    print('Do yo want redacted this?(Yes/No)')
    Redacted_Input_Spends = input()
    if Redacted_Input_Spends == 'Yes':
        print('Ok')
        Check_My_Balance()
        global happy_input_spends
        happy_input_spends = False
    elif Redacted_Input_Spends == 'No':
        Minus_Money()
        Spends_Categories[Input_Categories_Spends] = Input_How_Many_Spends
        date_spends = datetime.datetime.now()
        insert_varible_into_table_spends(date_spends, Input_Categories_Spends, Input_How_Many_Spends)
    else:
        expected_redacted()

########################################################################
#Добавить расходы
########################################################################
def Add_Spends():
    print('Do you want add spends?(Yes/No)')
    global Add_Spends_input
    Add_Spends_input = input()
    if Add_Spends_input == 'Yes':
        print('Ok')
        Check_My_Balance()
        global happy_input_spends
        happy_input_spends = False
        Input_Spends()
    elif Add_Spends_input == 'No':
        Input_Income()
    else:
        print('You was expected. Sorry')
        expected_redacted()

##########################################################################
#Ввести доходы
##########################################################################

def Input_Income():
    Cikle_Input_Income()
    Add_Income()

##############################################################################3
#Цикл ввода доходов
##############################################################
def Cikle_Input_Income():
    global try_set
    global happy_input_income
    while(happy_input_income != True and try_set < 6):
        if agree == 'No':
            return
        print('What did you income your money on?')
        global Input_Categories_Income
        Input_Categories_Income = input()
        Input_Income_Check = 'Input your income:'
        Check_Correctly(Input_Income_Check)
        happy_input_income = True
        global Spends_Categories
        Redacted_Income()
####################################################################
#Добавить доходы
def Add_Income():
    print('Do you want add income?(Yes/No)')
    global Add_Income_Input
    Add_Income_Input = input()
    if Add_Income_Input == 'Yes':
        print('Ok')
        Check_My_Balance()
        global happy_input_income
        happy_input_income = False
        Input_Income()
    elif Add_Income_Input == 'No':
        Check_My_Balance()
    else:
        print('You was expected')
        expected_redacted()

################################################################
#Редактор ввода доходов
def Redacted_Income():
    print('Do yo want redacted this?(Yes/No)')
    Redacted_Input_Income = input()
    if Redacted_Input_Income == 'Yes':
        global happy_input_income
        happy_input_income = False
        print('Ok')
    elif Redacted_Input_Income == 'No':
        Plus_Money()
        Income_Categories[Input_Categories_Income] = Input_How_Many_Income
        date_incomes = datetime.datetime.now()
        insert_varible_into_table_incomes(date_incomes, Input_Categories_Income, Input_How_Many_Income)
    else:
        expected_redacted()
##############################################################
#Сложение дохода
##############################################################

def Plus_Money():
    global Money
    Money += int(input_text_money)
    Check_My_Balance()

#############################################################
#Проверяет(доходы и расходы), чтоб только числа были

def Check_Correctly(input_text):
    if happy_input_income == True:
         return
    else:
        Check_Correctly_Input(input_text)

####################################################################
#Проверка цифр
def Check_Correctly_Input(input_text):
    try:
        print(input_text)
        global text
        text = input_text
        global input_text_money
        input_text_money = input()
        if text == 'Input your spendes:':
            Money = 0
            Money -= int(input_text_money)
            global Input_How_Many_Spends
            Input_How_Many_Spends = input_text_money
        else:
            Money = 0
            Money += int(input_text_money)
            global Input_How_Many_Income
            Input_How_Many_Income = input_text_money
            Check_My_Balance()
    except:
        print('You was expected')
        global try_set
        try_set += 1
        Check_try_set()
        if text == 'Input your spendes:':
            Input_Spends()
        else:
            Input_Income()
###################################################################
#Проверка цифр - блок try
def Check_Correctly_Input_Try(input_text):

###################################################################
    try:
        Check_My_Balance()
    except:
        print('You don`t have money')
        Money = 0
#######################################################################
#Начало
Input_Spends()

######################################################################
#Сохранение базы данных
Money_Save = {}
Money_Save['Spends'] = Spends_Categories
Money_Save['Income'] = Income_Categories

##############################################################
#Запись последних изменений в отдельный файл
with open(Data_Base, 'wb') as g:
    pickle.dump(Money_Save, g)

#Дозапись последних изменений в весь бюджет
Money_Save_Base = str(Money_Save)
with open(All_data_Base, 'a') as g:
    g.write(Money_Save_Base)

#Записываем в базу данных sql
#for k in Spends_Categories.keys():
    #insert_varible_into_table_spends(k, a)

#for k in Income_Categories.keys():
    #a = Income_Categories[key]
    #insert_varible_into_table_spends(k, a)

















