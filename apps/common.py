import uuid


def random_string():
    return uuid.uuid4().hex


if __name__ == '__main__':
    print(random_string())