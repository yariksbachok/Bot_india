from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
import asyncio
import text
import config
import keyboard
import database
import logic

bot = Bot(token=config.token, parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())

db = database.DBConnection()
db.create_tables()

@dp.message_handler(state=logic.For_state.referal_user)
async def referal_user(message: types.Message, state: FSMContext):
    tex = message.text
    if tex.isdigit():
        bool = logic.func_referal(int(tex), message.from_user.id)
        if bool == True:
            await bot.send_message(message.chat.id, text=logic.translet('id_surefly', message.from_user.id))
            await state.finish()
        else:
            await bot.send_message(message.chat.id, text=logic.translet('eror_referal', message.from_user.id).format(tex))
            await state.finish()

    else:
        inline = keyboard.btn_cancel(message.from_user.id)
        await bot.send_message(message.chat.id, text=logic.translet('return_referal', message.from_user.id), reply_markup=inline)
        await logic.For_state.referal_user.set()

@dp.message_handler(state=logic.For_state.spam_sms)
async def spam_sms(message: types.Message, state: FSMContext):
    tex = message.text
    loop = asyncio.get_event_loop()
    loop.create_task(send_spam_sms(tex))
    inline = keyboard.btn_admin()
    await bot.send_message(message.chat.id, text='Рассылка запущенна', reply_markup=inline)
    await state.finish()



@dp.message_handler(state=logic.For_state.btc_address)
async def btc_address(message: types.Message, state: FSMContext):
    tex = message.text
    id = message.chat.id
    user_data = await state.get_data()
    settings = user_data['settings']
    db.updateBtc(tex, id)
    if settings == 'no':
        btc_or_eth = user_data['btc_or_eth']
        withdraw = btc_or_eth.split(':')[0]
        sum = btc_or_eth.split(':')[1]
        await bot.send_message(message.chat.id, text=logic.translet('excetly_withdraw', message.from_user.id),
                               reply_markup=keyboard.excetly_withdraw(message.from_user.id, withdraw, sum))
        await state.finish()
    else:
        txt = logic.translet('cheng_address_done',id)
        row = db.chek_user(id)
        txt += logic.translet('payment_txt', id).format(row[11], row[12])
        inline = keyboard.btn_payment_detal(id)
        await bot.send_message(id, text=txt, reply_markup=inline)

@dp.message_handler(state=logic.For_state.eth_address)
async def btc_address(message: types.Message, state: FSMContext):
    tex = message.text
    id = message.chat.id
    user_data = await state.get_data()
    settings = user_data['settings']
    db.updateEth(tex, id)
    if settings == 'no':
        btc_or_eth = user_data['btc_or_eth']
        withdraw = btc_or_eth.split(':')[0]
        sum = btc_or_eth.split(':')[1]
        await bot.send_message(message.chat.id, text=logic.translet('excetly_withdraw', message.from_user.id),
                               reply_markup=keyboard.excetly_withdraw(message.from_user.id, withdraw, sum))
        await state.finish()
    else:
        txt = logic.translet('cheng_address_done',id)
        row = db.chek_user(id)
        txt += logic.translet('payment_txt', id).format(row[11], row[12])
        inline = keyboard.btn_payment_detal(id)
        await bot.send_message(id, text=txt, reply_markup=inline)

@dp.message_handler(state=logic.For_state.invest_quantly)
async def invest_quantly(message: types.Message, state: FSMContext):
    tex = message.text
    if tex.isdigit():
        row = db.chek_user(message.from_user.id)
        if float(tex) <= row[3]:
            await bot.send_message(message.chat.id, text=logic.translet('text_you_done_reinvest', message.chat.id).format(tex), reply_markup=keyboard.done_or_not_reinvest(tex, message.chat.id))
            await state.finish()
        else:
            inline = keyboard.close_invest(message.chat.id)
            await bot.send_message(message.chat.id, text=logic.translet('send_reinvest_text', message.chat.id),
                                   reply_markup=inline)
            await logic.For_state.invest_quantly.set()
    else:
        inline = keyboard.close_invest(message.chat.id)
        await bot.send_message(message.chat.id, text=logic.translet('send_reinvest_text', message.chat.id),
                               reply_markup=inline)
        await logic.For_state.invest_quantly.set()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    row = db.chek_user(message.from_user.id)
    if row == None:
        button = keyboard.select_lang()
        txt = text.data_text['en']['select_lang']
        await bot.send_message(message.chat.id, text=txt, reply_markup=button)
        logic.start_work(message.from_user.id)
    elif row[10] == 'ty':
        button = keyboard.select_lang()
        txt = text.data_text['en']['select_lang']
        await bot.send_message(message.chat.id, text=txt, reply_markup=button)
        logic.start_work(message.from_user.id)
        config.Static.today += 1
        config.Static.week += 1
    else:
        print(row)
        txt = logic.translet('hello', message.from_user.id)
        button = keyboard.main_menu(message.from_user.id)
        await bot.send_message(message.chat.id, text=txt, reply_markup=button)

    try:
        referal = message.text.split()[1]
        bool = logic.func_referal(int(referal), message.from_user.id)
        if bool == True:
            await bot.send_message(message.from_user.id, text=logic.translet('id_surefly', message.from_user.id))
        else:
            await bot.send_message(message.from_user.id, text=logic.translet('eror_referal', message.from_user.id).format(referal))
    except:
        pass

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if message.from_user.id in config.admin_id:
        inline = keyboard.btn_admin()
        await bot.send_message(message.chat.id, text='Вы в админ панели', reply_markup=inline)

@dp.callback_query_handler(lambda c: c.data, state="*")
async def callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'add_pay':
        row = db.chek_user(call.from_user.id)
        await bot.send_message(call.message.chat.id, text=f'Ваш BTC-адресс: {row[1]}')
    elif call.data == 'withdraw':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=logic.translet('select_pay_text', call.from_user.id), reply_markup=keyboard.withdraw(call.from_user.id))

    elif call.data == 'spam_sms':
        inline = keyboard.btn_cancel(call.from_user.id)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.message.chat.id, text='ведите текст для рассылки', reply_markup=inline)
        await logic.For_state.spam_sms.set()

    elif call.data == 'statistic_admin':
        await bot.send_message(call.message.chat.id, text=f'Статистика:\n'
                                                          f'За день пришло юзеров в бота: {config.Static.today}\n'
                                                          f'За неделюпришло юзеров:{config.Static.week}')

    elif call.data == 'referal_user':
        inline = keyboard.close_state()
        await bot.send_message(call.message.chat.id, text='Уведите id который вас пригласил', reply_markup=inline)
        await logic.For_state.referal_user.set()

    elif call.data == 'close_state':
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    elif call.data == 'reinvest':
        inline = keyboard.close_invest(call.from_user.id)
        await bot.send_message(call.message.chat.id, text=logic.translet('send_reinvest_text', call.from_user.id), reply_markup=inline)
        await logic.For_state.invest_quantly.set()

    elif call.data == 'all_invest':
        logic.all_invest(call.from_user.id)
        await bot.send_message(call.from_user.id, text=logic.translet('done_reinvest', call.from_user.id))

        await state.finish()

    elif call.data == 'paymet_detail':
        row = db.chek_user(call.from_user.id)
        txt = logic.translet('payment_txt', call.from_user.id).format(row[11], row[12])
        inline = keyboard.btn_payment_detal(call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=txt, reply_markup=inline)

    elif call.data == 'back_detail_payment':
        inline = keyboard.inline_setting(call.from_user.id)
        row = db.chek_user(call.from_user.id)
        txt = logic.translet('menu_settings', call.from_user.id).format(str(call.from_user.id), row[10])
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=txt, reply_markup=inline)

    elif call.data == 'btc_paymet':
        txt = logic.translet('send_btc_adr', call.from_user.id)
        inline = keyboard.btn_cancel(call.from_user.id)
        await bot.send_message(call.message.chat.id, text=txt, reply_markup=inline)
        await state.update_data(settings='yes')

        await logic.For_state.btc_address.set()

    elif call.data == 'eth_payment':
        txt = logic.translet('send_eth_adr', call.from_user.id)
        inline = keyboard.btn_cancel(call.from_user.id)
        await bot.send_message(call.message.chat.id, text=txt, reply_markup=inline)
        await state.update_data(settings='yes')

        await logic.For_state.eth_address.set()

    elif call.data == 'paytm_gray_phonese':
        await bot.send_message(call.message.chat.id, text=logic.translet('paytm_gray_phonese', call.from_user.id))

    elif call.data == 'cancel':
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    elif call.data == 'change_lang':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        button = keyboard.select_lang()
        txt = logic.translet('text_cahnge_lang', call.from_user.id)
        await bot.send_message(call.message.chat.id, text=txt, reply_markup=button)

    elif call.data == 'instal_invate':
        inline = keyboard.btn_cancel(call.from_user.id)
        txt = logic.translet('send_me_id', call.from_user.id)
        await bot.send_message(call.message.chat.id, text=txt, reply_markup=inline)

        await logic.For_state.referal_user.set()

    elif call.data == 'up_pay':
        inline = keyboard.up_pay_select_sum(call.from_user.id)
        txt = logic.translet('select_sum_up_pay', call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=txt, reply_markup=inline)

    elif call.data == 'hi_bank':
        inline = keyboard.back_my_bank(call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=logic.translet('send_admin', call.from_user.id), reply_markup=inline)

    elif call.data == 'back_my_bank':
        txt = logic.translet('my_bank', call.from_user.id)
        row = db.chek_user(call.from_user.id)
        txt = txt.format(row[3], row[2], row[9])
        inline = keyboard.inline_my_bank(call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=txt, reply_markup=inline)

    elif call.data == 'check_payment':
        t = logic.examination_pay(call.from_user.id)
        await bot.send_message(call.message.chat.id, text=t)

    elif call.data == 'btc_withdraw':
        await bot.send_message(call.message.chat.id, text=logic.translet('select_sum_up_pay', call.from_user.id), reply_markup=keyboard.withdraw_select_sum('btc'))

    elif call.data == 'eth_withdraw':
        await bot.send_message(call.message.chat.id, text=logic.translet('select_sum_up_pay', call.from_user.id), reply_markup=keyboard.withdraw_select_sum('eth'))

    elif call.data == 'excetly_cancel':
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_message(call.message.chat.id, text=logic.translet('money_send_cancel', call.from_user.id))

    elif call.data == 'not_reinvest':
        await bot.send_message(call.message.chat.id, text=logic.translet('cancel_reinvest', call.from_user.id))

    elif call.data == 'history':
        await bot.send_message(call.from_user.id, text=logic.translet('pls_wait', call.from_user.id))
        loop = asyncio.get_event_loop()
        loop.create_task(logic.history_to_excel(call.from_user.id))
        f = open(f'exel_file/{call.from_user.id}.xlsx', "rb")
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await bot.send_document(chat_id=call.from_user.id, document=f)

    elif call.data == 'btn_me_invate':
        row = db.chek_user(call.from_user.id)
        if row[4] == 0:
            await bot.send_message(call.message.chat.id, text=logic.translet('he_not_referal', call.from_user.id))
        else:
            await bot.send_message(call.from_user.id, text=logic.translet('who_referal', call.from_user.id).format(row[4]))

    elif call.data == 'my_team':
        msg = await bot.send_message(call.from_user.id, text=logic.translet('pls_wait', call.from_user.id))
        logic.level_id(call.from_user.id)
        f = open(f'exel_file/{call.from_user.id}.xlsx', "rb")
        await bot.delete_message(chat_id=call.from_user.id, message_id=msg.message_id)
        await bot.send_document(chat_id=call.from_user.id, document=f)

    elif call.data == 'create_referal_link':
        await bot.send_message(call.message.chat.id, text=f'http://t.me/test1234tebot?start={call.from_user.id}')

    elif 'yes_reinvest' in call.data:
        sum = call.data.split(':')[1]
        row = db.chek_user(call.from_user.id)
        logic.change_balance(sum, call.from_user.id, row)
        await bot.send_message(call.from_user.id, text=logic.translet('done_reinvest', call.from_user.id))

    elif 'up_pay_sum' in call.data:
        txt = logic.translet('choose_pay', call.from_user.id)
        inline = keyboard.choose_pay(call.data, call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=txt, reply_markup=inline)

    elif 'cryptocurrency_pay' in call.data:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=logic.translet('select_pay_text', call.from_user.id), reply_markup=keyboard.pay_BTC_or_ETH(call.data, call.from_user.id))

    elif 'crypto_pay' in call.data:
        inline = keyboard.cryptocurrency_pay(call.data, call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=logic.translet('select_pay_method', call.from_user.id), reply_markup=inline)

    elif 'he_pay_BTC' in call.data:
        address = logic.create_adress(call.data, 'BTC', call.from_user.id)
        txt = logic.translet('send_adrs', call.from_user.id).format(address)
        inline = keyboard.btn_examination_pay(call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=txt, reply_markup=inline)

    elif 'he_pay_ETH' in call.data:
        address = logic.create_adress(call.data, 'ETH', call.from_user.id)
        txt = logic.translet('send_adrs', call.from_user.id).format(address)
        inline = keyboard.btn_examination_pay(call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=txt, reply_markup=inline)

    elif 'with_pay' in call.data:
        print(call.data)
        withdraw = call.data.split(':')[1]
        sum = call.data.split(':')[2]
        row = db.chek_user(call.from_user.id)

        if withdraw == 'btc':
            if row[11] == 'None':
                await state.update_data(settings='no')
                await state.update_data(btc_or_eth=f'{withdraw}:{sum}')
                txt = logic.translet('send_btc_adr', call.from_user.id)
                inline = keyboard.btn_cancel(call.from_user.id)
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=txt, reply_markup=inline)
                await logic.For_state.btc_address.set()
            else:
                await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=logic.translet('excetly_withdraw', call.from_user.id), reply_markup=keyboard.excetly_withdraw(call.from_user.id, withdraw, sum))

        elif withdraw == 'eth':
            if row[12] == 'None':
                await state.update_data(settings='no')
                await state.update_data(btc_or_eth=f'{withdraw}:{sum}')
                txt = logic.translet('send_btc_adr', call.from_user.id)
                inline = keyboard.btn_cancel(call.from_user.id)
                await bot.send_message(call.message.chat.id, text=txt, reply_markup=inline)
                await logic.For_state.eth_address.set()
            else:
                await bot.send_message(call.message.chat.id, text=logic.translet('excetly_withdraw', call.from_user.id), reply_markup=keyboard.excetly_withdraw(call.from_user.id, withdraw, sum))

    elif 'excetly_done' in call.data:
        withdraw = call.data.split(':')[1]
        sum = call.data.split(':')[2]
        print(withdraw, sum)
        logic.send_money(withdraw, sum, call.from_user.id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=logic.translet('money_send', call.from_user.id))

@dp.message_handler(content_types=['text'], state="*")
async def text_message(message: types.Message, state: FSMContext):
    tex = message.text
    if tex == 'Английский':
        row = db.chek_user(message.from_user.id)
        if row[10] == 'ty':
            txt = text.data_text['en']['hello']
            db.updateLange('en', message.from_user.id)
            button = keyboard.main_menu(message.from_user.id)
            await bot.send_message(message.chat.id, text=txt, reply_markup=button)
        else:
            txt = logic.translet('done_change_laung', message.from_user.id)
            db.updateLange('en', message.from_user.id)
            button = keyboard.main_menu(message.from_user.id)
            await bot.send_message(message.chat.id, text=txt, reply_markup=button)
            inline = keyboard.inline_setting(message.from_user.id)
            row = db.chek_user(message.from_user.id)
            txt = logic.translet('menu_settings', message.from_user.id).format(str(message.from_user.id), row[10])
            await bot.send_message(message.chat.id, text=txt, reply_markup=inline)

    elif tex == 'Индийский':
        row = db.chek_user(message.from_user.id)
        if row[10] == 'ty':
            txt = text.data_text['en']['hello']
            db.updateLange('hi', message.from_user.id)
            button = keyboard.main_menu(message.from_user.id)
            await bot.send_message(message.chat.id, text=txt, reply_markup=button)
        else:
            txt = logic.translet('done_change_laung', message.from_user.id)
            db.updateLange('hi', message.from_user.id)
            button = keyboard.main_menu(message.from_user.id)
            await bot.send_message(message.chat.id, text=txt, reply_markup=button)
            inline = keyboard.inline_setting(message.from_user.id)
            row = db.chek_user(message.from_user.id)
            txt = logic.translet('menu_settings', message.from_user.id).format(str(message.from_user.id), row[10])
            await bot.send_message(message.chat.id, text=txt, reply_markup=inline)




    elif tex == text.data_text['en']['main_menu'][0] or tex == text.data_text['hi']['main_menu'][0]:
        txt = logic.translet('my_bank', message.from_user.id)
        row = db.chek_user(message.from_user.id)
        txt = txt.format(row[3], row[2], row[9])
        inline = keyboard.inline_my_bank(message.from_user.id)
        await bot.send_message(message.chat.id, text=txt, reply_markup=inline)

    elif tex == text.data_text['en']['main_menu'][3] or tex == text.data_text['hi']['main_menu'][3]:
        inline = keyboard.inline_setting(message.from_user.id)
        row = db.chek_user(message.from_user.id)
        txt = logic.translet('menu_settings', message.from_user.id).format(str(message.from_user.id), row[10])
        await bot.send_message(message.chat.id, text=txt, reply_markup=inline)

    elif tex == text.data_text['en']['main_menu'][2] or tex == text.data_text['hi']['main_menu'][2]:
        inline = keyboard.inline_about_us(message.from_user.id)
        txt = logic.translet('about_us', message.from_user.id)
        await bot.send_message(message.chat.id, text=txt, reply_markup=inline)

    elif tex == text.data_text['en']['main_menu'][1] or tex == text.data_text['hi']['main_menu'][1]:
        msg = await bot.send_message(message.chat.id, text=logic.translet('pls_wait', message.chat.id))
        inline = keyboard.btn_my_referals(message.from_user.id)
        all_len, not_pay, all_sum_invest, first_invest, not_first_all = logic.all_info_invest(message.from_user.id)
        txt = logic.translet('my_invate', message.from_user.id).format(all_len, not_pay, all_sum_invest, first_invest, not_first_all, str(message.chat.id))
        await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
        await bot.send_message(message.chat.id, text=txt, reply_markup=inline)



async def interest_accrual():
    await logic.log_interest_accrual()
    await logic.send_today_all_proc(bot)
    config.Static.day_work += 1
    if config.Static.day_work % 7 == 0:
        config.Static.week = 0
    config.Static.today = 0
    await asyncio.sleep(24*60*60)


async def send_spam_sms(text):
    row = db.chek_all_user()
    for i in row:
        await bot.send_message(i[0], text=text)
    for i in config.admin_id:
        await bot.send_message(i, text='Рассылка завершенна')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(interest_accrual())
    executor.start_polling(dp)
