import os
from typing import Text, BinaryIO, Tuple


class CheckImage():
    @staticmethod
    def open_image(img_path: Text) -> BinaryIO:
        """Open image

        Args:
            img_path (Text): Image path

        Returns:
            BinaryIO: Binary image
        """
        with open(img_path, "rb") as fp:
            fp.seek(-2, 2)
            img_text = fp.read()
        return img_text

    @classmethod
    def check_jpeg(cls, img_path: Text) -> bool:
        """Check jpeg integrity

        Args:
            img_path (Text): Image path

        Returns:
            bool: Is the image complete
        """
        return cls.open_image(img_path).endswith(b'\xff\xd9')

    @classmethod
    def check_png(cls, img_path: Text):
        """Check png integrity

        Args:
            img_path (Text): Image path

        Returns:
            bool: Is the image complete
        """
        return cls.open_image(img_path).endswith(b'\xaeB`\x82')

    @classmethod
    def run(cls, image_path: Text) -> Tuple[int, int, int]:
        """Check image integrity

        Args:
            image_path (Text): Image path

        Returns:
            Tuple[int, int, int]: complete, incomplete, error
        """
        complete = 0
        incomplete = 0
        error = 0

        for image in os.listdir(image_path):
            file_path = os.path.join(image_path, image)

            if os.path.isfile(file_path):
                image_extension = os.path.splitext(image)[1].lower()

                if image_extension == '.jpg' or image_extension == ".jpeg":
                    ret = cls.check_jpeg(file_path)
                elif image_extension == '.png':
                    ret = cls.check_png(file_path)
                else:
                    ret = None

                if ret is True:
                    complete += 1
                elif ret is False:
                    incomplete += 1
                    os.remove(file_path)
                else:
                    error += 1

        return complete, incomplete, error


if __name__ == '__main__':
    base_path = './images'
    for category in os.listdir(base_path):
        print(f'Check Image - {category}')
        complete, incomplete, error = CheckImage.run(
            os.path.join(base_path, category))
        print(f'{category} - {"normal":>8s}: {complete:5d}')
        print(f'{category} - {"distory":>8s}: {incomplete:5d}')
        print(f'{category} - {"error":>8s}: {error:5d}')
