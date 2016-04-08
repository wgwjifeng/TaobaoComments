# -*- coding: utf-8 -*-
from pyquery import PyQuery as pq
from selenium.common.exceptions import TimeoutException
from twisted.python.win32 import WindowsError
import config
import time
import socket
import urllib2
from lib.newdriver import new_proxy_driver, new_driver


def get_product(url, fail_time=0):
    try:
        #time.sleep(0.5)
        driver = config.DRIVER
        driver.get(url)
        html = driver.page_source
        doc = pq(html)
        title = doc('title').text()
        return title
    except TimeoutException:
        if fail_time <= 3:
            print u'请求超时, 正在切换会话, 继续重试'
            new_driver()
        else:
            print u'请求超时, 正在切换代理, 继续重试'
            new_proxy_driver()
        fail_time = fail_time + 1
        if config.CONSOLE_OUTPUT:
            print u'当前失败次数', fail_time
        if fail_time == config.MAX_FAIL:
            if config.CONSOLE_OUTPUT:
                print u'失败次数过多, 跳过此请求'
            return False
        get_product(url, fail_time)
    except (socket.error, urllib2.URLError):
        print u'请求宝贝过于频繁, 请求被中断, 正在切换会话重试'
        new_driver()
        fail_time = fail_time + 1
        if config.CONSOLE_OUTPUT:
            print u'当前失败次数', fail_time
        if fail_time == config.MAX_FAIL:
            if config.CONSOLE_OUTPUT:
                print u'失败次数过多, 跳过此请求'
            return False
        get_product(url, fail_time)
    except (WindowsError, OSError, Exception):
        print u'未知错误, 跳过继续运行'
