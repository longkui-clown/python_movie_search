#coding=gb18030
import requests
import urllib.request
import re
import threading

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

search_url = 'http://so.hao6v.com/e/search/index.php'

def second_search(tt_res, k, url):
    res = {}
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            decode_resp = resp.content.decode("gb18030", "ignore")
            decode_resp = re.sub('\r\n', '', decode_resp)
            res_1 = re.findall('<tbody>(.*?)</tbody>', decode_resp, re.S)
            for t_res_1 in res_1:
                # ���߹ۿ�
                res_2 = re.findall(r'(���߹ۿ���).*?<a.*?>(.*?)</a>', t_res_1)
                t_res_1 = re.sub(r'���߹ۿ�.*?/td>', '', t_res_1)
                if "online_watch" in res.keys():
                    res["online_watch"] = res["online_watch"] + res_2
                else:
                    res["online_watch"] = res_2
                # ��������
                res_2 = re.findall(r'(�������ӣ�).*?<a.*?href="(.*?)">.*?�룺(\w{4})', t_res_1) 
                t_res_1 = re.sub(r'�������ӣ�.*?�룺\w{4}', '', t_res_1)
                if "baiduyun" in res.keys():
                    res["baiduyun"] = res["baiduyun"] + res_2
                else:
                    res["baiduyun"] = res_2

                # ����
                res_2 = re.findall(r'<a.*?href="(.*?)">(.*?)</a>.*?</td>', t_res_1)
                if "cili" in res.keys():
                    res["cili"] = res["cili"] + res_2
                else:
                    res["cili"] = res_2
    except:
        ""
    
    tt_res[k] = res


def first_search(movie_name):
    res_num = 0
    find_movies = {}
    try:
        req_data = {
            "show": "title,smalltext",
            "tempid": "1",
            "keyboard": movie_name.encode("gb18030"),
            "tbname": "article",
            "x": 35,
            "y": 8
        }
        resp = requests.post(search_url, data=req_data, timeout=5)
        if resp.status_code == 200:
            decode_resp = resp.content.decode("gb18030", "ignore")
            # print(decode_resp)
            decode_resp = re.sub('\r\n', '', decode_resp)
            ttt_res = re.findall('<table width="100%" border="0" align="center" cellpadding="3" cellspacing="1">(.*)</table>', decode_resp)
            for str_table in ttt_res:
                res = re.findall('<span.*?><a href=(.*?) target=_blank>(.*?)</a>', str_table)
                res_num = len(res)
                threads = {}
                for (k, v) in res:
                    n_f_v = re.findall('.*>(.*?)<.*', v)
                    if n_f_v != []:
                        v = n_f_v[0]
                    # find_movies[(k, v)] = second_search(k)
                    t = threading.Thread(target=second_search,args=(find_movies, (k, v), k))
                    t.setDaemon(True)
                    t.start()
                    threads[(k, v)] = t

                for k, v in threads.items():
                    v.join()

        else:
            print("δ�ҵ��õ�Ӱ������ݣ�����")
    except:
        print("error when request������")

    return {
        "num": res_num,
        "res": find_movies
    }


def search_movie(movie_name):
    res = first_search(movie_name)
    print("�����ҵ� " + str(res["num"]) + "�������")
    if res["num"] > 0:
        print(generate_res(res["res"]))

    print("")
    print("-------ok-------\n\n")



def generate_res(find_movies):
    ks = list(find_movies.keys())
    idx = 0
    print('---------------------------------------------------------------------------------------------')
    for (m_url, m_title) in ks:
        print('| %d %s %s |' % (idx + 1, m_title.ljust(45, " "), m_url.ljust(45, " ")))
        idx += 1
    print('---------------------------------------------------------------------------------------------')
    while 1:
        try:
            choose_index = input("\n������ѡ�����ţ�1 - %d��(���� q �˳�)��\n" % (len(ks)))
            if choose_index == 'q':
                print("****�˳�ѡ��****")
                break

            elif (eval(choose_index) <= len(ks)) and (eval(choose_index) > 0):
                print(format_links(ks[eval(choose_index) - 1], find_movies[ks[eval(choose_index) - 1]]))
                print("��ʽ�����")
        except:
            ""


format_order = ['online_watch', 'baiduyun', 'cili']
def format_links(src, links):
    (f_n, f_s_url) = src
    formated = f_n + "    " + f_s_url + '\n'
    for ooo in format_order:
        if ooo in links.keys():
            formated += per_format(ooo, links[ooo]) + '\n'
        else:
            formated += ""
    
    return formated.replace('\n\n', '').strip('\n').strip(' ')


def per_format(type, links):
    res = ""
    for link in links:
        if type == 'cili':
            (ed2k, film_name) = link
            res += film_name + "    " + ed2k + '\n'
        elif type in format_order:
            res += " ".join(link).strip(" ")
        else:
            res += ""
    return res


def main():
    print("------------------��Ӱ��Դ����------------------")

    try:
        while 1:
            movie_name = input("��������ҵĵ�Ӱ����: \n")
            # print(movie_name)
            search_movie(movie_name)
    except:
        print("�˳�����")


if __name__ == "__main__":
    try:
        main()
    except:
        print("�˳�����")    
    # # ����
    # print(second_search("http://www.hao6v.com/dy/2019-01-22/HTJZHSGWG.html"))