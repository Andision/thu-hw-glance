__author__ = "Trinkle23897"
__copyright__ = "Copyright (C) 2019 Trinkle23897"
__license__ = "MIT"

import urllib,time,json,operator
import urllib.request, http.cookiejar


#https://learn.tsinghua.edu.cn/b/kc/v_wlkc_xk_sjddb/detail?id=2019-2020-2140258587

url = 'https://learn.tsinghua.edu.cn'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
cookie = http.cookiejar.MozillaCookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)

def open_page(uri, values={}):
    post_data = urllib.parse.urlencode(values).encode() if values else None
    request = urllib.request.Request(uri if uri.startswith('http') else url + uri, post_data, headers)
    try:
        response = opener.open(request)
        return response
    except urllib.error.URLError as e:
        print(uri, e.code, ':', e.reason)

def get_page(uri, values={}):
    data = open_page(uri, values)
    if data:
        return data.read().decode()

def login(username, password):
    login_uri = 'https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/bb5df85216504820be7bba2b0ae1535b/0?/login.do'
    #login_uri = 'https://info.tsinghua.edu.cn/Login'
    values = {'i_user': username, 'i_pass': password, 'atOnce': 'true'}
    #values = {'redirect': 'NO','userName': '2018011319','password': 'jyZhang_629','x': '25','y': '10'}
    info = get_page(login_uri, values)
    successful = 'SUCCESS' in info
    # print('User %s login successfully' % (username) if successful else 'User %s login failed!' % (username))
    if successful:

        get_page(get_page(info.split('replace("')[-1].split('");\n')[0]).split('location="')[1].split('";\r\n')[0])
    return successful

def get_json(uri, values={}):
    for i in range(10):
        try:
            page = get_page(uri, values)
            result = json.loads(page)
            return result
        except json.JSONDecodeError:
            print('\rJSON Decode Error, reconnecting (%d) ...' % (i + 1), end='')
            time.sleep(5)
    return {}




def get_wjhw(uname,upswd):
    username = uname
    password = upswd

    my_login = login(username, password)

    #cookie.load('cookies.txt', ignore_discard=True, ignore_expires=True)

    # data = {'aoData': [{"name": "wlkcid", "value": '2019-2020-2140259619'}]}
    # for hwtype in ['zyListWj', 'zyListYjwg', 'zyListYpg']:
    #     try:
    #         print(get_json('/b/wlxt/kczy/zy/student/%s' % hwtype, data))
    #     except:
    #         continue
    # print(get_page('https://learn.tsinghua.edu.cn/f/wlxt/calendar/student/view'))
    now = get_json('/b/kc/zhjw_v_code_xnxq/getCurrentAndNextSemester')['result']['xnxq']
    #print(now)
    course_all=get_json('/b/wlxt/kc/v_wlkc_xs_xkb_kcb_extend/student/loadCourseBySemesterId/' + now)['resultList']

    # print(type(course_all))
    hws_wj = []
    hwtype="zyListWj"
    for i in course_all:
        # print(i['kcm'])
        data = {'aoData': [{"name": "wlkcid", "value": i['wlkcid']}]}
        hw_list=get_json('/b/wlxt/kczy/zy/student/%s' % hwtype, data)['object']['aaData']

        for j in hw_list:
            tj=j
            tj['kcm']=i['kcm']
            hws_wj.append(tj)

    hws_wj=sorted(hws_wj,key=operator.itemgetter('jzsj'))

    return_list=[]

    now_time=int(time.time()*1000)
    for i in hws_wj:
        # if i['jzsj']<now_time:
        #     continue

        # print(i)
        # print()
        return_list.append([i['bt'],i['jzsjStr'],i['kcm']])

    # print(return_list)

    return return_list
    # print('----------------------------------------------------------------------')
    # print(get_page('https://zhjw.cic.tsinghua.edu.cn/jxmh_out.do?m=bks_jxrl_all&p_start_date=20200301&p_end_date=20200401&sjtzb=true&jsoncallback=no_such_method2&_=1593958368080'))
    # print(cookie)
        # if args.login:
        #     courses = get_courses(args)
        #     for c in courses:
        #         c['_type'] = {'0': 'teacher', '3': 'student'}[c['jslx']]
        #         print('Sync ' + c['xnxq'] + ' ' + c['kcm'])
        #         if not os.path.exists(c['kcm']): os.makedirs(c['kcm'])
        #         sync_info(c)
        #         sync_discuss(c)
        #         sync_notify(c)
        #         sync_file(c)
        #         sync_hw(c)
