'''
@author : johnwest
@github : https://github.com/JohnWes7/Daily_Nutrition
config类因为没有get;所以全部包装成方法防止被修改好了
'''
import configparser
import json
import os
from urllib import request


class path:
    # 直接通过属性名调用 不可更改
    # 文件路径
    # cookie_path = os.path.dirname(__file__) + '/data/cookies.json'
    # ajax_discovery_data_path = os.path.dirname(__file__) +
    # '/data/wwwpixivnet_ajax_discovery_artworks.json'
    # download_record_path = os.path.dirname(__file__) +
    # '/data/downloadrecord.json'
    # performance_log_path = os.path.dirname(__file__) +
    # '/data/performance.json'
    # bookmarkdata_path = os.path.dirname(__file__) + '/data/bookmarkdata.json'
    # # 驱动位置
    # chromedriver_exe_path = os.path.dirname(__file__) + '/chromedriver.exe'
    # geckodriver_exe_path = os.path.dirname(__file__) +
    # '/driver/geckodriver.exe'
    # edgedriver_exe_path = os.path.dirname(__file__) + '/msedgedriver.exe'
    # # 文件夹路径
    # data_dir = datadir
    # data_temp_dir = data_dir + 'temp/'

    # 文件路径
    @staticmethod
    def get_cookie_path():
        '''cookie文件路径'''
        return f'{os.path.dirname(__file__)}/data/cookies.json'

    @staticmethod
    def get_ajax_discovery_data_path():
        '''向推荐页面请求的推荐数据保存路径'''
        return os.path.dirname(
            __file__) + '/data/wwwpixivnet_ajax_discovery_artworks.json'

    @staticmethod
    def get_download_record_path():
        '''下载过的图的记录数据路径'''
        return f'{os.path.dirname(__file__)}/data/downloadrecord.json'

    @staticmethod
    def get_performance_log_path():
        '''浏览器log文件保存路径'''
        return f'{os.path.dirname(__file__)}/data/performance.json'

    @staticmethod
    def get_bookmarkdata_path():
        '''调用add网络请求的记录'''
        return f'{os.path.dirname(__file__)}/data/bookmarkdata.json'

    # 驱动位置
    @staticmethod
    def get_chromedriver_exe_path():
        '''谷歌驱动路径'''
        return f'{os.path.dirname(__file__)}/chromedriver.exe'

    @staticmethod
    def get_geckodriver_exe_path():
        '''火狐驱动路径'''
        return f'{os.path.dirname(__file__)}/driver/geckodriver.exe'

    @staticmethod
    def get_edgedriver_exe_path():
        '''edge驱动路径'''
        return f'{os.path.dirname(__file__)}/msedgedriver.exe'

    # 文件夹路径
    @staticmethod
    def get_data_dir():
        '''data文件夹路径'''
        return f'{os.path.dirname(__file__)}/data/'

    @staticmethod
    def get_data_temp_dir():
        '''temp文件夹路径'''
        return f'{path.get_data_dir()}temp/'

    @staticmethod
    def getcwd():
        '''获得环境文件夹路径'''
        return f'{os.path.dirname(__file__)}/'

    @staticmethod
    def get_tutu_dir():
        return f'{os.path.dirname(__file__)}/tutu/'


class url:
    pixiv = 'https://www.pixiv.net/'
    pixiv_login_page = 'https://accounts.pixiv.net/\
        login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'

    discovery_page = 'https://www.pixiv.net/discovery'

    @staticmethod
    def get_pixiv():
        return 'https://www.pixiv.net/'

    @staticmethod
    def get_pixiv_login_page():
        return 'https://accounts.pixiv.net/\
            login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'

    @staticmethod
    def get_discover_page():
        return 'https://www.pixiv.net/discovery'


class recordcookie:
    custom_cookie = {}

    headtemplate = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'referrer': 'https://www.pixiv.net/discovery'
    }

    @staticmethod
    def get_headtemplate():
        return recordcookie.headtemplate.copy()

    @staticmethod
    def get_head_with_cookie():
        from src import tool
        '''获取本地cookie'''
        head = recordcookie.headtemplate

        cookiejson = tool.get_json_data(path.get_cookie_path())
        # 如果没有值的花就直接来个新的
        if type(cookiejson) != list:
            cookiejson = []

        # 添加客制化cookie
        for name in recordcookie.custom_cookie.keys():
            tempdict = {'name': name, 'value': config.custom_cookie.get(name)}
            cookiejson.append(tempdict)

        # 添加已经抓取的cookie到head
        cookiestr = ''
        for i, item in enumerate(cookiejson):
            name = item.get('name')
            value = item.get('value')
            temp = None
            temp = f'{name}={value}' if i == 0 else f'; {name}={value}'
            cookiestr += temp

        head['cookie'] = cookiestr

        return head

    @staticmethod
    def update_cookies(oldcookies: list, newcookies: list) -> list:
        '''
        更新cookie 返回用新cookie更新后的cookie数据
        '''
        if newcookies is None:
            return

        oldcopy = oldcookies.copy()
        add = []
        for new in newcookies:
            isadd = True
            for old in oldcopy:
                if old.get('name').__eq__(new.get('name')):
                    old.update(new)
                    isadd = False
                    break
            if isadd:
                add.append(new)

        oldcopy.extend(add)
        return oldcopy

    @staticmethod
    def update_local_cookies(newcookies: list):
        from src import tool
        '''
        用新cookie 更新到本地
        '''
        oldcookie = tool.get_json_data(path.get_cookie_path())
        if oldcookie is None:
            # 如果先前没有值直接保存
            oldcookie = newcookies
        else:
            oldcookie = recordcookie.update_cookies(oldcookie, newcookies)
        tool.save_str_data(path.get_cookie_path(),
                           json_str=json.dumps(oldcookie))

    @staticmethod
    def append_record_pid_local(pid, is_success):
        from src import tool
        '''
        将pid根据是否成功添加到本地下载记录列表
        下载pid后回调函数
        '''
        # 如果没有成功下载不执行
        if not is_success:
            return

        record = tool.get_json_data(path=path.get_download_record_path())
        if record is None:
            record = []

        record.append(pid)
        tool.save_str_data(path.get_download_record_path(), json.dumps(record))

    @staticmethod
    def contrast_with_localrecord(id_list: list):
        from src import tool
        '''
        和本地下载记录对比 返回一个字典包含了
        record: 本地下载列表
        unrecorded: 对比之后发现没有被记录的
        recorded: 已经被记录过的项
        '''
        record = tool.get_json_data(path.get_download_record_path())
        if record is None:
            record = []

        recorded = []
        unrecorded = []
        for id in id_list:
            if id in record:
                recorded.append(id)
            else:
                unrecorded.append(id)

        return {
            'record': record,
            'unrecorded': unrecorded,
            'recorded': recorded
        }


# 通过静态方法调用放外面
# 默认设置
default_setting = {
    'image_quality': 'original',  # thumb_mini small regular original 图片质量
    'is_cover': False,  # 是否覆盖
    'browser': 'edge',  # firefox chrome
    'forcelogin': False,  # 是否强制登录
    'download_path': path.get_tutu_dir(),  # 下载文件夹
    'is_proxies': True,  # 是否启用代理
    'proxies': {  # 代理
        'http': 'http://127.0.0.1:1080',
        'https': 'https://127.0.0.1:1080'
    },
    'mode': 'save',
    'limit': 60,
    'lang': 'zh',
    'skip_recorded': True,
    'retry': 3
}

# 读取Config.ini
conf_path = f'{os.path.dirname(__file__)}/Config.ini'
conf = configparser.ConfigParser()
conf.read(conf_path, encoding='utf-8')

# section名称
ads = 'auto_download_setting'
link = 'link'


class config:
    '''设置类获得所有ini里面的设置'''

    @staticmethod
    def get_image_quality():
        '''获取图片质量'''
        image_quality = conf.get(ads,
                                 'image_quality',
                                 fallback=default_setting.get('image_quality'))
        if image_quality.__eq__('thumb_mini') or image_quality.__eq__(
                'small') or image_quality.__eq__(
                    'regular') or image_quality.__eq__('original'):
            return image_quality

        return default_setting.get('image_quality')

    @staticmethod
    def get_is_cover():
        '''获取是否被覆盖'''
        return conf.getboolean(ads,
                               'is_cover',
                               fallback=default_setting.get('is_cover'))

    @staticmethod
    def get_browser():
        '''获取设置的浏览器'''
        browser = conf.get(link,
                           'browser',
                           fallback=default_setting.get('browser'))
        if browser.__eq__('chrome') or browser.__eq__(
                'firefox') or browser.__eq__('edge'):
            return browser

        return default_setting.get('browser')

    @staticmethod
    def get_forcelogin():
        '''获取是否强制登录'''
        return conf.getboolean(ads,
                               'forcelogin',
                               fallback=default_setting.get('forcelogin'))

    @staticmethod
    def get_ads_download_path():
        '''获取设置的下载位置'''
        path = conf.get(ads,
                        'download_path',
                        fallback=default_setting.get('download_path'))
        if os.path.exists(path=path):
            return path if path[path.__len__() - 1].__eq__('/') else f'{path}/'
        return default_setting.get('download_path')

    @staticmethod
    def get_is_proxies():
        '''获取是否打开代理'''
        return conf.getboolean(link,
                               'is_proxies',
                               fallback=default_setting.get('is_proxies'))

    @staticmethod
    def get_proxies_dict():
        '''获取代理的地址和端口字典'''
        http = conf.get(link, 'http', fallback='http://127.0.0.1:1080')
        https = conf.get(link, 'https', fallback='https://127.0.0.1:1080')

        return {'http': http, 'https': https}

    @staticmethod
    def get_discovery_query_dict():
        '''获取需要请求的查询字符串'''
        qd = {}

        mode = conf.get(ads, 'mode', fallback=default_setting.get('mode'))
        if mode.__eq__('save') or mode.__eq__('all') or mode.__eq__('r18'):
            qd['mode'] = mode
        else:
            qd['mode'] = default_setting.get('mode')

        limit = conf.getint(ads,
                            'limit',
                            fallback=default_setting.get('limit'))
        qd['limit'] = limit

        lang = conf.get(ads, 'lang', fallback=default_setting.get('lang'))
        if lang.__eq__('en') or lang.__eq__('ko') or lang.__eq__(
                'zh') or lang.__eq__('zh_tw') or lang.__eq__('romaji'):
            qd['lang'] = lang
        else:
            qd['lang'] = default_setting.get('lang')

        return qd

    @staticmethod
    def get_skip_recorded():
        '''获取是否跳过记录的id项'''
        return conf.getboolean(ads,
                               'skip_recorded',
                               fallback=default_setting.get('skip_recorded'))

    @staticmethod
    def get_retry():
        '''获取重试次数'''
        return conf.getint(ads, 'retry', fallback=default_setting.get('retry'))

    @staticmethod
    def build_custom_opener() -> request.OpenerDirector:
        '''根据config.ini创建一个具有代理的opener'''
        if not config.get_is_proxies():
            return request.build_opener()
        # 代理
        proxies = config.get_proxies_dict()
        prox = request.ProxyHandler(proxies=proxies)
        return request.build_opener(prox)  # opener

    @staticmethod
    def tips():
        '''debug 打印'''
        print('=' * 30, 'Tips', '=' * 30)
        print('当前设置:')
        print(f'图片质量image_quality : {config.get_image_quality()}')
        print(f'是否覆盖is_cover : {config.get_is_cover()}')
        print(f'浏览器browser : {config.get_browser()}')
        print(f'是否强制登录forcelogin : {config.get_forcelogin()}')
        print(f'下载保存路径download_path : {config.get_ads_download_path()}')
        print(f'代理 is_proxies : {config.get_is_proxies()}')
        print(config.get_proxies_dict())
        print(f'api查询字符串参数：\n{config.get_discovery_query_dict()}')
        print(f'是否跳过记录中的pid skip_recorded : {config.get_skip_recorded()}')
        print(f'cookie_path:{path.get_cookie_path()}')
        print(f'discovery返回数据path:{path.get_ajax_discovery_data_path()}')
        print(f'需要谷歌驱动位置:{path.get_chromedriver_exe_path()}')
        print(f'需要火狐驱动位置:{path.get_geckodriver_exe_path()}')
        print(f'需要Edge驱动位置:{path.get_edgedriver_exe_path()}')
        print('=' * 60)


# 创文件夹（防止被删）
if not os.path.exists(path.get_data_dir()):
    os.makedirs(path.get_data_dir())
if not os.path.exists(path.get_tutu_dir()):
    os.makedirs(path.get_tutu_dir())
