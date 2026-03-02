import hashlib


class MD5Utility:
    @staticmethod
    def encrypt(text: str, encoding: str = 'utf-8') -> str:
        """
        对输入的文本进行MD5加密

        参数:
            text: 待加密的文本
            encoding: 文本编码方式，默认为utf-8

        返回:
            加密后的MD5值（32位十六进制字符串）
        """
        try:
            # 创建MD5对象
            md5 = hashlib.md5()
            # 更新MD5对象的内容
            md5.update(text.encode(encoding))
            # 获取加密后的十六进制字符串
            return md5.hexdigest()
        except Exception as e:
            print(f"MD5加密出错: {e}")
            return None

    @staticmethod
    def verify(text: str, md5_hash: str, encoding: str = 'utf-8') -> bool:
        """
        验证文本的MD5值是否与给定的MD5哈希值匹配

        参数:
            text: 待验证的原始文本
            md5_hash: 预期的MD5哈希值
            encoding: 文本编码方式，默认为utf-8

        返回:
            如果匹配返回True，否则返回False
        """
        # 计算文本的MD5值
        encrypted = MD5Utility.encrypt(text, encoding)
        # 比较计算得到的MD5值与给定的MD5值
        return encrypted == md5_hash
