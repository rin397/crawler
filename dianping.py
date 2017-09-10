# -*- coding: utf-8 -*-

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from codecs import BOM_UTF8

 
 
def init_driver(time):
    driver = webdriver.Chrome()
    driver.wait = WebDriverWait(driver, time)
    return driver
 
 
def lookup(driver, query):
    try:
        driver.execute_script("window.scrollBy(0, 150);")
    	driver.find_element_by_xpath(query).click()
        html_source = driver.page_source
    	print 'done..',query
    except TimeoutException:
        print("Box or Button not found in google.com")

def loop_shop_item(driver):
    shop_list = driver.find_element_by_id('shop-all-list')
    
    items = shop_list.find_elements_by_css_selector('li')
    for item in items:
        
        pic_ele = item.find_element_by_class_name('pic')
        pic = pic_ele.find_element_by_tag_name('img').get_attribute("src")


        txt_ele = item.find_element_by_class_name('txt')
        tit_ele = txt_ele.find_element_by_class_name('tit')
        shop_infos = tit_ele.find_elements_by_css_selector('a')
        shop_name = shop_infos[0].get_attribute("title")
        shop_href = shop_infos[0].get_attribute("href")
        

        comment_1_ele = txt_ele.find_element_by_class_name('comment')
        rank_stars = comment_1_ele.find_element_by_css_selector('span')
        ranK_start_css = rank_stars.get_attribute("class")
        rank_start_title = rank_stars.get_attribute("title")
        
        try:
            comment_2_ele = txt_ele.find_element_by_class_name('comment-list')
            comment_2_categorys = comment_2_ele.find_elements_by_css_selector('span')
            falvor = comment_2_categorys[0].find_element_by_css_selector('b').get_attribute('innerHTML')
            eviroments = comment_2_categorys[1].find_element_by_css_selector('b').get_attribute('innerHTML')
            service = comment_2_categorys[2].find_element_by_css_selector('b').get_attribute('innerHTML')
        except NoSuchElementException:
            falvor = 0
            eviroments = 0
            service = 0

        addr_ele = txt_ele.find_element_by_class_name('tag-addr')
        tags = addr_ele.find_elements_by_css_selector('a')
        shop_type = tags[0].find_element_by_css_selector('span').get_attribute('innerHTML')
        location = tags[1].find_element_by_css_selector('span').get_attribute('innerHTML')
        addr = addr_ele.find_element_by_class_name('addr').get_attribute('innerHTML')

        try:
            review_num_item = comment_1_ele.find_element_by_class_name('review-num')
            review_href = review_num_item.get_attribute("href")
            review_num = review_num_item.find_element_by_css_selector('b').get_attribute('innerHTML')
        except NoSuchElementException:
            review_href = shop_href+'#comment'
            review_num = 0
        
        try:
            mean_price_item = comment_1_ele.find_element_by_class_name('mean-price')
            mean_price = mean_price_item.find_element_by_css_selector('b').get_attribute('innerHTML')
        except NoSuchElementException:
            mean_price = 0
        
        # 店家图党
        print pic
        # 店名
        print shop_name
        # ID
        print shop_href
        # 星星数
        print ranK_start_css
        # 星等
        print rank_start_title
        # 评论 连结
        print review_href
        # 评论数
        print review_num
         # flavor
        print falvor
        # eviroments
        print eviroments
        # service
        print service
        # shop_type
        print shop_type
        # location
        print location
        # addr
        print addr
        # addr
        print mean_price

def parse_process(driver):
    loop_shop_item(driver)
    print driver.current_url+'-----'

    page_component = driver.find_element_by_class_name('page')
    page_items = page_component.find_elements_by_class_name('PageLink')
    try:
        for page in page_items:
            print page,'...'
            page_driver = init_driver(10)

            href = page.get_attribute("href")
            print href,'...'
            page_driver.get(href)
            loop_shop_item(page_driver)
            page_driver.close()
    except NoSuchElementException:
        print 'finish...'

 
def init_dianping():
    if __name__ == "__main__":
        driver = init_driver(5)
        driver.get("http://www.dianping.com/search/category/1/10/r801")
        #lookup(driver, '//a[@alt="陆家嘴"]')
        #time.sleep(5)
        # wait to make sure there are two windows open
        #WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) == 2)
        #print 'switch_to_window..'
        # switch windows
        #driver.switch_to_window(driver.window_handles[1])
        #lookup(driver,'//a[@href="/search/category/1/10/r842"]')
        #time.sleep(5)
        parse_process(driver)

def init_store():
    if __name__ == "__main__":
        driver = init_driver(5)
        print '1'
        driver.get("http://www.dianping.com/shop/3144349")
        print '2'
        tel_item = driver.find_element_by_xpath("//*[@class='expand-info tel']")
        print tel_item.find_element_by_class_name('item').get_attribute('innerHTML')
        recommend_names = driver.find_element_by_xpath("//*[@class='shop-tab-recommend J-panel']")
        recommend_items = recommend_names.find_element_by_class_name('recommend-name').find_elements_by_class_name('item')
        recommend_photos = recommend_names.find_element_by_xpath("//*[@class='recommend-photo clearfix']").find_elements_by_class_name('item')
        recommend_dishes = {}
        for item in recommend_items:
            values = {}
            values['name'] = item.get_attribute("title")
            values['count'] = item.find_element_by_css_selector('em').get_attribute('innerHTML')
            recommend_dishes[item.get_attribute("title")] = values

        for item in recommend_photos:
            img_item = item.find_element_by_css_selector('img')
            key_item = img_item.get_attribute("alt")
            if recommend_dishes.has_key(key_item): 
                values = recommend_dishes[key_item]
                values['pic'] = img_item.get_attribute("src")
                #values['price'] = item.find_element_by_class_name('price').get_attribute('innerHTML')

        comment_component = driver.find_element_by_xpath("//*[@class='comment-condition J-comment-condition Fix']")
        
        for comment_item in comment_component.find_elements_by_xpath("//*[@class='good J-summary']"):
            tag_value = comment_item.find_element_by_css_selector('a').get_attribute('innerHTML')
            values = tag_value.split('(')
            tag = values[0]
            count = values[1][0:-1]
            print values, count

def rertival_comment():
        driver = init_driver(5)
        driver.get("http://www.dianping.com/shop/17225622/review_more")
        # comment-start
        # dd[1] : five-start
        # dd[2] : four-start        
        # dd[3] : three-start
        # dd[4] : two-start
        # dd[5] : one-start                
        store_each_star_items = driver.find_element_by_class_name("comment-star").find_elements_by_css_selector('dd')
        store_each_stars = {}
        for item in store_each_star_items:
              key = item.find_element_by_css_selector('a').get_attribute('href').split('/')[-1]
              count = item.find_element_by_css_selector('em').get_attribute('innerHTML')[2:-2]
              store_each_stars[key] = count
        print store_each_stars

        # loop each comment
        # retrival  
        # comment_person , falvor , eviroments  , service , comment , favorite_dish , create_date
        comment_list = driver.find_element_by_class_name("comment-list").find_elements_by_css_selector('li')
        comment_items = {}
        
        for comment in comment_list:
            comment_id =  comment.get_attribute('data-id')
            if not comment_id is None:
                #print comment_id
                comment_item = {}
                comment_items[comment_id] = comment_item
                person_item = comment.find_element_by_class_name('pic').find_element_by_class_name('name').find_element_by_css_selector('a')
                comment_item['name'] = person_item.get_attribute('innerHTML')
                comment_item['name_id'] = person_item.get_attribute('href').split('/')[-1]
                # comment start
                comment_start_item = comment.find_element_by_class_name('user-info')
                comment_start = comment_start_item.find_element_by_class_name('item-rank-rst').get_attribute('class').split()[-1]
                comment_item['comment_start'] = comment_start[-2:-1]
                comment_rsts = comment_start_item.find_element_by_class_name('comment-rst').find_elements_by_css_selector('span')
                comment_item['falvor'] = comment_rsts[0].text.split('(')[0][-1]
                comment_item['eviroments'] = comment_rsts[1].text.split('(')[0][-1]
                comment_item['service'] = comment_rsts[2].text.split('(')[0][-1]
                 
                comment_item['comment'] = comment.find_element_by_class_name('J_brief-cont').get_attribute('innerHTML')
                comment_item['create_date'] = comment.find_element_by_class_name('time').get_attribute('innerHTML')
                print comment_item['comment']            

if __name__ == "__main__":
    init_dianping()
        





