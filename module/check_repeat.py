from hashlib import md5
import os
from typing import Text, Tuple


class CheckRepeat():
    @staticmethod
    def get_MD5(file_name: Text) -> Text:
        """Get MD5's value of file

        Args:
            file_name (Text): File name

        Returns:
            Text: The MD5's value of file
        """
        with open(file_name, 'rb') as fp:
            file_txt = fp.read()
        return md5(file_txt).hexdigest()

    @classmethod
    def run(cls, image_path: Text) -> Tuple[int, int]:
        """Check image repect

        Args:
            path (Text): Image Path

        Returns:
            Tuple[int, int]: images, delete
        """
        images = 0
        delete = 0
        all_size = dict()

        for image in os.listdir(image_path):
            file_path = os.path.join(image_path, image)

            if os.path.isfile(file_path):
                size = os.stat(file_path).st_size
                md5_result = cls.get_MD5(file_path)

                if size not in all_size.keys() or md5_result not in all_size[size]:
                    images += 1
                    all_size.get(size, []).append(md5_result)
                else:
                    delete += 1
                    os.remove(file_path)

        return images, delete


if __name__ == "__main__":
    base_path = './images'
    for category in os.listdir(base_path):
        print(f'Check Repect - {category}')
        images, delete = CheckRepeat.run(os.path.join(base_path, category))
        print(f'{category} - {"remain":>8s}: {images:5d}')
        print(f'{category} - {"delete":>8s}: {delete:5d}')
