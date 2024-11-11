#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tianzhichao
File: stock_price.py
Time: 2024/11/7 16:39
"""
from app.client.base import BaseRequests


class StockMsgCli(BaseRequests):
    def get_stock_company_info(self):
        """
            东方财富网-沪深京 A 股-实时行情
            https://quote.eastmoney.com/center/gridlist.html#hs_a_board
            :return: 实时行情
            :rtype: pandas.DataFrame
        """
        params = {
            "pn": "1",
            "pz": "50000",
            "po": "1",
            "np": "1",
            "ut": "bd1d9ddb04089700cf9c27f6f7426281",
            "fltt": "2",
            "invt": "2",
            "fid": "f3",
            "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
            "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
            "_": "1623833739532",
        }

        res = self.get(params=params)

        return res.json()


stock_cli = StockMsgCli(base_url="http://82.push2.eastmoney.com/api/qt/clist/get", is_retry=True)

if __name__ == '__main__':
    res = stock_cli.get_stock_company_info()
    print(res)
    # xinlang_cli.get_stock_price()