import io
import sys
import urllib.request as req
# from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import pandas as pd
# import pymysql
from fake_useragent import UserAgent
from datetime import datetime, timedelta
from requests.exceptions import HTTPError
import logging

class MysqlController:
    def __init__(self, host, id, pw, db_name):
        self.conn = pymysql.connect(host=host, user=id, password=pw, db=db_name, charset='utf8')
        self.curs = self.conn.cursor()

    def insert_rec_info(self, _list):
        insert_sql = '''
               insert
                   into
                   tbl_rec_rltm_data(trade_day,
                   aver_value)
                   values (%s, %s)
           '''
        self.curs.execute(insert_sql, (_list[0],_list[1]))

class CreateLogger:
    def logger(self, log_name):
        logger = logging.getLogger(log_name)
        if len(logger.handlers) > 0:
            return logger  # Logger already exists
        logger.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_handler = logging.StreamHandler()
        log_handler.setFormatter(formatter)
        logger.addHandler(log_handler)
        file_handler = logging.FileHandler('/apps/kdn/pv/cron_script/log/'+'client_get_rec'+'.log')
        # file_handler = logging.FileHandler('./Log/' + 'client_get_rec' + '.log')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

class GetRec:

    cnt_list = 1
    cnt_normal = 0
    cnt_http_err = 0
    cnt_other_err = 0

    def get_rec(self, url, set_day):
        ua = UserAgent()
        # 헤더 선언
        headers = {
            'User-Agent': ua.ie,
            'referer': 'https://new.kpx.or.kr/main/#section-2nd'
        }

        try:
            url = url
            html = req.urlopen(req.Request(url, headers=headers)).read().decode('utf-8')
            # print('html', html)
            soup = BeautifulSoup(html, 'html.parser')
            aver_html = soup.find("div", attrs={"class":"rec_table"}).find("td", attrs={"data-label":"평균가"})
            # print(aver_html)
            str_aver = aver_html.string.replace(" ", "").replace(",","")
            print(str_aver)
            day_html = soup.find("div", attrs={"class": "rec_table"}).find("td", attrs={"data-label": "거래일"})
            str_day = day_html.string.replace(" ", "")
            print(str_day)

            # table_html = str(table)
            # table_df_list = pd.read_html(table_html)
            # print(table_df_list)
            # print(table_df_list[0])
            # # print(table_df_list[0][1])
            # str_day = table_df_list[0][1][0]
            # print(str_day)
            # str_aver = table_df_list[0][1][2]
            # print(str_aver)
            date_list = [str_day, str_aver]
            mysql_controller.insert_rec_info(date_list)
            mysql_controller.conn.commit()

        except HTTPError as http_err:
            _err = 'Date:' + set_day + '==> HTTP error occurred:' + http_err
            # log = cl.logger('GetRec')
            # log.error(_err)
            self.cnt_http_err = self.cnt_http_err + 1

        except Exception as err:
            _err = 'Date:' + set_day + '==> Other error occurred:' + err
            # log = cl.logger('GetRec')
            # log.error(_err)
            self.cnt_other_err = self.cnt_other_err + 1

        _err_msg = 'Total count:' + str(self.cnt_list) + ', Success count:' + str(
            self.cnt_normal) + ', Http Error count:' + str(self.cnt_http_err) + ', Other Error count:' + str(
            self.cnt_other_err)



    def getRest(self, url):
        set_day = str((datetime.today() + timedelta(days=1)).strftime("%Y%m%d"))
        msg = self.get_rec(url, set_day)
        return msg


mysql_controller = MysqlController('localhost','kdn_pv','kdn_pv123','kdn_pv')
cl = CreateLogger()
log = cl.logger('GetRec')
log.error('Start Log')

getRec = GetRec()
msg = getRec.getRest('https://new.kpx.or.kr/main/#section-2nd')
