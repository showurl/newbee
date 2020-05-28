import base64
from Crypto.Cipher import AES
import json
import os

from newbee.newbee_util.pro_log import logger

from newbee.config import BASE_DIR

'''
采用AES对称加密算法
'''

with open(os.path.join(BASE_DIR, "sign_key")) as file:
    sign_key = file.readline().replace("\r", "").replace("\n", "")


def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'
    # return str.encode(value)  # 返回bytes
    return bytes.fromhex(value)


# 加密方法
def encrypt_oracle(key, text):
    if not text:
        return None
    logger.debug("加密之前的数据是:%s" % text)
    if not isinstance(text, str):
        text = json.dumps(text).replace(" ", "")
    text = text.replace(" ", "")
    cipher = AES.new(add_to_16(key), AES.MODE_ECB)
    x = AES.block_size - (len(text) % AES.block_size)
    if x != 0:
        text = text + chr(x) * x
    msg = cipher.encrypt(text.encode(encoding="utf-8"))
    # msg = base64.urlsafe_b64encode(msg).replace('=', '')
    msg = base64.b64encode(msg)
    # print(msg.decode("utf-8"))
    return msg.decode("utf-8")


# 解密方法
def decrypt_oralce(key, text):
    if not text:
        return None
    unpad = lambda s: s[0:-s[-1]]
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    # 优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(bytes(text, encoding='utf-8'))
    decrypted_text = unpad(aes.decrypt(base64_decrypted)).decode('utf-8').replace('\0', '')
    try:
        logger.debug("解密之后的数据是:%s" % json.loads(decrypted_text))
        return json.loads(decrypted_text)
    except:
        logger.debug("解密之后的数据是:%s" % decrypted_text)
        return decrypted_text


if __name__ == '__main__':
    pass
