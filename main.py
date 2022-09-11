'''
https://github.com/Sugobet/EVE_Get_MaNei

Sugobet
QQ: 321355478
qq群: 924372864
'''

import os
import time
import datetime
from PIL import Image
import cv2
from cnocr import CnOcr
import threading
import random


path = 'C:/Users/sugob/Desktop/EVE_Get_MaNei'       # 脚本文件夹绝对路径  （反斜杠改斜杠）
devices = {'kuanggong1': '127.0.0.1:62001'}      # cmd输入adb devices查看模拟器地址
M = {
    '第一槽位': [920, 438],
    '第二槽位': [868, 438],
    '第三槽位': [814, 438],
    '第四槽位': [924, 495],
    '第五槽位': [868, 495],
    '第六槽位': [813, 495],
    '第七槽位': [762, 495],
}
high_cao = {
    'kuanggong1': [M['第一槽位']],
}      # 高槽

# 低槽
low_cao = {
    'kuanggong1': [M['第二槽位'], M['第三槽位'], M['第四槽位'], M['第五槽位'], M['第六槽位'], M['第七槽位']],
}

timer = 3        # 点击屏幕的时间间隔    单位：秒

conVal = 1.875      # 程序执行一遍的间隔时间    单位: 秒


def LoadImage(tag, path) -> Image.Image:
    try:
        img = Image.open(f'{path}/{tag}.png')
    except:
        time.sleep(3)
        return LoadImage(tag, path)
    return img


class Listening:
    def __init__(self, device_name: str, device_address: str, cnocr: CnOcr):
        self.device_name = device_name
        self.device_address = device_address

        self.ocr = cnocr

    
    def screenc(self):
        os.system(f'adb -s {self.device_address} exec-out screencap -p > {self.device_name}.png')


    def crop(self, x1, y1, x2, y2, img: Image.Image) -> Image.Image:
        try:
            newimg = img.crop((x1, y1, x2, y2))
        except Exception:
            return
        return newimg


    def IsInSpace(self, img: Image.Image):
        '''
        : 判断是否在太空
        '''
        status = self.crop(453, 511, 508, 526, img)
        if not status:
            return False

        res = self.ocr.ocr(status)
        for keys in res:
            if '米' in keys['text'] or '秒' in keys['text']:
                return True
        return False


    def IsAtSation(self, img: Image.Image):
        '''
        : 判断是否在空间站
        '''
        status = self.crop(877, 163, 941, 194, img)
        if not status:
            return False

        res = self.ocr.ocr(status)
        for keys in res:
            key: str = keys['text']
            key = key.replace(" ", "")
            if '离站' in key:
                return True
        return False

    
    def IsHaveKArea(self, img: Image.Image):
        '''
        : 判断矿区存在
        '''

        status = self.crop(260, 70, 704, 166, img)
        if not status:
            return True

        res = self.ocr.ocr(status)
        if res == []:
            return True
        for key in res:
            if '内没有可' in key['text']:
                return False
        return True


    def GetShipState(self, img: Image.Image):
        '''
        : 判断舰船状态
        : state -> 1 -> 准备跃迁
        : state -> 2 -> 跃迁至
        : state -> 3 -> 即将到达
        : state -> 4 -> 舰船正在停止
        '''
        if self.IsAtSation(img):
            return False, -1, ''

        status = self.crop(374, 394, 594, 414, img)
        if not status:
            return False, -1, ''

        res = self.ocr.ocr(status)
        if res == []:
            return False, -1, ''
        text = res[0]['text']
        if '准备' in text:
            return True, 1, '准备跃迁'
        if '跃迁至' in text:
            return True, 2, '跃迁至'
        if '即将到达' in text:
            return True, 3, '即将到达'
        if '停止' in text:
            return True, 4, '舰船正在停止'
        return False, -1, ''
    

    def FindBlueFuckShip(self, img: Image.Image):
        '''
        : 蓝加拦截 舰船监测
        '''
        status = self.crop(792, 51, 911, 316, img)
        if not status:
            return False

        res = self.ocr.ocr(status)
        if res == []:
            return False
        for key in res:
            if '拦截' in key['text']:
                tim = str(datetime.datetime.now()).replace(' ', '---')
                print(self.device_name, f'疑似蓝加拦截----------------{tim}')
                print(self.device_name, f'疑似蓝加拦截----------------{tim}')
                print(self.device_name, f'疑似蓝加拦截----------------{tim}')
                img.save(f'{path}/{self.device_name}_FUCK_BLUE_SHIP_{tim}.png')
                return True
        return False

    
    def IsMax(self, img: Image.Image):
        '''
        : 监测满仓
        '''
        status = self.crop(229, 89, 711, 171, img)
        if not status:
            return False

        res = self.ocr.ocr(status)
        if res == []:
            return False
        for key in res:
            if '满了' in key['text']:
                return True

        return False
    

    def LocalHaveEnemy(self, img: Image.Image):
        '''
        : 监测本地红白
        '''
        i1 = self.crop(82, 430, 123, 451, img)
        if not i1:
            return False
        res = self.ocr.ocr(i1)
        if res == []:
            return False
        num = (res[0]['text']).replace('o', '0').replace('O', '0').replace('D', '0').replace('U', '0')
        if len(num) >= 2:
            return True
        if len(num) == 1 and num != '0':
            return True
        
        i1 = self.crop(144, 430, 180, 452, img)
        if not i1:
            return False
        res = self.ocr.ocr(i1)
        if res == []:
            return False
        num = (res[0]['text']).replace('o', '0').replace('O', '0').replace('D', '0').replace('U', '0')
        if len(num) >= 2:
            return True
        if len(num) == 1 and num != '0':
            return True
        
        return False
        

class Command:
    def __init__(self, device_name, device_address, cnocr: CnOcr):
        self.device_name = device_name
        self.device_address = device_address
        self.ocr = cnocr

        self.adb = f'adb -s {self.device_address} '
    

    def screenc(self):
        os.system(f'adb -s {self.device_address} exec-out screencap -p > {self.device_name}.png')

    
    def crop(self, x1, y1, x2, y2, img) -> Image.Image:
        try:
            newimg = img.crop((x1, y1, x2, y2))
        except Exception:
            return
        return newimg


    def GetShipType(self):
        os.system(self.adb + f'shell input tap {7 + random.randint(2, 40)} {18 + random.randint(2, 25)}')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {110 + random.randint(2, 50)} {135 + random.randint(2, 50)}')
        time.sleep(4)

        self.screenc()
        img = LoadImage(self.device_name, path)

        state = self.crop(4, 164, 186, 198, img)
        if not state:
            img.close()
            return self.GetShipType()
        img.close()
        if not state:
            return False, -1, ''
        os.system(self.adb + 'shell input tap 924 31')

        res = self.ocr.ocr(state)
        if res == []:
            return False, -1, ''
        text = res[0]['text']
        if '回' in text:
            return True, 1, '回旋者级'
        if '获' in text:
            return True, 2, '猎获级'
        if '想级二' in text:
            return True, 4, '妄想级二型'
        if '想' in text:
            return True, 3, '妄想级'
        if '逆' in text:
            return True, 5, '逆戟鲸级'
        
        return False, -1, ''
    

    def OutHome(self):
        os.system(self.adb + f'shell input tap {869 + random.randint(2, 65)} {165 + random.randint(2, 20)}')


    def PutK(self):
        os.system(self.adb + 'shell input tap 20 89')
        time.sleep(4)
        os.system(self.adb + f'shell input tap {16 + random.randint(2, 170)} {70 + random.randint(2, 20)}')

        time.sleep(1)
        self.screenc()
        img = LoadImage(self.device_name, path)

        res = self.ocr.ocr(img)
        img.close()
        if res == []:
            return False
        for key in res:
            if '矿石舱' in key['text']:
                x = int(key['position'][0][0])
                y = int(key['position'][0][1])
                os.system(self.adb + f'shell input tap {str(x)} {str(y)}')
                break

        time.sleep(timer)
        os.system(self.adb + f'shell input tap {700 + random.randint(2, 60)} {460 + random.randint(2, 50)}')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {30 + random.randint(2, 150)} {90 + random.randint(2, 35)}')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {315 + random.randint(2, 185)} {100 + random.randint(2, 42)}')
        time.sleep(3)
        os.system(self.adb + 'shell input tap 924 30')
        return True


    def SetHomePoint(self):
        os.system(self.adb + 'shell input tap 927 302')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {20 + random.randint(2, 5)} 146')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {168 + random.randint(2, 35)} {490 + random.randint(2, 26)}')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {225 + random.randint(2, 148)} {237 + random.randint(2, 25)}')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {32 + random.randint(2, 96)} {218 + random.randint(2, 20)}')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {230 + random.randint(2, 138)} {180 + random.randint(2, 35)}')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {173 + random.randint(2, 28)} 189')


    def GoToKAreaUp(self, img: Image.Image, state):
        res = self.ocr.ocr(img)
        if res == []:
            return False, -1, ''

        css = []
        sts = []
        std = []
        for key in res:
            if '集群' in key['text']:
                x = int(key['position'][0][0])
                y = int(key['position'][0][1])
                css.append([x, y])
                continue
            if '星群' in key['text']:
                x = int(key['position'][0][0])
                y = int(key['position'][0][1])
                sts.append([x, y])
                continue
            if '星带' in key['text']:
                x = int(key['position'][0][0])
                y = int(key['position'][0][1])
                std.append([x, y])
                continue
        
        if css != []:
            if len(css) >= 2 and state:
                os.system(self.adb + f'shell input tap {str(css[1][0])} {str(css[1][1])}')
                return True, 1, '小行星集群'
            elif not state:
                os.system(self.adb + f'shell input tap {str(css[0][0])} {str(css[0][1])}')
                return True, 1, '小行星集群'
        if sts != []:
            if len(sts) >= 2 and state:
                os.system(self.adb + f'shell input tap {str(sts[1][0])} {str(sts[1][1])}')
                return True, 2, '小行星群'
            elif not state:
                os.system(self.adb + f'shell input tap {str(sts[0][0])} {str(sts[0][1])}')
                return True, 2, '小行星群'
        if std != []:
            if len(std) >= 2 and state:
                os.system(self.adb + f'shell input tap {str(std[1][0])} {str(std[1][1])}')
                return True, 3, '小行星带'
            elif not state:
                os.system(self.adb + f'shell input tap {str(std[0][0])} {str(std[0][1])}')
                return True, 3, '小行星带'
        
        return False, -1, ''
    

    def GoToKAreaDown(self, img: Image.Image):
        res = self.ocr.ocr(img)
        if res == []:
            return False

        for key in res:
            if '跃迁' in key['text']:
                x = int(key['position'][0][0])
                y = int(key['position'][0][1])
                os.system(self.adb + f'shell input tap {str(x)} {str(y)}')
                return True
        return False
    

    def RunK(self):
        '''
        : 接近矿石
        '''
        os.system(self.adb + f'shell input tap {740 + random.randint(2, 96)} 20')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {740 + random.randint(2, 148)} {448 + random.randint(2, 27)}')

        time.sleep(timer)
        os.system(self.adb + f'shell input tap {767 + random.randint(2, 126)} {50 + random.randint(2, 33)}')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {555 + random.randint(2, 145)} {110 + random.randint(2, 38)}')


    def ActHighCao(self, type: str):
        '''
        : 激活高槽
        '''
        os.system(self.adb + f'shell input tap 477 531')
        time.sleep(1)
        for lis in high_cao[self.device_name]:
            os.system(self.adb + f'shell input tap {lis[0]} {lis[1]}')
            time.sleep(0.5)
        if type == '逆戟鲸级':
            time.sleep(2)
            for lis in high_cao[self.device_name]:
                os.system(self.adb + f'shell input tap {lis[0]} {lis[1]}')
                time.sleep(0.5)


    def ToShipShow(self):
        '''
        : 总览切换至 舰船 标签
        '''
        os.system(self.adb + f'shell input tap {740 + random.randint(2, 96)} 20')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {742 + random.randint(2, 141)} {129 + random.randint(2, 35)}')


    def ToKShow(self):
        '''
        : 总览切换至 挖矿 标签
        '''
        os.system(self.adb + f'shell input tap {740 + random.randint(2, 96)} 20')
        time.sleep(timer)
        os.system(self.adb + f'shell input tap {746 + random.randint(2, 139)} {400 + random.randint(2, 30)}')


    def GoHome(self):
        os.system(self.adb + f'shell input tap {20 + random.randint(2, 5)} 146')


    def ActLowCao(self):
        '''
        : 激活低槽
        '''
        for lis in low_cao[self.device_name]:
            os.system(self.adb + f'shell input tap {lis[0]} {lis[1]}')
            time.sleep(0.5)


def Start(device_name, device_address, cnocr):
    des = ''
    is_waK = False
    is_station = True
    if_Max = 0
    listening = Listening(device_name, device_address, cnocr)
    command = Command(device_name, device_address, cnocr)
    # 检测本地红白、跑路
    # 在空间站内：检测舰船类型、离站、设置自动导航
    # 检测仓库满仓: 回家、放置矿石
    # 在矿区：检测蓝加拦截、接近矿石、激活高槽、总览切换至 舰船 列表
    # 在太空: 切换总览至 挖矿 、寻找矿区进入矿区、检测舰船状态、跃迁细节
    while True:
        time.sleep(conVal)
        listening.screenc()
        img = LoadImage(device_name, path)
        dtm = datetime.datetime.now()
        state = listening.LocalHaveEnemy(img)
        # 检测本地红白
        if state:
            if listening.IsAtSation(img):
                print(device_name, '检测到本地有人---------------', dtm)
                img.close()
                continue
            command.GoHome()
            command.ActLowCao()
            print(device_name, '检测到本地有人---------------', dtm)
            while True:
                # 检测舰船状态
                listening.screenc()
                img = LoadImage(device_name, path)
                if listening.IsAtSation(img):
                    is_station = True
                    img.close()
                    print(device_name, '进入空间站', dtm)
                    break
                img.close()
                time.sleep(1)
            img.close()
            continue

        # 在空间站内
        if is_station:
            is_waK = False
            listening.screenc()
            time.sleep(1)
            img = LoadImage(device_name, path)
            s, _, des1 = command.GetShipType()
            print(des1)
            des = des1
            if not s:
                img.close()
                print(device_name, f'{des}  该船型暂不支持, {device_name} 暂停运行', dtm)
                return
            
            command.OutHome()
            while True:
                # 检测是否已出站
                listening.screenc()
                img = LoadImage(device_name, path)
                if listening.IsInSpace(img):
                    is_station = False
                    img.close()
                    break
                img.close()
                time.sleep(1)
            # 已出站
            print(device_name, '已出站')
            # 设置自动导航
            time.sleep(3)

            command.SetHomePoint()
            img.close()
            continue

        # 仓库满仓
        if if_Max >= 1:
            if_Max = 0
            if not listening.IsMax(img):
                continue
            print(device_name, '仓库满仓')
            command.GoHome()
            command.ActLowCao()

            while True:
                # 检测是否已进站
                listening.screenc()
                img = LoadImage(device_name, path)
                if listening.IsAtSation(img):
                    is_station = True
                    img.close()
                    time.sleep(3)
                    # 放置矿石
                    print(device_name, '放置矿石')
                    command.PutK()
                    break
                img.close()
                time.sleep(1)
            img.close()
            continue
        if_Max += 1

        # 检测蓝加拦截舰船
        if listening.FindBlueFuckShip(img):
            command.GoHome()
            command.ActLowCao()

            while True:
                # 检测是否已进站
                listening.screenc()
                img = LoadImage(device_name, path)
                if listening.IsAtSation(img):
                    is_station = True
                    img.close()
                    print(device_name, '安全逃离----------', dtm)
                    print(device_name, '等待三分钟-----------', dtm)
                    time.sleep(90)
                    break
                time.sleep(1)
            img.close()
            continue

        # 在太空 & 挖矿  整合
        if listening.IsInSpace(img):
            # 整合     判断矿区消失
            if is_waK and listening.IsHaveKArea(img):
                img.close()
                continue
            print(device_name, '矿区消失')
            # 切换总览-挖矿
            command.ToKShow()
            # 寻找、进入矿区
            print(device_name, '寻找、进入矿区')
            time.sleep(2)
            listening.screenc()
            img = LoadImage(device_name, path)
            _, k_index, des33 = command.GoToKAreaUp(img, is_waK)
            img.close()
            is_waK = False
            print(des33)

            time.sleep(1)
            listening.screenc()
            img = LoadImage(device_name, path)
            st = command.GoToKAreaDown(img)
            img.close()
            if not st:
                continue
            while True:
                # 检测舰船状态
                listening.screenc()
                img = LoadImage(device_name, path)
                _, index, des2 = listening.GetShipState(img)
                img.close()
                print(device_name, '检测舰船状态', des2)
                if index == 4:
                    print(device_name, '已进入矿区')
                    break
                time.sleep(1)
            if not is_waK:
                # 接近矿石
                print(device_name, '接近矿石')
                command.RunK()
                # 激活高槽
                print(device_name, '激活高槽')
                command.ActHighCao(des)
                if k_index == 1 or k_index == 2:
                    print('正在接近矿石')
                    time.sleep(8)
                # 切换总览-舰船
                print(device_name, '切换总览-舰船')
                command.ToShipShow()
                is_waK = True
            img.close()
            continue


if __name__ == '__main__':
    cnocr = CnOcr(rec_model_name='densenet_lite_136-gru')
    for key, val in devices.items():
        t = threading.Thread(target=Start, args=(key, val, cnocr))
        t.start()
