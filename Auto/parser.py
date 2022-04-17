import pandas as pd
import requests
from bs4 import BeautifulSoup
from abc import abstractmethod
from datetime import datetime


class Parser(object):
    _headers: dict
    _url: str

    def __init__(self, iv_url):
        self._url = iv_url
        self._headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/100.0.4896.88 Safari/537.36 '
        }

    @abstractmethod
    def CntPages(self):
        pass

    @abstractmethod
    def PasrPage(self, iv_numPage):
        pass

    def SetHeaders(self, io_headers):
        self._headers = io_headers

    def PasrAllPages(self):
        lo_dfFull = pd.DataFrame()
        for lv_i in range(1, self.CntPages() + 1):
            print(lv_i)
            lo_dfPage = self.PasrPage(lv_i)
            lo_dfFull = lo_dfFull.append(lo_dfPage)
        return lo_dfFull


class ParseDrom(Parser):
    _urlParam: str  # параметры поиска (передаются после номера страницы)

    def __init__(self, iv_url, iv_paramUrl=""):
        super().__init__(iv_url)
        self._urlParam = iv_paramUrl

    def CntPages(self):
        with requests.Session() as lo_s:
            lo_r = lo_s.get("{}page{}/{}".format(self._url, 100, self._urlParam), headers=self._headers)
            if lo_r.status_code == 200:
                lo_soup = BeautifulSoup(lo_r.text, "html.parser")

                # ищем кнопку next. Если ее нет - значит мы увидим номер последней страницы.
                # если кнопка есть - вернем 100, т.к. Drom больше 100 страниц не открывает
                lo_btnNext = lo_soup.find("a", attrs={"data-ftid": "component_pagination-item-next"})
                if lo_btnNext is not None:
                    return 100
                else:
                    lo_btnPages = lo_soup.findAll("a", attrs={"data-ftid": "component_pagination-item"})
                    return int(lo_btnPages[len(lo_btnPages) - 1].text)
            else:
                print("Error", lo_r.status_code)
        return 1

    def PasrPage(self, iv_numPage):
        lo_dfPage = pd.DataFrame()
        with requests.Session() as lo_s:
            lo_r = lo_s.get("{}page{}/{}".format(self._url, iv_numPage, self._urlParam), headers=self._headers)
            if lo_r.status_code == 200:
                # with open('xz.html', 'w') as file:
                #     file.write(lo_r.text)
                # lo_r.encoding = 'utf-8'
                lo_soup = BeautifulSoup(lo_r.text, "html.parser")
                lo_allCar = lo_soup.findAll('a', attrs={"data-ftid": "bulls-list_bull"})

                iv_numCar = 0
                for lo_data in lo_allCar:
                    iv_numCar += 1
                    try:
                        lo_dctRow = {}
                        lo_dctRow["URL"] = lo_data['href']
                        lo_divAuto = lo_data.find('span', attrs={"data-ftid": "bull_title"})  # обычный случай
                        # if lo_divAuto is None:
                        #     lo_divAuto = lo_data.find('div', class_='css-r91w5p e3f4v4l2') # случай, если авто продан
                        lo_dctRow["Авто"] = lo_divAuto.text

                        lo_dctRow["Цена"] = lo_data.find('span', attrs={"data-ftid": "bull_price"}).text
                        # dic["Состояние"] = data.find('div', class_='css-citfcw ejipaoe0').text

                        # TODO: если какого-то параметра не будет, все значения уедут. Нужны доп.условия
                        lo_lstDv = lo_data.findAll('span', attrs={"data-ftid": "bull_description-item"})

                        for lv_i in range(len(lo_lstDv)):
                            lv_val = lo_lstDv[lv_i].text.rstrip(",")
                            if lv_val.find(" л") != -1:
                                lo_tmp = lv_val.split("(")
                                if len(lo_tmp) == 2:
                                    lo_dctRow["Объем двигателя"] = lo_tmp[0]
                                    lo_dctRow["Мощность двигателя"] = lo_tmp[1].rstrip(")")
                                else:
                                    if lo_tmp[0].find("л.с.") != -1:
                                        lo_dctRow["Мощность двигателя"] = lo_tmp[0]
                                    else:
                                        lo_dctRow["Объем двигателя"] = lo_tmp[0]

                            elif lv_val in ["бензин", "гибрид", "дизель", "электро"]:
                                lo_dctRow["Топливо"] = lv_val
                            elif lv_val in ["АКПП", "механика", "робот", "вариатор"]:
                                lo_dctRow["КПП"] = lv_val
                            elif lv_val in ["4WD", "задний", "передний"]:
                                lo_dctRow["Привод"] = lv_val

                            elif lv_val.find(' тыс. км') != -1:
                                lo_dctRow["Пробег, тыс. км"] = lv_val[:-8]
                            elif lv_val.find('б/п') != -1:
                                lo_dctRow["Пробег по РФ, тыс. км"] = lv_val

                            else:
                                lo_dctRow["Цвет"] = lv_val

                        lo_dfPage = lo_dfPage.append(lo_dctRow, ignore_index=True)
                    except Exception as lo_ex:
                        print(iv_numPage, ": ", iv_numCar, ": ", lo_ex)
            else:
                print("Error", lo_r.status_code)
        return lo_dfPage


class ParseAuto(Parser):

    def __init__(self, iv_url):
        super().__init__(iv_url)

    def BuildURL(self, iv_numPage):
        if self._url.find("?") != -1:
            return "{}&page={}".format(self._url, iv_numPage)
        else:
            return "{}?page={}".format(self._url, iv_numPage)

    def CntPages(self):
        with requests.Session() as lo_s:
            lo_r = lo_s.get(self.BuildURL(2), headers=self._headers)
            if lo_r.status_code == 200:
                lo_r.encoding = 'utf-8'
                # with open('xz.html', 'w', encoding='utf-8') as file:
                #     file.write(lo_r.text)

                lo_soup = BeautifulSoup(lo_r.text, "html.parser")
                lo_groupPages = lo_soup.find("div", class_="ListingPagination")
                lo_btnPages = lo_groupPages.findAll("a", class_="ListingPagination__page")
                return int(lo_btnPages[-1].text)
            else:
                print("Error", lo_r.status_code)
        return 1

    def PasrPage(self, iv_numPage):
        lo_dfPage = pd.DataFrame()
        with requests.Session() as lo_s:
            lo_r = lo_s.get(self.BuildURL(iv_numPage), headers=self._headers)
            if lo_r.status_code == 200:
                lo_r.encoding = 'utf-8'
                with open('xz.html', 'w', encoding='utf-8') as file:
                    file.write(lo_r.text)
                soup = BeautifulSoup(lo_r.text, "html.parser")
                allcar = soup.findAll('div', class_='ListingItem__main')

                iv_numCar = 0
                for data in allcar:
                    iv_numCar += 1
                    try:
                        dic = {}
                        dic["URL"] = data.find('a', class_='Link ListingItemTitle__link')['href']
                        dic["Марка"] = data.find('a', class_='Link ListingItemTitle__link').text

                        lst_dv = data.findAll('div', class_='ListingItemTechSummaryDesktop__cell')
                        lo_array = lst_dv[0].text.split("/")
                        dic["Топливо"] = lo_array[2]
                        if dic["Топливо"].find("Электро") != -1:
                            dic["Объем двигателя"] = lo_array[1]
                            dic["Мощность двигателя"] = lo_array[0]
                        else:
                            dic["Объем двигателя"] = lo_array[0]
                            dic["Мощность двигателя"] = lo_array[1]

                        for lv_i in range(1, len(lst_dv)):
                            lv_val = lst_dv[lv_i].text
                            if lv_val in ["автомат", "вариатор", "механика", "робот"]:
                                dic["КПП"] = lv_val
                            elif lv_val in ["передний", "полный", "задний"]:
                                dic["Привод"] = lv_val

                        dic["Цена"] = data.find('div', class_='ListingItemPrice__content').text
                        dic["Год выпуска"] = data.find('div', class_='ListingItem__year').text
                        dic["Пробег"] = data.find('div', class_='ListingItem__kmAge').text
                        # print(dic)
                        lo_dfPage = lo_dfPage.append(dic, ignore_index=True)
                    except Exception as lo_ex:
                        print(iv_numPage, ": ", iv_numCar, ": ", lo_ex)

            else:
                print("Error")
        return lo_dfPage
# go_parser = ParseDrom(r"https://auto.drom.ru/toyota/all/")
#
# go_dfCars = go_parser.PasrAllPages()
#
# gv_name = datetime.now().strftime("%Y%m%d-%H%M%S")
# go_dfCars.to_excel("job\\" + gv_name + ".xlsx")
# print(len(go_dfCars))

go_parser = ParseAuto(r"https://auto.ru/cars/all/")
go_parser.SetHeaders({
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Accept-Language' : 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control' : 'max-age=0',
    'Connection' : 'keep-alive',
    'Cookie' : 'gdpr=0; _ym_uid=1650040415881014180; spravka=dD0xNjUwMDQwNDE3O2k9OTUuMzEuMTY0LjIwNDtEPTZCN0IyMzg0QjgxMDhFRDUwQjE2ODJDODM1MEM5MDVCNUNBNzE0RDQxRTQ2MzVBMUU0MDZFN0EzRjUzNkFCMTY1RDdBOTk2Qzt1PTE2NTAwNDA0MTc3MDkwMTAxMjk7aD02ZDA1Zjk0YmM2ZTBlNjYzMGI4YWQxMzRjY2U2YTYyMQ==; _csrf_token=05526f7dc250b81c6ad8a6fe234afedab0f64fd54726108f; suid=beb23d545bdf34b6846c46043cb502d3.27f1dd7bf67e250b0d265b5f6b7e3562; from=direct; yuidlt=1; yandexuid=4560098021572630586; my=YwA%3D; ys=udn.cDp5YWdvbmNoYXJvdmExNTEyMjU%3D%23c_chck.3729760260; autoru_sid=a%3Ag62599e62257ibr3vhsohmp9phq27ook.b87b08f76d8c3e8622bf276898b0f84b%7C1650040418338.604800.pRLucir6kCSl0INJLfO1KA.FZgwNkU425AyH1gkx7Ri7MN6isl4r4YqtH4R-YL579g; autoruuid=g62599e62257ibr3vhsohmp9phq27ook.b87b08f76d8c3e8622bf276898b0f84b; cmtchd=MTY1MDA0MDQyMTk4Mw==; crookie=AMxwNNvnHFBycGTqFyhFX+CbR2dC7trC/w99WUyAeR6OWq2kd3Hzhl+WVpdoaAaJWr4Zbork7Lvll4/6k4+HCIGSLFc=; los=1; bltsr=1; gids=1%2C213; yandex_login=yagoncharova151225; i=WWcVfXvVydauEmguFL5w3EHm4kCn53EOQ1QfIs9zBVdQel0tSu7pUMc7RbO43Iwo8JDzKXp7Z7MwM1Ah/Pm6MNzkZhQ=; _ym_isad=1; mmm-search-accordion-is-open-cars=%5B0%5D; Session_id=3:1650202774.5.3.1631103548565:SmmzWQ:27.1.2:1|563763314.13423332.2.2:13423332|1327063823.118819.2.2:118819|1015261777.1995054.2.2:1995054|844574756.3271684.2.2:3271684|1118691669.13466947.2.2:13466947|61:3798.699210.xCZtcPdBVjzP3190M6uGWQ8Bdq4; mda2_beacon=1650202774412; sso_status=sso.passport.yandex.ru:blocked; _yasc=JEmOf+Nm131Y/gkvY75lLxcqI47UcvrxcJjYGrlrRA6xHvrk; safe_deal_promo=1; autoru-visits-count=1; autoru-visits-session-unexpired=1; from_lifetime=1650207044635; _ym_d=1650207304',
    'Host' : 'auto.ru',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
})

go_dfCars = go_parser.PasrAllPages()

gv_name = datetime.now().strftime("%Y%m%d-%H%M%S")
go_dfCars.to_excel("job\\" + gv_name + ".xlsx")
print(len(go_dfCars))

