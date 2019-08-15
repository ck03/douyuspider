from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import json


class DouyuSpider:
    def __init__(self):
        chrome_options = Options()
        # 沒有這一行會自動開啟瀏覽器
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=r'D:\Study\Python2\chromedriver\chromedriver.exe')
        self.statr_url = "https://www.douyu.com/directory/all"
        self.result_list = []
        self.domainname = "https://www.douyu.com"

    def get_content_list(self):
        wait = WebDriverWait(self.driver, 2)
        # # VIP，内容加载完成后爬取
        wait.until(
            lambda driver: self.driver.find_elements_by_xpath(
                "//section[@class='layout-Module js-ListContent']//ul[@class='layout-Cover-list']/li"))

        li_list = self.driver.find_elements_by_xpath("//section[@class='layout-Module js-ListContent']//ul[@class='layout-Cover-list']/li")
        print(len(li_list))
        x = len(li_list) / 5
        print("x=%d" % x)
        for i in range(int(x)):
            wait = WebDriverWait(self.driver, 7)
            # # VIP，内容加载完成后爬取
            wait.until(
                lambda driver: self.driver.find_elements_by_xpath(
                    "//section[@class='layout-Module js-ListContent']//ul[@class='layout-Cover-list']/li"))

            c = 5 * (i+1)
            # print("c=%d" % c)
            li_list = self.driver.find_elements_by_xpath("//section[@class='layout-Module js-ListContent']//ul[@class='layout-Cover-list']/li[{}]".format(c))
            self.driver.execute_script('arguments[0].scrollIntoView();', li_list[-1])  # 拖动到可见的元素去
            time.sleep(3)
            # x = self.driver.find_element_by_xpath(
            #     "//section[@class='layout-Module js-ListContent']//ul[@class='layout-Cover-list']/li/div[@class='DyListCover HeaderCell is-href']/a[1]").get_attribute("href")
            # print("x=%s" % x)
            # print(len(li_list))

        print("第一次讀取資料中....")

        # 仍然會有些元素沒有加載到,所以把沒有加載到的元素個別記錄下來
        img_null_index = []
        li_list = self.driver.find_elements_by_xpath("//section[@class='layout-Module js-ListContent']//ul[@class='layout-Cover-list']/li")
        for index, li in enumerate(li_list):
            item = {}
            x = li.find_elements_by_xpath(".//div[@class='LazyLoad is-visible DyImg DyListCover-pic']/img")
            # print(len(x))
            if len(x) == 0:
                img_null_index.append(index)

        if len(img_null_index) > 0:
            print("記錄未讀取到的資料...")
            count = 1
            # 再次移動到沒有讀取到的元素上
            while True:
                next = False
                for i in img_null_index:
                    li_list = self.driver.find_elements_by_xpath(
                        "//section[@class='layout-Module js-ListContent']//ul[@class='layout-Cover-list']/li[{}]".format(i))
                    self.driver.execute_script('arguments[0].scrollIntoView();', li_list[-1])  # 拖动到可见的元素去
                    time.sleep(2)
                    x = self.driver.find_elements_by_xpath("//section[@class='layout-Module js-ListContent']//ul[@class='layout-Cover-list']/li[{}]//div[@class='LazyLoad is-visible DyImg DyListCover-pic']/img".format(i))
                    # print("*"*50)
                    # print("i=%d" % i)
                    # print(len(x))
                    # 仍然讀不到,再讀
                    if len(x) == 0:
                        next = False
                        count += 1
                        break
                    else:
                        next = True

                if count == 5:
                    break  # 不讀了放棄,以免無窮迴圈

                if next is True:
                    break

        print("再次讀資料中....")

        # 全部讀到.再次串資料
        li_list = self.driver.find_elements_by_xpath(
            "//section[@class='layout-Module js-ListContent']//ul[@class='layout-Cover-list']/li")
        for index, li in enumerate(li_list):
            item = {}
            item["url"] = li.find_element_by_xpath("./div[@class='DyListCover HeaderCell is-href']/a[1]").get_attribute("href")
            item["img"] = li.find_element_by_xpath(".//div[@class='LazyLoad is-visible DyImg DyListCover-pic']/img").get_attribute("src")
            item["title"] = li.find_element_by_xpath(
                ".//div[@class='DyListCover-content']/div[@class='DyListCover-info'][1]/h3").text
            item["zone"] = li.find_element_by_xpath(".//div[@class='DyListCover-content']/div[@class='DyListCover-info'][1]/span").text
            item["user"] = li.find_element_by_xpath(".//div[@class='DyListCover-content']/div[@class='DyListCover-info'][2]/h2").text
            item["hot"] = li.find_element_by_xpath(
                ".//div[@class='DyListCover-content']/div[@class='DyListCover-info'][2]/span").text
            self.result_list.append(item)
        print(self.result_list)
        next_url = self.driver.find_elements_by_xpath("//li[@class=' dy-Pagination-next']")
        next_url = next_url[0] if len(next_url) > 0 else None
        return next_url

    def run(self):  # 主要實現邏輯
        # 1. start_url
        # 2. 發送請求,獲取響應
        self.driver.get(self.statr_url)
        # 3. 提取數據,提取下一頁按鈕
        next_url = self.get_content_list()
        # 4. 保存數據
        # 5. 點擊下一頁元素,循環
        print(next_url)
        while next_url is not None:
            next_url.click()
            next_url = self.get_content_list()


if __name__ == "__main__":
    douyuspider = DouyuSpider()
    douyuspider.run()