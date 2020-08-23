import django.conf
import os
import configparser

BASE_DIR = django.conf.settings.BASE_DIR
# BASE_DIR = "/Users/mashouyue/PycharmProjects/django_newbee_framework/Django_NEWBEE_AUTOAPI"
NEWBEE_INI = os.path.join(BASE_DIR, "newbee_config.ini")

if not os.path.exists(NEWBEE_INI):
    with open(NEWBEE_INI, 'a') as ini:
        ini.write("# 数据加密中间件配置\r\n"
                  "[DT]\r\n"
                  "# 是否允许接收json数据(未加密)\r\n"
                  "is_recv_json = True\r\n"
                  "# 是否返回加密响应\r\n"
                  "is_send_text = True\r\n"
                  "# 不包含哪些路径 格式：[\"newbee/v1.0.1/area/data\", \"newbee/v1.0.1/user/data\"&&\"POST\", ...]\r\n"
                  "exclude_path = []\r\n"
                  "\r\n"
                  "# 查询时的配置\r\n"
                  "[FIND]\r\n"
                  "# 分页查询时默认一页的行数\r\n"
                  "FINDDEFUALTPAGESIZE = 10\r\n"
                  "# URL配置\r\n"
                  "[URL]\r\n"
                  "# 填写你需要修改的PATH, 无论修改成什么, 都必须有/<str:action>/\r\n"
                  "PATH = newbee/v1.0.1/<str:action>/data\r\n"
                  )

config = configparser.ConfigParser()
# -read读取ini文件
config.read(NEWBEE_INI, encoding='utf-8')
is_recv_json = True if config.get('DT', 'is_recv_json').lower().strip() in ("true", "1") else False
is_send_text = True if config.get('DT', 'is_send_text').lower().strip() in ("true", "1") else False
exclude_path_ = config.get('DT', 'exclude_path') or None

if exclude_path_:
    exclude_path_ = str(exclude_path_).replace(" ", "").split(",")
exclude_path = []
for exclude in exclude_path_:
    if "&&" in exclude:
        exclude_path.append(list(exclude.split("&&")))
    else:
        exclude_path.append(exclude)

FINDDEFUALTPAGESIZE = config.getint('FIND', 'FINDDEFUALTPAGESIZE') or 10
PATH = config.get('URL', 'PATH') or "newbee/v1.0.1/<str:action>/data"
