#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 15:23:00 2020

@author: 19424
"""
import re
import logging
import argparse
import datetime
from pathlib import Path
import pandas as pd
#import modin.pandas as pd
from log import get_my_logger

RENAME_DICT = {'市场代码':'[23]Exg', '合约代码':'[1]Code',
               '时间':'[5]TradingDateTime', '最新':'[6]LastPrice',
               '持仓':'[11]Position', '增仓':'[12]PositionIncrease',
               '成交额':'[8]TurnoverAmount', '成交量':'[7]Volume',
               '开仓':'[9]OpenVolume', '平仓':'[10]CloseVolume',
               '成交类型':'[13]TradeType', '方向':'[14]BuySellDirection',
               '买一价':'[15]AskPrice1', '卖一价':'[16]BidPrice1',
               '买一量':'[17]AskVolume1', '卖一量':'[18]BidVolume1'}

TRANSLATION_DICT = {'多开':'LO', '多平':"LC", '多换':"LE",
                    '空开':"SO", '空平':"SC", '空换':"SE",
                    '双开':"OO", '双平':"CC", '双换':"EE"}

logger = get_my_logger([['info.log', logging.INFO],
                        ['warning.log', logging.WARNING],
                        ['error.log', logging.ERROR]])


def single_file(file):
    df = pd.read_csv(file, encoding='gb2312', converters={'时间':pd.Timestamp})
    if not df.empty:
        df.rename(columns=RENAME_DICT, inplace=True)
        df['[19]Open'] = df['[6]LastPrice'][0]
        df['[20]Low'] = df['[6]LastPrice'].min()
        df['[21]High'] = df['[6]LastPrice'].max()
        df['[2]TradingDate'] = (df['[5]TradingDateTime'].dt
                                .date.apply(lambda x: x.strftime('%Y%m%d')))
        df['[3]TradingTime'] = (df['[5]TradingDateTime'].dt.time
                                .apply(lambda x: x.strftime('%H%M%S%f')).str.slice(0,-3))
        df['[4]TradeDate'] = re.compile('\d{8}').search(file).group()
        df['[22]Multipiler'] = (df['[8]TurnoverAmount']
                                /(df['[6]LastPrice']*df['[7]Volume'])).round(1)
        df['[13]TradeType'] = df['[13]TradeType'].replace(TRANSLATION_DICT)
        df['[23]Exg'] = df['[23]Exg'].str.upper().replace({'ZC':'CZCE',
                                                           'DC':'DCE',
                                                           'SC':'SHFE',
                                                           'SF':'CFFEX'})
        logger.info('{} done'.format(file))
        return df
    else:
        logger.warning('{} is empty!'.format(file))
        return None


def single_date(path, date):
    p = Path(Path().resolve(), path, date)
    try:
        return pd.concat([single_file(str(file)) for file in list(p.iterdir())])
    except FileNotFoundError:
        return None


def inputs_date_list():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str,
        help=("Relative path where all date-named folders are."
              "Usually, this is the name of the origin rar."),
        default=str(datetime.date.today()-datetime.timedelta(days=1)))
    parser.add_argument(
        "--start", "-s", type=str,
        help=("""Starting date, the result would include all days' data 
              between start and end whenever available."""
              "If not given, take one-year-ago by default."),
        default=str(datetime.date.today()-datetime.timedelta(days=365)))
    parser.add_argument(
        "--end", "-e", type=str,
        help=("""Ending date, the result would include all days' data 
              between start and end whenever available"""
              "If not given, take yesterday by default. "),
        default=str(datetime.date.today()-datetime.timedelta(days=1)))
    args = parser.parse_args()
    path = args.path
    start = pd.to_datetime(args.start)
    end = pd.to_datetime(args.end)
    return [path, [x.strftime('%Y%m%d') for x in pd.date_range(start, end)]]


def demo():
    path = inputs_date_list()[0]
    date_list = inputs_date_list()[1]
    try:
        
        df = pd.concat([single_date(path, date) for date in date_list])
        logger.info('DataFrame generated, reordering columns')
        order = ['[1]Code', '[2]TradingDate', '[3]TradingTime', '[4]TradeDate',
                 '[5]TradingDateTime', '[6]LastPrice', '[7]Volume',
                 '[8]TurnoverAmount', '[9]OpenVolume', '[10]CloseVolume',
                 '[11]Position', '[12]PositionIncrease', '[13]TradeType',
                 '[14]BuySellDirection', '[15]AskPrice1', '[16]BidPrice1',
                 '[17]AskVolume1', '[18]BidVolume1', '[19]Open', '[20]Low',
                 '[21]High', '[22]Multipiler', '[23]Exg']
        df = df.reindex(order, axis=1)
        logger.info('Reordered, generating csv')
        df.to_csv('{}_to_{}.csv'.format(date_list[0],date_list[-1]), index=False)
        logger.info('{}_to_{}.csv generated'.format(date_list[0],date_list[-1]))
    except ValueError:
        logger.info('All are empty!')


if __name__=="__main__":
    demo()

    




