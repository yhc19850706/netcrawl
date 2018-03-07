import logging
from wxpy import *


class Wxml(object):
    def __init__(self):
        self.bot = Bot(console_qr=-2, cache_path=True, qr_path = '/Users/yhc/devtool/workspace/weixin/qr/wxpy.pkl')
        self.bot.enable_puid(path='/Users/yhc/devtool/workspace/weixin/wxpy_puid.pkl')
        # 在 Web 微信中把自己加为好友
        self.bot.self.add()
        self.bot.self.accept()

    #查找朋友
    def find_friend(self, name):
        friends = self.bot.friends().search(name)[0]
        return friends

    @staticmethod
    def send_txt(my_friend, txte):
        # 发送文本
        my_friend.send(txte)

    @staticmethod
    def send_img(my_friend, img):
        # 发送图片
        my_friend.send_image(img)

    @staticmethod
    def send_video(my_friend, video_name):
        # 发送视频
        my_friend.send_video(video_name)

    @staticmethod
    def send_file(my_friend, file_name):
        # 发送文件
        my_friend.send_file(file_name)

    @staticmethod
    def send_gif(self, my_friend, gif_img):
        # 以动态的方式发送图片
        my_friend.send(gif_img)


if __name__=='__main__':
    wxml = Wxml()
    friend = wxml.find_friend('殷化程')
    if friend:
        Wxml.send_txt(friend, '你好')
