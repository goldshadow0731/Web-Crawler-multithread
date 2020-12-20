import os
from os.path import isdir, join
from hashlib import md5

class Repeat:
    def __init__(self, path, folder_name):
        self.path = path
        self.folder_name = folder_name
        self.all_size = {}
        self.total_file = 0
        self.total_delete = 0
        self.total_images = 0

    def getmd5(self, filename):
        file_txt = open(filename, 'rb').read()
        return md5(file_txt).hexdigest()

    def main(self):
        for file in os.listdir(self.path + self.folder_name):
            self.total_file += 1
            real_path = os.path.join(self.path + self.folder_name, file)

            if os.path.isfile(real_path) == True:
                size = os.stat(real_path).st_size
                name_and_md5 = [real_path, '']

                if size in self.all_size.keys():
                    new_md5 = self.getmd5(real_path)
                    if self.all_size[size][1] == '':
                        self.all_size[size][1] = self.getmd5(self.all_size[size][0])
                    if new_md5 in self.all_size[size]:
                        os.remove(self.path + self.folder_name + '/' + file)
                        self.total_delete += 1
                    else:
                        self.all_size[size].append(new_md5)
                else:
                    self.all_size[size] = name_and_md5
        self.total_images = self.total_file - self.total_delete

        # print(self.folder_name)
        print(self.folder_name,'-檔案張數：', self.total_file)
        print(self.folder_name,'-刪除張數：', self.total_delete)
        print(self.folder_name,'-未重複張數', self.total_images)
        print()
        self.total_file = 0
        self.total_delete = 0

    def start(self):
        self.main()
