import string
from random import choice

def generate_random(random_length):
    """

    :param random_length: 字符串长度
    :return:
    """
    random_str=[]
    while(len(random_str)<random_length):
        random_str.append(choice(string.digits))
    return ''.join(random_str)

if __name__ == '__main__':
    print(generate_random(6))