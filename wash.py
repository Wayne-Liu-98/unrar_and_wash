#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 15:23:00 2020

@author: 19424
"""
import os
import re
import logging
import argparse
import datetime
from pathlib import Path
import pandas as pd
#import modin.pandas as pd
from log import get_my_logger
from tools import get_file_days_between

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

# logger = get_my_logger([['info.log', logging.INFO],
#                         ['warning.log', logging.WARNING],
#                         ['error.log', logging.ERROR]])


def single_file(file):
    # import pdb; pdb.set_trace()
    if os.path.getsize(file) >= 104:
        logger.info('Working on {}'.format(str(file)))
        df = pd.read_csv(file, encoding='gb2312', converters={'时间':pd.Timestamp})
    else:
        logger.warning('{} is abnormally small in size, doubtably empty.'.format(file))
        return None
        
    if not df.empty:
        # import pdb; pdb.set_trace()
        df.rename(columns=RENAME_DICT, inplace=True)
        df['[1]Code'] = df['[1]Code'].str.upper()
        df['[19]Open'] = df['[6]LastPrice'][0]
        df['[20]Low'] = df['[6]LastPrice'].min()
        df['[21]High'] = df['[6]LastPrice'].max()
        df['[2]TradingDate'] = (df['[5]TradingDateTime'].dt.date.astype(str)
                                .str.replace("-", ""))
        df['[3]TradingTime'] = (df['[5]TradingDateTime'].dt.time.astype(str)
                                .str.extract("([0-9:]+)", expand=False).str.replace(":", "")+"000")
        df['[4]TradeDate'] = re.compile('\d{8}').search(file).group()
        df['[22]Multipiler'] = (df['[8]TurnoverAmount']
                                /(df['[6]LastPrice']*df['[7]Volume'])).round(1)
        df['[13]TradeType'] = df['[13]TradeType'].replace(TRANSLATION_DICT)
        df['[23]Exg'] = df['[23]Exg'].str.upper().replace({'ZC':'CZCE',
                                                           'DC':'DCE',
                                                           'SC':'SHFE',
                                                           'SF':'CFFEX'})
        logger.info('{} done'.format(file))
        # import pdb; pdb.set_trace()
        return df
    else:
        logger.warning('{} is empty!'.format(file))
        # import pdb; pdb.set_trace()
        return None


def single_date(source_path, date):
    p = Path(source_path, date[0:4], date[4:6], date[6:8])
    result = {} 
    # import pdb; pdb.set_trace()
    for file in list(p.glob('*.csv')):
        df = single_file(str(file))
        result.update({str(file): df})
    if result:
        return pd.concat(result.values())
    else:
        logger.warning("No csv found under {}".format(str(p)))
        return None

def inputs_date_list():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source_path", type=str,
        help=("Absolute path where all date-named folders are."
              "Take /dat5/all/L1/Future/JSY/v0.0/data, the source path on server 9, by default"),
        default='/dat5/all/L1/Future/JSY/v0.0/data')
    parser.add_argument(
        "--target_path", "-t", type=str,
        help=("Absolute path where all date-named folders are."
              "Take /dat5/all/L1/Future/JSY/v1.0/data, the target path on server 9, by default"),
        default='/dat5/all/L1/Future/JSY/v1.0/data')
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
              "If not given, take today by default. "),
        default=str(datetime.date.today()-datetime.timedelta(days=1)))
    args = parser.parse_args()
    source_path = args.source_path
    target_path = args.target_path
    start = pd.to_datetime(args.start).strftime('%Y%m%d')
    end = pd.to_datetime(args.end).strftime('%Y%m%d')
    return [source_path, list(get_file_days_between(start, end)), target_path]


def gen_csv(df, target_path, date_list):
    if len(date_list)==1:
        date = date_list[0]
        name = date[0:4]+"-"+date[4:6]+"-"+date[6:8]+".csv"
    else:
        name = '{}_to_{}.csv'.format(date_list[0],date_list[-1])
        date = None
    if date:
        p = Path(target_path, date[0:4], date[4:6], date[6:8])
        if not p.is_dir():
            p.mkdir(mode=0o777, parents=True)
        full_name = str(Path(p, name))
    else:
        full_name = str(Path(target_path, name))
    df.to_csv(full_name, index=False, sep="|", encoding="gb2312")
    logger.info('{} generated'.format(name))


def run():
    # import pdb; pdb.set_trace()
    source_path, date_list, target_path = inputs_date_list()
    if not date_list:
        logger.warning('No trading days between start and end.')
    else:
        logger.info('Generating df for {}'.format(date_list))
        list_df = [single_date(source_path, date) for date in date_list]
        if list_df:
            df = pd.concat(list_df)
            logger.info('DataFrame generated, reordering columns')
        else: 
            logger.error('No data found')
            return None
        order = ['[1]Code', '[2]TradingDate', '[3]TradingTime', '[4]TradeDate',
                 '[5]TradingDateTime', '[6]LastPrice', '[7]Volume',
                 '[8]TurnoverAmount', '[9]OpenVolume', '[10]CloseVolume',
                 '[11]Position', '[12]PositionIncrease', '[13]TradeType',
                 '[14]BuySellDirection', '[15]AskPrice1', '[16]BidPrice1',
                 '[17]AskVolume1', '[18]BidVolume1', '[19]Open', '[20]Low',
                 '[21]High', '[22]Multipiler', '[23]Exg']
        # df = df.reindex(order, axis=1)
        df = df[order]
        logger.info('Reordered, generating csv')
        gen_csv(df, target_path, date_list)


if __name__=="__main__":
    logger = get_my_logger()
    run()