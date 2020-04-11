import uuid
from pypinyin import lazy_pinyin


def random_string():
    return uuid.uuid4().hex


def check_filename(file):
    return True


if __name__ == '__main__':
    print(random_string())