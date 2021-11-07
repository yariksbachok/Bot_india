from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import database
import logic
import text


db = database.DBConnection()

def start_keyboard(id_user):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='Пополнить', callback_data='add_pay'),
               InlineKeyboardButton(text='Вывести', callback_data='Withdraw'))
    inline.add(InlineKeyboardButton(text='Проверить оплату', callback_data='chek_pay'))
    row = db.chek_user(id_user)
    if row[4] == 0:
        inline.add(InlineKeyboardButton(text='Рефералка', callback_data='referal_user'))
    inline.add(InlineKeyboardButton(text='Иныестировать', callback_data='invest_now'))
    return inline


def close_state():
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='Close', callback_data='close_state'))
    return inline

def close_invest(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=logic.translet('reinvest_all', id), callback_data='all_invest'))
    inline.add(InlineKeyboardButton(text=logic.translet('close', id), callback_data='close_state'))
    return inline

def select_lang():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Английский'), KeyboardButton(text='Индийский'))
    return keyboard

def main_menu(id):
    button = ReplyKeyboardMarkup(resize_keyboard=True)
    list_text = logic.translet('main_menu', id)
    n = 0
    t = ''
    for i in list_text:
        n+=1
        if n % 2 == 0:
            button.add(KeyboardButton(text=t), KeyboardButton(text=i))
        t = i

    return button

def inline_my_bank(id):
    row = db.chek_user(id)
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=text.data_text[row[10]]['up_pay'], callback_data='up_pay'), InlineKeyboardButton(text=text.data_text[row[10]]['withdraw'], callback_data='withdraw'))
    inline.add(InlineKeyboardButton(text=text.data_text[row[10]]['reinvest'],callback_data='reinvest'), InlineKeyboardButton(text=text.data_text[row[10]]['history'], callback_data='history'))

    return inline

def inline_setting(id):
    button = InlineKeyboardMarkup()
    button.add(InlineKeyboardButton(text=logic.translet('change_lang', id), callback_data='change_lang'), InlineKeyboardButton(text=logic.translet('paymet_detail', id), callback_data='paymet_detail'))
    button.add(InlineKeyboardButton(text=logic.translet('instal_invate', id),callback_data='instal_invate'))

    return button

def inline_about_us(id):
    button = InlineKeyboardMarkup()
    button.add(InlineKeyboardButton(text=logic.translet('Community', id), callback_data='Community'), InlineKeyboardButton(text=logic.translet('partners', id), callback_data='partners'))
    button.add(InlineKeyboardButton(text=logic.translet('support', id), callback_data='support'))

    return button

def btn_payment_detal(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=logic.translet('btc_paymet', id), callback_data='btc_paymet'), InlineKeyboardButton(text=logic.translet('eth_payment', id), callback_data='eth_payment'))
    inline.add(InlineKeyboardButton(text=logic.translet('back', id), callback_data='back_detail_payment'))

    return inline

def btn_cancel(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=logic.translet('cancel', id), callback_data='cancel'))

    return inline

def up_pay_select_sum(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='100', callback_data=f'up_pay_sum:{100}'), InlineKeyboardButton(text='500', callback_data=f'up_pay_sum:{500}'), InlineKeyboardButton(text='1000', callback_data=f'up_pay_sum:{1000}'))
    inline.add(InlineKeyboardButton(text='2000', callback_data=f'up_pay_sum:{2000}'), InlineKeyboardButton(text='3000', callback_data=f'up_pay_sum:{3000}'), InlineKeyboardButton(text='50000', callback_data=f'up_pay_sum:{5000}'))
    inline.add(InlineKeyboardButton(text=logic.translet('back', id), callback_data='back_my_bank'))

    return inline

def choose_pay(text, id):
    sum = text.split(':')[1]
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=logic.translet('cryptocurrency', id),callback_data=f'crypto_pay:{sum}'))
    inline.add(InlineKeyboardButton(text=logic.translet('hi_bank', id), callback_data='hi_bank'))
    inline.add(InlineKeyboardButton(text=logic.translet('back', id), callback_data='back_my_bank'))

    return inline

def cryptocurrency_pay(text, id):
    sum = text.split(':')[1]
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='paytm', callback_data='paytm_gray_phonese'), InlineKeyboardButton(text='gpay', callback_data='paytm_gray_phonese'), InlineKeyboardButton(text='phonePE', callback_data='paytm_gray_phonese'))
    inline.add(
        InlineKeyboardButton(text=logic.translet('cryptocurrency', id), callback_data=f'cryptocurrency_pay:{sum}'))
    inline.add(InlineKeyboardButton(text=logic.translet('back', id), callback_data='back_my_bank'))

    return inline

def pay_BTC_or_ETH(text, id):
    sum = text.split(':')[1]
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='BTC', callback_data=f'he_pay_BTC:{sum}'))
    inline.add(InlineKeyboardButton(text='ETH', callback_data=f'he_pay_ETH:{sum}'))
    inline.add(InlineKeyboardButton(text=logic.translet('back', id), callback_data='back_my_bank'))

    return inline

def btn_examination_pay(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=logic.translet('check_payment',id), callback_data='check_payment'))

    return inline

def withdraw(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='💸 Bitcoin', callback_data='btc_withdraw'), InlineKeyboardButton(text='💸 Ethereum', callback_data='eth_withdraw'))
    inline.add(InlineKeyboardButton(text=logic.translet('back', id), callback_data='back_my_bank'))

    return inline

def withdraw_select_sum(calldata):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='300', callback_data=f'with_pay:{calldata}:{300}'), InlineKeyboardButton(text='500', callback_data=f'with_pay:{calldata}:{500}'), InlineKeyboardButton(text='1000', callback_data=f'with_pay:{calldata}:{1000}'))
    inline.add(InlineKeyboardButton(text='2000', callback_data=f'with_pay:{calldata}:{2000}'), InlineKeyboardButton(text='3000', callback_data=f'with_pay:{calldata}:{3000}'), InlineKeyboardButton(text='50000', callback_data=f'with_pay:{calldata}:{5000}'))

    return inline

def excetly_withdraw(id, withdraw, sum):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=logic.translet('excetly_done', id), callback_data=f'excetly_done:{withdraw}:{sum}'), InlineKeyboardButton(text=logic.translet('excetly_cancel', id), callback_data='excetly_cancel'))

    return inline

def done_or_not_reinvest(sum, id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=logic.translet('yes_reinvest', id) , callback_data=f'yes_reinvest:{sum}'), InlineKeyboardButton(text=logic.translet('not_reinvest', id), callback_data='not_reinvest'))

    return inline

def btn_my_referals(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=logic.translet('my_team', id), callback_data='my_team'), InlineKeyboardButton(text=logic.translet('btn_me_invate', id), callback_data='btn_me_invate'))
    inline.add(InlineKeyboardButton(text=logic.translet('create_referal_link', id), callback_data='create_referal_link'))

    return inline

def btn_admin():
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text='Рассылка', callback_data='spam_sms'), InlineKeyboardButton(text='Статистика', callback_data='statistic_admin'))

    return inline

def back_my_bank(id):
    inline = InlineKeyboardMarkup()
    inline.add(InlineKeyboardButton(text=logic.translet('back', id), callback_data='back_my_bank'))

    return inline