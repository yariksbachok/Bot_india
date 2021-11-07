import sqlite3
import config

class DBConnection:
    def __init__(self):
        self.conn = sqlite3.connect(f'{config.DIR}database.db', check_same_thread=False)
        self.c = self.conn.cursor()

    def create_tables(self):
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS USER (id INT, address_wallet TEXT, balance_invest INT, balance INT, first_referal INT,  second_referal INT, three_referal INT, four_referal INT, five_referal INT, progres INT, laung TEXT, address_btc TEXT, address_eth TEXT, id_user INTEGER PRIMARY KEY)")
        self.c.execute(
            "CREATE TABLE IF NOT EXISTS HISTORY (id INT, payments TEXT, sum INT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS today_proc (id INT, all_sum INT)")

    def add_USER(self, id, address_BTC, balance_invest, balance, first_referal, second_referal, three_referal, four_referal, five_referal, progres, laung, address_btc, address_eth):
        self.c.execute(
            'INSERT INTO USER(id, address_wallet, balance_invest, balance, first_referal, second_referal, three_referal, four_referal, five_referal, progres, laung, address_btc, address_eth) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (id, address_BTC, balance_invest, balance, first_referal, second_referal, three_referal, four_referal, five_referal, progres, laung, address_btc, address_eth)
        )
        self.conn.commit()

    def add_history(self, id, payments, sum):
        self.c.execute(
            'INSERT INTO HISTORY(id, payments, sum) VALUES (?, ?, ?)',
            (id, payments, sum)
        )
        self.conn.commit()

    def add_today_proc(self, id, sum):
        self.c.execute(
            'INSERT INTO today_proc(id, sum) VALUES (?, ?)',
            (id, sum)
        )
        self.conn.commit()

    def chek_today_proc(self, id):
        return self.c.execute(f"SELECT * FROM today_proc WHERE id='{id}'").fetchone()

    def chek_today_all_proc(self):
        return self.c.execute(f"SELECT * FROM today_proc").fetchall()

    def chek_history(self, id):
        return self.c.execute(f"SELECT * FROM HISTORY WHERE id='{id}'").fetchall()

    def chek_first_referal(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE first_referal='{id}'").fetchall()

    def chek_second_referal(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE second_referal='{id}'").fetchall()

    def chek_three_referall(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE three_referal='{id}'").fetchall()

    def chek_four_referal(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE four_referal='{id}'").fetchall()

    def chek_five_referal(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE five_referal='{id}'").fetchall()

    def chek_first_referal_not_pay(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE first_referal='{id}' and balance_invest=0").fetchall()

    def chek_second_referal_not_pay(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE second_referal='{id}' and balance_invest=0").fetchall()

    def chek_three_referall_not_pay(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE three_referal='{id}' and balance_invest=0").fetchall()

    def chek_four_referal_not_pay(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE four_referal='{id}' and balance_invest=0").fetchall()

    def chek_five_referal_not_pay(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE five_referal='{id}' and balance_invest=0").fetchall()

    def updateBtc(self, address, id):
        self.c.execute(f'UPDATE USER SET address_btc=(?) WHERE id = (?)', [address, id])
        self.conn.commit()

    def updateEth(self, address, id):
        self.c.execute(f'UPDATE USER SET address_eth=(?) WHERE id = (?)', [address, id])
        self.conn.commit()

    def chek_user(self, id):
        return self.c.execute(f"SELECT * FROM USER WHERE id='{id}'").fetchone()

    def chek_all_user(self):
        return self.c.execute(f"SELECT * FROM USER").fetchall()

    def updateWallet(self, wallet, id):
        self.c.execute(f'UPDATE USER SET address_wallet=(?) WHERE id = (?)', [wallet, id])
        self.conn.commit()

    def updateLange(self, lang, id):
        self.c.execute(f'UPDATE USER SET laung=(?) WHERE id = (?)', [lang, id])
        self.conn.commit()

    def updateProgres(self, progres, id):
        self.c.execute(f'UPDATE USER SET progres=(?) WHERE id = (?)', [progres, id])
        self.conn.commit()

    def updateBalanceUser(self, balance, id):
        self.c.execute(f'UPDATE USER SET balance=(?) WHERE id = (?)', [balance, id])
        self.conn.commit()

    def updateInvestUser(self, invest, id):
        self.c.execute(f'UPDATE USER SET balance_invest=(?) WHERE id = (?)', [invest, id])
        self.conn.commit()

    def updateFirstReferal(self, referal_id, id):
        self.c.execute(f'UPDATE USER SET first_referal=(?) WHERE id = (?)', [referal_id, id])
        self.conn.commit()

    def updateSecondReferal(self, referal_id, id):
        self.c.execute(f'UPDATE USER SET second_referal=(?) WHERE id = (?)', [referal_id, id])
        self.conn.commit()

    def updateThreeReferal(self, referal_id, id):
        self.c.execute(f'UPDATE USER SET three_referal=(?) WHERE id = (?)', [referal_id, id])
        self.conn.commit()

    def updateFourReferal(self, referal_id, id):
        self.c.execute(f'UPDATE USER SET four_referal=(?) WHERE id = (?)', [referal_id, id])
        self.conn.commit()

    def updateFiveReferal(self, referal_id, id):
        self.c.execute(f'UPDATE USER SET five_referal=(?) WHERE id = (?)', [referal_id, id])
        self.conn.commit()

    def __del__(self):
        self.c.close()
        self.conn.close()