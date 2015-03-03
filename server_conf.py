# -*- coding: UTF-8 -*-
from tornado.options import define,options as _options
import logging,os

define('root_path', default='/opt/spzhuan/api', help='invite pkg path')
define('package_path', default='/opt/spzhuan/api/html/pkg/', help='invite pkg path')
define("package_domain", default="sohu-cdn.dianjoy.com", help="package request domain")
define('port', default=8899, help='this server will listen on the port')
define('process', default=16, help='work process')
define('debug', default=False, help='is in debug mode?')
define('appid', default="c81bc556d5dc52b854f591320d4c951b", help='is in debug mode?')
define('iosappid', default="5763c2eb596b7a4e511f588d4ee7e50f", help='is in debug mode?')

define("db_host", default="", help="db_host")
define("db_port", default="", help="db_port")
define("db_uname", default="", help="db_uname")
define("db_upass", default="", help="db_upass")
define("db_name", default="", help="db_name")

define("db_host_name_list", default="", help="db_host")

# define("db_r_host", default="", help="db_host")
# define("db_r_port", default="", help="db_port")
# define("db_r_uname", default="", help="db_uname")
# define("db_r_upass", default="", help="db_upass")
# define("db_r_name", default="", help="db_name")
#
# define("db_d_host", default="", help="db_host")
# define("db_d_port", default="", help="db_port")
# define("db_d_uname", default="", help="db_uname")
# define("db_d_upass", default="", help="db_upass")
# define("db_d_name", default="", help="db_name")
#
# define("db_dianjoy_host", default="", help="db_host")
# define("db_dianjoy_port", default="", help="db_port")
# define("db_dianjoy_uname", default="", help="db_uname")
# define("db_dianjoy_upass", default="", help="db_upass")
# define("db_dianjoy_name", default="", help="db_name")

#添加redis服务器需要先填写名称，用“,”隔开
define('redis_host_name_list',default='', help='host list of redis server')
#添加redis服务器需要添加3项内容，中间填写名称，用“_”和其他默认部分连接
define('redis_host',default='', help='host of redis server')
define('redis_port', default=6379, help='port number of redis')
define('redis_db', default=6, help='db base number of redis')
# define('redis_ad_host',default='', help='host of redis server')
# define('redis_ad_port', default=6379, help='port number of redis')
# define('redis_ad_db', default=1, help='db base number of redis')


define("db_max_process", default=500, help="max db process num")


define('APP_VERSION', default='1.1.1', help='app version for update') # 用户端提示更新改这个
define('APP_VERSION_DEL', default='1', help='app version for delelop')
define('PAK_VERSION', default='1.3.2.5', help='package show version') # 打渠道包修改这个
define('PAK_VERSION_CHANNEL', default='1.3.2.5', help='package jump version') # 渠道包跳转修改这个
# 默认的下载地址  这个需要舜东传到CDN
define('APP_NEW_APK', default='http://fast-cdn.dianjoy.com/dev/upload/ad_url/hongbao/hongbaosuoping.apk', help='app version apk for update')
define('IOS_APP_NEW_APK', default='itms-services://?action=download-manifest&url=https://www.hongbaosuoping.com/plist/update.plist', help='ios_app version apk for update')
# define('IOS_APP_NEW_APK', default='itms-services://?action=download-manifest&url=https://www.hongbaosuoping.com/plist/share.plist', help='ios_app version apk for update')

_LOCAL_PATH_ = os.path.abspath(os.path.dirname(__file__))
_CONF_PATH_ = _LOCAL_PATH_+"/server.conf"
try:
    _options.parse_config_file(_CONF_PATH_)
except:
    logging.error('load server.conf failed , use command line option')

#通过第一次加载的配置项再增加数据库等配置项，这种情况需要再加载一遍，因为tornado必须在这里定于
for db_tag in _options.db_host_name_list.split(","):
    define("db_"+db_tag+"_host", default="", help="db_host")
    define("db_"+db_tag+"_port", default="", help="db_port")
    define("db_"+db_tag+"_uname", default="", help="db_uname")
    define("db_"+db_tag+"_upass", default="", help="db_upass")
    define("db_"+db_tag+"_name", default="", help="db_name")

for db_tag in _options.redis_host_name_list.split(","):
    define("redis_"+db_tag+"_host", default="", help="db_host")
    define("redis_"+db_tag+"_port", default=6379, help="db_port")
    define("redis_"+db_tag+"_db", default=1, help="db_uname")

#通过二次加载解决无法增加不存在配置项问题
try:
    _options.parse_config_file(_CONF_PATH_)
except:
    logging.error('second load server.conf failed , use command line option')

