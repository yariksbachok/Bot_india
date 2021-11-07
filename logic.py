from coinpayments import CoinPaymentsAPI
from aiogram.dispatcher.filters.state import State, StatesGroup
import xlsxwriter
import os
import config
import database
import text
import asyncio
import json

db = database.DBConnection()

api = CoinPaymentsAPI(public_key=config.api_public_key,
                          private_key=config.api_private_key)

class For_state(StatesGroup):
    referal_user = State()
    invest_quantly = State()
    btc_address = State()
    eth_address = State()
    settings = State()
    btc_or_eth = State()
    spam_sms = State()

def start_work(id):
    row = db.chek_user(id)
    if row == None:
        address = 'None'
        db.add_USER(id, address, 0, 0, 0, 0, 0, 0, 0, 0, 'ty', 'None', 'None')
    else:
        pass

def translet(func, id):
    row = db.chek_user(id)
    my_text = text.data_text[row[10]][func]
    return my_text

async def log_interest_accrual():
    row = db.chek_all_user()
    for _ in row:
        id_user = _[0]
        balance_invest = _[2]
        first_releral = _[4]
        second_referal = _[5]
        three_referal = _[6]
        four_referal = _[7]
        five_referal = _[8]
        me_balance = round(balance_invest / 100 * config.today_proc, 0)
        first_balance = round(balance_invest / 100 * config.first_releral, 0)
        second_balance = round(balance_invest / 100 * config.second_referal, 0)
        three_balance = round(balance_invest / 100 * config.three_referal, 0)
        four_balance = round(balance_invest / 100 * config.four_referal, 0)
        five_balance = round(balance_invest / 100 * config.five_referal, 0)
        data = {id_user:me_balance, first_releral:first_balance, second_referal:second_balance, three_referal:three_balance, four_referal:four_balance, five_referal:five_balance}
        await change_invest_investbal_all(data)
        await plus_today_proc(data)

async def change_invest_investbal_all(data):
    for k, v in data.items():
        if k != 0 or k != None:
            try:
                row = db.chek_user(k)
                if row[3] == 0 and v == 0.:
                    pass
                else:
                    invest = row[3] + v
                    progres = row[9] + v
                    db.updateBalanceUser(invest, k)
                    db.updateProgres(progres, k)
            except:
                pass
        else:
            break


def change_balance(tex, id, row):
    invest = row[2] + float(tex)
    db.updateInvestUser(invest, id)
    balance = row[3] - float(tex)
    db.updateBalanceUser(balance, id)

def func_referal(id_ref, id_user):
    row = db.chek_user(id_ref)
    row_user = db.chek_user(id_user)
    if row == None:
        return False
    else:
        if row_user[4] == 0:
            list_referal = [id_ref, row_user[4], row_user[5], row_user[6], row_user[7]]
            add_referal_user(list_referal, id_user)
            return True
        else:
            return False

def add_referal_user(list_user, id_user):
    n = 0
    for i in list_user:
        n += 1
        if n == 1:
            db.updateFirstReferal(i, id_user)

        elif n == 2:
            db.updateSecondReferal(i, id_user)

        elif n == 3:
            db.updateThreeReferal(i, id_user)

        elif n == 4:
            db.updateFourReferal(i, id_user)

        elif n == 5:
            db.updateFiveReferal(i, id_user)


def create_adress(amount, currency1, id_user):
    # pi = api.get_callback_address(currency='BTC', label=str(id))
    # address = pi['result']['address']
    # return address
    sum = amount.split(':')[1]
    pi = api.create_transaction(amount=sum, currency1='INR', currency2=currency1, buyer_email='yarikolesnik@ukr.net')
    address = pi['result']['address']
    txn_id = pi['result']['txn_id']
    db.updateWallet(txn_id, id_user)

    return address

def all_invest(id):
    row = db.chek_user(id)
    change_balance(row[3], id, row)


def get_text_in(id):
    row = db.chek_user(id)
    pi = api.get_tx_info()

def examination_pay(id):
    row = db.chek_user(id)
    pi = api.get_tx_info(txid=row[1])
    return pi

def send_money(btc_or_eth, sum, id):
    row = db.chek_user(id)
    if btc_or_eth == 'btc':
        curr = 'BTC'
        addres = row[11]
    elif btc_or_eth == 'eth':
        curr = 'ETH'
        addres = row[12]
    db.add_history(id, 'Withdraw funds', sum)
    api.create_withdrawal(amount=sum, currency=curr, currency2='INR', address=addres)

async def history_to_excel(id):
    if os.path.isfile(f'exel_file/{id}.xlsx') == True:
        os.remove(f'exel_file/{id}.xlsx')

    workbook = xlsxwriter.Workbook(f'exel_file/{id}.xlsx')
    worksheet = workbook.add_worksheet()

    sum = []
    payments = []
    row = db.chek_history(id)
    for i in row:
        payments.append(i[1])
        sum.append(i[2])
    await write_in_excel(worksheet, sum, column=0)
    await write_in_excel(worksheet, payments, column=1)

    workbook.close()

async def plus_today_proc(data):
    for k, v in data.items():
        try:
            if k != 0 or v != 0:
                row = db.chek_today_proc(k)
                all_sum = row[1] + v
                db.add_today_proc(k, all_sum)
        except:
            pass

async def send_today_all_proc(bot):
    row = db.chek_today_all_proc()
    for i in row:
        await bot.send_message(i[0], text=translet('today_profit', i[0]).format(i[1]))

async def write_in_excel(worksheet, list, column):
    row = 0
    for i in list:
        worksheet.write(row, column, i)
        row += 1

def all_info_invest(id):
    first = db.chek_first_referal(id)
    second = db.chek_second_referal(id)
    three = db.chek_three_referall(id)
    four = db.chek_four_referal(id)
    five = db.chek_five_referal(id)
    first_not_pay = db.chek_first_referal_not_pay(id)
    second_not_pay = db.chek_second_referal_not_pay(id)
    three_not_pay = db.chek_three_referall_not_pay(id)
    four_not_pay = db.chek_four_referal_not_pay(id)
    five_not_pay = db.chek_five_referal_not_pay(id)
    f_len = len(first)
    second_l = len(second)
    three_l = len(three)
    four_l = len(four)
    five_l = len(five)
    f_len_not_pay = len(first_not_pay)
    second_l_not_pay = len(second_not_pay)
    three_l_not_pay = len(three_not_pay)
    four_l_not_pay = len(four_not_pay)
    five_l_not_pay = len(five_not_pay)
    all_len = int(f_len)+int(second_l)+int(three_l)+int(four_l)+int(five_l)
    all_len_not_pay = int(f_len_not_pay)+int(second_l_not_pay)+int(three_l_not_pay)+int(four_l_not_pay)+int(five_l_not_pay)
    not_pay = all_len - all_len_not_pay
    all_sum_invest = plus_sum_all_user_invset([first, second, three, four, five])
    not_first_all = plus_sum_all_user_balance([second, three, four, five])
    first_invest = all_first_progres(first)

    return all_len, not_pay, all_sum_invest, first_invest, not_first_all

def plus_sum_all_user_invset(list):
    sum = 0
    for i in list:
        for j in i:
            sum+=j[2]

    return sum

def plus_sum_all_user_balance(list):
    sum = 0
    for i in list:
        for j in i:
            sum+=j[9]

    return sum

def all_first_progres(data):
    sum = 0
    for i in data:
        sum += i[9]

    return sum

def level_id(id):
    if os.path.isfile(f'exel_file/{id}.xlsx') == True:
        os.remove(f'exel_file/{id}.xlsx')

    workbook = xlsxwriter.Workbook(f'exel_file/{id}.xlsx')
    worksheet = workbook.add_worksheet()
    first = db.chek_first_referal(id)
    second = db.chek_second_referal(id)
    three = db.chek_three_referall(id)
    four = db.chek_four_referal(id)
    five = db.chek_five_referal(id)
    list = [first, second, three, four, five]
    column= 0
    row = 0
    for i in list:
        for j in i:
            worksheet.write(row, column, str(j[0]))
            row += 1

    workbook.close()

async def start_referal(bot, id_referal, id_user):
    bool = func_referal(int(id_referal), id_user)
    if bool == True:
        await bot.send_message(id_user, text=translet('id_surefly', id_user))
    else:
        await bot.send_message(id_user, text=translet('eror_referal', id_user).format(id_referal))

