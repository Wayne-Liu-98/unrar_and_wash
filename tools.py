# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 17:19:40 2020

@author: user
"""
import pandas as pd




def get_file_days_between(start_date, end_date, date_file="/dat/all/Equity/Wind/Daily/list/tradedays.csv"):
    trade_days = pd.Series(pd.read_csv(date_file, header=None, dtype={0:str})[0])
    return trade_days.loc[(trade_days >= start_date) & (trade_days <= end_date)]


def is_trade_day(datenum):
    date_file = "/dat/all/Future/WIND/list/tradedays.csv"
    trade_days = pd.Series(pd.read_csv(date_file, header=None, dtype={0:str})[0])
    return datenum in set(trade_days.loc[(trade_days >= datenum)])