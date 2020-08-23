from captcha.image import ImageCaptcha
from PIL import Image
import random,string


def random_captcha():
    captcha_text = []
    letter = list(string.ascii_letters)
    total = [str(i) for i in range(10)] + letter
    for i in range(4):
        c = random.choice(total)
        captcha_text.append(c)
    return ''.join(captcha_text)  # 字符串中间没有空格

# 生成验证码方法
def gen_capthca():
    image = ImageCaptcha()
    captcha_text = random_captcha()
    captcha_image = Image.open(image.generate(captcha_text))
    return captcha_text, captcha_image
