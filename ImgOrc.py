#   图片识别模块
from PIL import Image
import pytesseract

class ImgOrc(object):
    """docstring for ImgOrc.
    图片验证码识别
    """
    def __init__(self, imgpath):
        self.imgpath = imgpath
        self.img = None
        self.dealImg()

    def loadImg(self, p):
        self.img = Image.open(p)

    def dealImg(self):
        image = Image.open(self.imgpath)
        image = image.convert('L')  # 将图像转化为灰度图像
        image = image.convert('1')  # 将图像转化为二值化图像，二值化阈值默认是127
        # 现将图片转化成灰度图像，再转化成二值化图像
        image = image.convert('L')
        threshold = 80  # 设定阈值
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        self.img = image.point(table,'1')

    def imgToCode(self):
        str = pytesseract.image_to_string(self.img)
        str = "".join(filter(lambda s:s.isalnum(), list(str))) #    过滤特殊字符，保留数组和字母
        return str

# if __name__ == '__main__':
#     p = "./temp/e467d049e3bd6463085a99599243f29d.jpg"
#     img_1 = ImgOrc(p)
#     print(img_1.imgToCode())
