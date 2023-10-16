# import schedule
# import time
#
#
# def job():
#     print("I'm working...")
#
#
# schedule.every(1).second.at("14:21").do(job)
#
#
# schedule.run_pending()

def score(cf, *scores):
    for i in scores:
        print(i)
        print(cf * i)

cf = 0.2
scores = [4, 5, 4]

score(cf, *scores)