# coding: utf-8

import rsa
import os
import base64

from seecode.libs.core.data import logger
from seecode.libs.core.common import make_dir


class RSAEncrypt(object):
    public_str = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAinv0brLfzd/671g70Sd3872tMfdr4kfvTrWEhmCz8PlBZSDk0I2N
Wiekk4AniFuDt2mUoIFzB4x5/SqTa0eK2kkJJK0826Peunrj/qvmTlviYaWbOYzx
Jr+WBqfAK8PpzNCG0GITheANJUzanljPPgvQpN5NW6fPArgLp3MTRUWgUP/TXE/C
JMTY47bwvz+DqsQBm7uUiSOG/62jvC0jeUlfhZscf68Uq/NYdLiXwThJBL8lkloz
5lICCKleZDBFYebNENDAVWnrmfKyh2ftbguk9jLFJjdQHBrUldS8tJxMdQ6Y+Qqs
1ErceIEKciNf1GZ9f82qmdXDXbFyCwPz6wIDAQAB
-----END RSA PUBLIC KEY-----
"""
    private_str = """-----BEGIN RSA PRIVATE KEY-----
MIIEqAIBAAKCAQEAinv0brLfzd/671g70Sd3872tMfdr4kfvTrWEhmCz8PlBZSDk
0I2NWiekk4AniFuDt2mUoIFzB4x5/SqTa0eK2kkJJK0826Peunrj/qvmTlviYaWb
OYzxJr+WBqfAK8PpzNCG0GITheANJUzanljPPgvQpN5NW6fPArgLp3MTRUWgUP/T
XE/CJMTY47bwvz+DqsQBm7uUiSOG/62jvC0jeUlfhZscf68Uq/NYdLiXwThJBL8l
kloz5lICCKleZDBFYebNENDAVWnrmfKyh2ftbguk9jLFJjdQHBrUldS8tJxMdQ6Y
+Qqs1ErceIEKciNf1GZ9f82qmdXDXbFyCwPz6wIDAQABAoIBACONaRZWU8Ct5OU3
eLvcbx4jLuiqBYdlQlmpnilFgEy4IQLObA/il0xy6vx3JS8Ll4gp0d9W/GoOtW66
VHhxOIOLxo4k73/P1Sl4zTmfdhPd4QOCmZQvy+VPwDtbK6nQtSBA1KuA0lRHTfiq
f2GxmRrru5fn/mIudWziubP0EvMlbWi3nQ4CQGwR+6mP7T/O7EPibirMrmZFwotU
dF5e0gynY/6SHai9jH/84nAuPdDlWi6xVa9I2e2SmGhAb1aRIEOfWOWrJAeE0W2B
x+FEqZcNLDqg2gMOyR3Ay73kmDZXPi2D/1IMeUxY+P1hiZypEyneBs2FcAY1S6Be
i/2QmKkCgYkA3c3PVGgut0aPpz17a8fwTMtKhuIw1yjnc9lysCQYd0vHiDjdoAKS
qHpAvnfETJ8ZMBT/aRzShh+sLtXJZI8mvC/6BUOkPpENRJoF602I7he7M2IRlNr4
F/v9UJHqFnrsWi8Rdc3atoubuAtVr1mlYa33mBpZEIFLe6PbYHPt8efeWGStNJQZ
BwJ5AJ/Vq02rciKwrqa6HQtVAyhNIudlfpt9B0IrbCnG9HaAG9pqb4Sc0QbTF9zY
4/mP1BTirUfCSYX6tW4PuVhnnIBagxc74rvHSInI+Mt25kbgyjb29CPxVKJa8Sss
66H5yXVjvNWoyBlHrz31pZ+NZvRVUNtwUGkI/QKBiBv7dwijDCG7GSx0KTnzw3Es
xH430wmR84E+EaX/J8cFHGsnIW6qZG403i4pVe6Es9zJCV/tbvHU1RgjiIDTPoPH
WbeITRRHoHDjLZP9+CRxggB9gtJQvbPo6pBbmDi10VOfVIiUK9+TxVV2uJyipqao
F/Bsgof+h9NVXLvSZFZ8diSYrvFPLckCeBJrDNJmb0CQG5Aa4j3sDfEW8m63w18n
iS6W0l/+DS2alZsVqMQfTfb7XESWua6IZGgDtvQN72sA+Oc16KXHSsF/rJuAyx/Y
VwOJpSHNEbwZKzQqQPfjV11eHWxcQMrpfc2JMLluOaCwIgGBzRQVt0dwjWC8EIgK
AQKBiHUo8WEpI30Mca7vtaRQD6U1upaUmMvPBVl7R75/1kp13sQGUEsV7fBZ5f0o
4XkCnOZDL6oIEe4HGJviK+NJcpTdyI5ROckg/bWCogbsreswnbW+jeter9AYVf5F
8oLWXr7cnbUhpgm2AB36fa3z3+Q9ZqoQk6nBDnOWTxTxkttDlyUi++FQSVU=
-----END RSA PRIVATE KEY-----
"""

    def __init__(self, nbits=2048):
        if RSAEncrypt.public_str:
            self.public_key = rsa.PublicKey.load_pkcs1(RSAEncrypt.public_str.encode())
        if RSAEncrypt.private_str:
            self.private_key = rsa.PrivateKey.load_pkcs1(RSAEncrypt.private_str.encode())
        self.default_length = int(nbits / 8 - 11)
        self.hash_method = 'SHA-256'

    def load(self, public_file, private_file):
        """

        :param public_file:
        :param private_file:
        :return:
        """
        with open(public_file, 'r') as fp:
            self.public_key = rsa.PublicKey.load_pkcs1(fp.read().encode())
        with open(private_file, 'r') as fp:
            self.private_key = rsa.PrivateKey.load_pkcs1(fp.read().encode())

    def generate_pem(self, save_path, nbits=2048):
        """

        :param save_path:  保存路径
        :param nbits:
        :return:
        """
        make_dir(save_path)
        self.public_key, self.private_key = rsa.newkeys(nbits)
        public_pem = os.path.join(save_path, 'public.pem')
        private_pem = os.path.join(save_path, 'private.pem')
        try:
            with open(public_pem, 'w+') as fp:
                fp.write(self.public_key.save_pkcs1().decode())

            with open(private_pem, 'w+') as fp:
                fp.write(self.private_key.save_pkcs1().decode())
        except Exception as ex:
            logger.error(ex)

        return public_pem, private_pem

    def encrypt_str(self, message):
        """

        :param message:
        :return:
        """
        if not isinstance(message, bytes):
            msg = message.encode('utf-8')
        else:
            msg = message
        length = len(msg)

        # 长度不用分段
        if length < self.default_length:
            return base64.b64encode(rsa.encrypt(msg, self.public_key))
        # 需要分段
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > self.default_length:
                res.append(rsa.encrypt(msg[offset:offset + self.default_length], self.public_key))
            else:
                res.append(rsa.encrypt(msg[offset:], self.public_key))
            offset += self.default_length
        byte_data = b''.join(res)

        return base64.b64encode(byte_data)

    def encrypt_file(self, file_path, save_path=None):
        """

        :param file_path:
        :param save_path:
        :return:
        """
        if not save_path:
            save_path = '{0}.crypto'.format(file_path)
        if os.path.isfile(file_path):
            with open(save_path, 'wb') as output, open(file_path, 'rb') as fp:
                output.write(self.encrypt_str(fp.read()))
        return save_path

    def decrypt_str(self, message):
        """

        :param message:
        :return: bytes
        """
        msg = base64.b64decode(message)
        length = len(msg)
        default_length = self.default_length + 11
        # 长度不用分段
        if length < default_length:
            return rsa.decrypt(msg, self.private_key)
        # 需要分段
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(rsa.decrypt(msg[offset:offset + default_length], self.private_key))
            else:
                res.append(rsa.decrypt(msg[offset:], self.private_key))
            offset += default_length
        return b''.join(res)

    def decrypt_file(self, file_path, save_path=None):
        """

        :param file_path:
        :param save_path:
        :return:
        """
        if os.path.isfile(file_path):
            if not save_path:
                save_path = '{0}.zip'.format(file_path)
            with open(save_path, 'wb') as output, open(file_path, 'rb') as fp:
                output.write(self.decrypt_str(fp.read()))

    def sign(self, message, hash_method=None):
        """

        :param message:
        :param hash_method:
        :return:
        """
        return rsa.sign(message.encode(), self.private_key, hash_method or self.hash_method)

    def verify(self, message, signature, hash_method=None):
        """

        :param message:
        :param signature:
        :param hash_method:
        :return:
        """
        try:
            compare_hash_method = hash_method or self.hash_method
            hash_m = rsa.verify(message.encode(), signature, self.public_key)
            if hash_m == compare_hash_method:
                return True
            else:
                return False
        except:
            return False
