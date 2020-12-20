import os
from .CheckImage import CheckImage


class CheckBrockImage(object):
    def __init__(self, path, folder_name):
        self.path = path
        self.folder_name = folder_name
        self.completeFile = 0
        self.incompleteFile = 0
    def getImgs(self):
        """搜尋底下圖片"""
        for file in os.listdir(self.path + self.folder_name):
            if os.path.splitext(file)[1].lower() == '.jpg' or os.path.splitext(file)[1].lower() == ".jpeg":
                ret = self.checkImg(file)
                if ret:
                    self.completeFile += 1

                else:
                    self.incompleteFile = self.incompleteFile + 1
                    self.imgRemove(file)  # 删除不完整图片

    def imgRemove(self, file):
        """刪除圖片"""
        os.remove(self.path + self.folder_name + '/' + file)

    def checkImg(self, img_file):
        """檢測圖片"""
        return CheckImage(self.path + self.folder_name + '/' + img_file).checkJpgJpeg()

    def start(self):
        """執行程式"""
        self.getImgs()
        print(self.folder_name,'-毀損圖片 : %d個' % self.incompleteFile)
        print(self.folder_name,'-正常圖片 : %d個' % self.completeFile)
        print()

# if __name__ == '__main__':
#     Ldir = './train/'
#     for Rdir in os.listdir(Ldir):
#         print('正在檢測' + Rdir + ':')
#         train_dir = Ldir + Rdir + '/'   # 检测文件夹
#         imgs = CheckBrockImage(train_dir)
#         imgs.start()
