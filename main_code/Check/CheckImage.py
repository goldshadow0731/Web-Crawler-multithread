class CheckImage(object):
    def __init__(self, img):
        with open(img, "rb") as f:
            f.seek(-2, 2)
            self.img_text = f.read()
            f.close()

    def checkJpgJpeg(self):
        """检测jpg图片完整性，完整返回True，不完整返回False"""
        buf = self.img_text
        return buf.endswith(b'\xff\xd9')

    def checkPng(self):
        """检测png图片完整性，完整返回True，不完整返回False"""
        buf = self.img_text
        return buf.endswith(b'\xaeB`\x82')
