import os
from Repeat import Repeat

if __name__ == '__main__':
    path = './train/'
    for list_dir in os.listdir(path):
        Repeat(path, list_dir).start()
