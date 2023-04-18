import schedule
import time


def job():
    print("I'm working...")


schedule.every().day.at("14:21").do(job)


schedule.run_pending()
