import datetime
import sqlite3


class User:
    def __init__(self, address: int, cur: sqlite3.Cursor):
        # переменные хранящие уникальные для пользователя
        self.ADDRESS = address
        self.t0_ch = 1
        self.t0_m = 0
        self.job = None
        self.eda = 0
        self.nedo_eda = 0
        self.cur = cur
        self.job0 = None
        self.job_last = None
        self.flag_sleep = True
        self.work = False

        # функции образующие
        self.create_table()


    def set_time_0(self, job_last, job0, ch=1, m=0):
        self.t0_ch, self.t0_m = ch, m
        self.delete_job(n=1)
        self.job_last = job_last
        self.job0 = job0

    def create_table(self):
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS Stat_{self.ADDRESS}(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE NOT NULL,
                        eda INTEGER NOT NULL,
                        perecus INTEGER NOT NULL)""")

    def data_out_table(self):
        return self.cur.execute(f"SELECT eda, perecus FROM Stat_{self.ADDRESS} ORDER BY id DESC LIMIT 7").fetchall()

    def data_in_table(self):
        self.delete_job()
        self.cur.execute(f"INSERT INTO Stat_{self.ADDRESS}(date, eda, perecus) VALUES(?, ?, ?)",
                         [datetime.datetime.today(), self.eda, self.nedo_eda])

    def set_new_var_job(self, job):
        self.delete_job()
        self.job = job


    def delete_job(self, n=0):
        if n:
            if self.job0 is not None:
                self.job0.remove()
                self.job0 = None

            if self.job_last is not None:
                self.job_last.remove()
                self.job_last = None

        else:
            if self.job is not None:
                self.job.remove()
                self.job = None

    def incr_var(self, n=0):
        if n == 1:
            self.eda += 1
        elif n == 2:
            self.eda, self.nedo_eda = 0, 0
        else:
            self.nedo_eda += 1


# ADDRESS = 605850528
scheduler = None
bot = None
con = None
user_id_work = dict()  # '''class, id, t0_ch, t0_m'''

morning_key = ["Не забудь поесть", "Уже утро. Не забудь о еде", "Чтобы убивать людей, надо зарядиться энергией, покушай по возможности",
               "*напоминаю о еде*", "Перекуси сегодня", "Утро зло, но поесть надо"]

waiting_key = ['Хорошо, засекаю и', 'Здорово!', '*звуки заводящегося таймера*',
               'Постановка на боевое дежурство.', "Хитро улыбнулся,", "Туц-туц-тудуц,"]

nignt_key = ["Добрых снов =)", "Засыпай...", "Тёплых снов", "Спокойной ночи)", "До связи утром)\nДоброй ночи"]
