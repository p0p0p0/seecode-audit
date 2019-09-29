# coding: utf-8


from seecode.libs.core.datatype import AttribDict
from seecode.libs.core.log import logger

logger = logger

paths = AttribDict()

# 配置文件初始化
conf = AttribDict()
conf.storage = {
    'ftp': None,
    'aws': None,
}
