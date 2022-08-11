import os
from xmlrpc.client import Boolean
from PIL import Image, ImageFile
from cnocr import CnOcr


path = 'C:/Users/sugob/Desktop/EVE_Get_MaNei'
devices = {'kuanggong1': '127.0.0.1:62001'}      # cmd输入adb devices查看模拟器地址


class Listening:
    def __init__(self, device_name: str, device_address: str, cnocr: CnOcr):
        self.device_name = device_name
        self.device_address = device_address

        self.ocr = cnocr

    
    def screenc(self):
        os.system(f'adb -s {self.device_address} exec-out screencap -p > {self.device_name}.png')


    def crop(self, x1, y1, x2, y2, scFileName):
        try:
            img = Image.open(scFileName)
            newimg = img.crop((x1, y1, x2, y2))
        except Exception:
            return
        return newimg


    def IsInSpace(self):
        '''
        : 判断是否在太空
        '''
        status = self.crop(453, 511, 508, 526, f'{path}/{self.device_name}.png')
        if not status:
            return False

        res = self.ocr.ocr(status)
        for keys in res:
            if '米' in keys['text'] or '秒' in keys['text']:
                return True
        return False


    def IsAtSation(self):
        '''
        : 判断是否在空间站
        '''
        status = self.crop(877, 163, 941, 194, f'{path}/{self.device_name}.png')
        if not status:
            return False

        res = self.ocr.ocr(status)
        for keys in res:
            key: str = keys['text']
            key = key.replace(" ", "")
            if '离站' in key:
                return True
        return False

    
    def IsAtKArea(self):
        '''
        : 判断是否在矿区
        '''
        if self.IsAtSation():
            return False

        status = self.crop(755, 51, 792, 84, f'{path}/{self.device_name}.png')
        if not status:
            return False

        res = self.ocr.ocr(status)
        if res == []:
            return False
        if '千米' in res[-1]['text']:
            if int(res[-1]['text']) <= 80:
                return True
        return False

    
    def GetShipState(self):
        '''
        : 判断舰船状态
        : state -> 1 -> 准备跃迁
        : state -> 2 -> 跃迁至
        : state -> 3 -> 即将到达
        '''
        if self.IsAtSation():
            return False

        status = self.crop(374, 394, 594, 414, f'{path}/{self.device_name}.png')
        if not status:
            return False

        res = self.ocr.ocr(status)
        if res == []:
            return False
        text = res[0]['text']
        if '准备跃迁' in text:
            return True, 1, '准备跃迁'
        if '跃迁至' in text:
            return True, 2, '跃迁至'
        if '即将到达' in text:
            return True, 3, '即将到达'
        return False
