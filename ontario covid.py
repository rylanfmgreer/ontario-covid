

import urllib.request as u
import pandas
import numpy as np
import math

url = 'https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv'

fileobj = u.urlopen(url)
d = pandas.read_csv(fileobj)

total = d["Total Cases"]
totala = np.nan_to_num(np.array(total), 0)

active = total - d["Resolved"] - d["Deaths"]

tests = np.nan_to_num(np.array(d["Total tests completed in the last day"]), 0)
testsa = np.nan_to_num(np.array(tests), 0)

dtotal = totala[1:] - totala[:-1]
dtests = testsa[1:]
prd = dtotal/dtests

def n_f_apply(df, n, f):

    l = []
    for i in range(1, n):
        l.append(np.nan)
    for i in range(n, len(df) + 1):
        s = f(df[(i - n):i])
        l.append(s)

    new_data = pandas.DataFrame(l)
    return new_data

def ndiff(df):
    n = len(df)
    y = float(df[(n- 1):(n)])
    x = float(df[0:1])

    return float(y - x)

def rdiff(df):
    n = len(df)
    y = float(df[(n- 1):(n)])
    x = float(df[0:1])

    return float(math.log(y) - math.log(x))

def n_day_ma(df, n):
    l = []
    for i in range(1, n):
        l.append(np.nan)
    for i in range(n, len(df) + 1):
        s = df[(i - n):i].sum()
        l.append(float(s/n))

    title = str(n) + "-value moving average of " + df.name
    new_data = pandas.DataFrame(l, columns=[title])
    return new_data


if __name__ == "__main__":

    total = d["Total Cases"]

    new = n_f_apply(total, 2, ndiff)
    new.name = "New Cases"

    new_ma = n_day_ma(new, 7)
    new_ma.name = "Seven Day MA of new cases"

    new_rate_chg = n_f_apply(total, 2, rdiff)
    new_rate_chg.name = "Growth rates"

    actv_rate_chg = n_f_apply(active, 2, rdiff)
    actv_rate_chg.name = "active change rates"

    actv_avg = n_day_ma(actv_rate_chg, 7)

    dtc = int((math.log(100/active[len(active) - 1]) / actv_avg[(len(actv_avg) - 1):len(actv_avg)]).to_numpy())

    s5 = "Days til 100 active cases: " + str(dtc)
    print(s5)


    active.name = "Active Cases"

    length = len(total)


    s1 = "New Cases: " + str(total[length - 1] - total[length - 2])
    s3 = "Active Cases: " + str(active[length - 1])
    s2 = "Change in active cases: " + str(active[length - 1] - active[length - 2])
    s4 = "Positive rate: "
    print(s1)
    print(s3)
    print(s2)
    d = d.transpose()
    d = np.nan_to_num(d, 0)


