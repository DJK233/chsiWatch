import urllib.request
import json
import requests
import time
import jsonpath

api = "https://sctapi.ftqq.com/SCT7313TVj2zEdoINtSaZJZ8e9uRsWFs.send"
title = "研招网光学类调剂有更新啦"
result = "前往研招网查看https://yz.chsi.com.cn/sytj/tj/qecx.html"


def find_school(start, zymc):
    headers = {
        "Host": "yz.chsi.com.cn",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Length": "125",
        "Origin": "https://yz.chsi.com.cn",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://yz.chsi.com.cn/sytj/tj/qecx.html",
        "Cookie": "JSESSIONID=EDC26EA644AE7EB09AF2138F8B3DA4A4; aliyungf_tc=a4613f8792222b613c149b0c6f76eb16fdab4cf1f0412abd6c0b8cf071e1c9e9; XSRF-CCKTOKEN=b39699eb9a86f7a9e9264de1b4eb1a40; CHSICC_CLIENTFLAGYZ=a557569bf69396e8904625df58ab9510; JSESSIONID=4836F9A6426897A5721FFD937CB48D2B; CHSICC_CLIENTFLAGSYTJ=56bb3864f051cd7d4633effe2f203b1a; acw_tc=2f6fc12916167412117864691eaeaae9c81160a2fccf322fcdd87d2862aa7e; zg_did=%7B%22did%22%3A%20%221786c276c194c9-0704608db47db-33405d63-13c680-1786c276c21164%22%7D; zg_adfb574f9c54457db21741353c3b0aa7=%7B%22sid%22%3A%201616741370748%2C%22updated%22%3A%201616741370764%2C%22info%22%3A%201616722226246%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22yz.chsi.com.cn%22%2C%22landHref%22%3A%20%22https%3A%2F%2Fyz.chsi.com.cn%2F%22%2C%22cuid%22%3A%20%227d5b35c4b65fd895e37f6b4c055f9fed%22%7D; _ga=GA1.3.1793808593.1616722225; _gid=GA1.3.1625249675.1616722225",
    }

    data = {
        "pageSize": "20",
        "start": start,
        "orderBy": "",
        "mhcx": "1",
        "ssdm2": "",
        "xxfs2": "",
        "dwmc2": zymc,
        "data_type": "json",
        "agent_from": "web",
        "pageid": "tj_qe_list",
    }

    url = "	https://yz.chsi.com.cn/sytj/stu/sytjqexxcx.action"
    resp = requests.post(url, headers=headers, data=data)
    # 学校列表
    school_list = json.loads(resp.text)["data"]["vo_list"]["vos"]
    return school_list

all_school_list = []
old_school_list = []
zymc_list = ["光学"]

new_school = ""
old_school = ""
def check():
    global all_school_list
    global old_school_list
    global new_school
    global old_school
    if old_school_list:
        all_school_list = []
        for zymc in zymc_list:
            for i in range(20):
                # 翻页
                start = str(i * 20) if i > 0 else ""
                school_list = find_school(start, zymc)
                all_school_list += school_list
                time.sleep(5)
                if len(school_list) < 20:
                    break
        jsonobj = json.dumps(all_school_list)
        jsonobj = json.loads(jsonobj)
        citylist = jsonpath.jsonpath(jsonobj, "$..dwmc")
        tree = json.dumps(citylist, ensure_ascii=False)
        new_school = tree.replace(", ", "\n\n")
        print(new_school)
        if new_school == old_school:
            print("未发现更新！")
        else:
            print("发现更新")
            data = {"text": title, "desp": new_school}
            req = requests.post(api, data=data)
            old_school = new_school
    else:
        for zymc in zymc_list:
            for i in range(20):  # 每页信息
                # 翻页
                start = str(i * 20) if i > 0 else ""
                school_list = find_school(start, zymc)
                all_school_list += school_list
                time.sleep(5)
                if len(school_list) < 20:
                    break
            old_school_list = all_school_list
            jsonobj = json.dumps(all_school_list)
            jsonobj = json.loads(jsonobj)
            citylist = jsonpath.jsonpath(jsonobj, "$..dwmc")
            tree = json.dumps(citylist, ensure_ascii=False)
            old_school = tree.replace(", ", "\n\n")
            print(old_school)


while True:
    check()
    print("\n休息30秒继续运行！")
    time.sleep(360)
    print("继续工作...")

