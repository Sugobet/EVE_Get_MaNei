import imghdr
import os
import time
import datetime
from PIL import Image
import cv2
from cnocr import CnOcr


path = 'C:/Users/sugob/Desktop/EVE_Get_MaNei'
devices = {'kuanggong1': '127.0.0.1:62001'}      # cmd输入adb devices查看模拟器地址
M = {
    '第一槽位': [920, 438],
    '第二槽位': [868, 438],
    '第三槽位': [814, 438],
    '第四槽位': [924, 495],
    '第五槽位': [868, 495],
    '第六槽位': [914, 495],
    '第七槽位': [924, 495],
}
high_cao = [M['第一槽位'], M['第二槽位'], M['第三槽位']]
low_cao = [M['第四槽位'], M['第五槽位'], M['第六槽位'], M['第七槽位']]


def IF_Img_I(src, mp):
    # w, h = mp.shape[::2]
    res = None
    try:
        res = cv2.matchTemplate(src,mp,cv2.TM_CCOEFF_NORMED)
    except Exception:
        return False, 0.999
    _, mac_v, _, _ = cv2.minMaxLoc(res)
    if mac_v < 0.99:
        return True, mac_v
    return False, mac_v


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

    
    def IsAtKArea(self, img: Image.Image):
        '''
        : 判断是否在矿区
        '''
        if self.IsAtSation():
            return False

        status = self.crop(755, 51, 792, 84, img)
        if not status:
            return False

        res = self.ocr.ocr(status)
        if res == []:
            return False
        if '千米' in res[-1]['text']:
            try:
                if int(res[0]['text']) <= 80:
                    return True
            except Exception:
                return False
        return False


    def GetShipState(self, img: Image.Image):
        '''
        : 判断舰船状态
        : state -> 1 -> 准备跃迁
        : state -> 2 -> 跃迁至
        : state -> 3 -> 即将到达
        : state -> 4 -> 舰船正在停止
        '''
        if self.IsAtSation():
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
                tim = str(datetime.datetime.now())
                print(f'疑似蓝加拦截----------------{tim}')
                print(f'疑似蓝加拦截----------------{tim}')
                print(f'疑似蓝加拦截----------------{tim}')
                img.save(f'{path}/{self.device_name}_疑似蓝加拦截_{tim}.png')
                return True
        return False

    
    def IsMax(self, img: Image.Image):
        '''
        : 监测满仓
        '''
        status = self.crop(792, 51, 911, 316, img)
        if not status:
            return False, ''

        res = self.ocr.ocr(status)
        if res == []:
            return False
        try:
            if int(((res[0]['text']).replace('%', ''))) >= 95:
                return True
        except Exception:
            return False
        return False
    

    def LocalHaveEnemy(self, img: Image.Image):
        '''
        : 监测本地红白
        '''
        i1 = self.crop(0, 408, 188, 448, img)
        i2 = cv2.imread(f'{path}/tem/list.png')
        i1.save(f'{path}/{self.device_name}_list.png')
        i1 = cv2.imread(f'{path}/tem/{self.device_name}_list.png')
        list_status, _ = IF_Img_I(i1, i2)
        if list_status:
            return True
        return False
        


class Command:
    def __init__(self, device_address, cnocr: CnOcr):
        self.device_address = device_address
        self.ocr = cnocr

        self.adb = f'adb -s {self.device_address} '

    
    def crop(self, x1, y1, x2, y2, img) -> Image.Image:
        try:
            newimg = img.crop((x1, y1, x2, y2))
        except Exception:
            return
        return newimg


    def GetShipType(self, img: Image.Image):
        os.system(self.adb + 'shell input tap 46 21')
        time.sleep(0.5)
        os.system(self.adb + 'shell input tap 141 164')
        time.sleep(4)

        state = self.crop(4, 164, 186, 198, img)
        if not state:
            return False, -1, ''
        os.system(self.adb + 'shell input tap 924 31')

        res = self.ocr.ocr(state)
        if res == []:
            return False, -1, ''
        text = res[0]['text']
        if '回旋' in text:
            return True, 1, '回旋者级'
        if '猎获' in text:
            return True, 2, '猎获级'
        if '妄想' in text:
            return True, 3, '妄想级'
        if '妄想级二' in text:
            return True, 4, '妄想级二型'
        if '逆' in text:
            return True, 5, '逆戟鲸级'
        
        return False, -1, ''


    def PutK(self, img: Image.Image):
        os.system(self.adb + 'shell input tap 20 89')
        time.sleep(4)
        os.system(self.adb + 'shell input tap 86 77')

        res = self.ocr.ocr(img)
        if res == []:
            return False
        for key in res:
            if '矿石舱' in key['text']:
                x = int(key['position'][0][0])
                y = int(key['position'][0][1])
                os.system(self.adb + f'shell input tap {str(x)} {str(y)}')
                break

        time.sleep(0.3)
        os.system(self.adb + 'shell input tap 734 487')
        time.sleep(0.3)
        os.system(self.adb + 'shell input tap 105 112')
        time.sleep(0.3)
        os.system(self.adb + 'shell input tap 427 120')
        time.sleep(3)
        os.system(self.adb + 'shell input tap 924 31')
        return True


    def SetHomePoint(self):
        os.system(self.adb + 'shell input tap 21 146')
        time.sleep(0.3)
        os.system(self.adb + 'shell input tap 186 504')
        time.sleep(0.3)
        os.system(self.adb + 'shell input tap 302 258')
        time.sleep(0.3)
        os.system(self.adb + 'shell input tap 79 228')
        time.sleep(0.3)
        os.system(self.adb + 'shell input tap 301 199')
        time.sleep(0.3)
        os.system(self.adb + 'shell input tap 188 189')


    def GoToKAreaUp(self, img: Image.Image):
        os.system(self.adb + 'shell input tap 799 20')
        time.sleep(0.2)
        os.system(self.adb + 'shell input tap 817 414')
        time.sleep(0.2)
        os.system(self.adb + 'shell input tap 939 62')

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
            os.system(self.adb + f'shell input tap {str(css[0][0])} {str(css[0][1])}')
            return True, 1, '小行星集群'
        if sts != []:
            os.system(self.adb + f'shell input tap {str(sts[0][0])} {str(sts[0][1])}')
            return True, 2, '小行星群'
        if std != []:
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
        os.system(self.adb + 'shell input tap 937, 109')
        time.sleep(0.5)
        os.system(self.adb + 'shell input tap 824 65')
        time.sleep(0.5)
        os.system(self.adb + 'shell input tap 630 133')


    def ActHighCao(self):
        '''
        : 激活高槽
        '''
        for lis in high_cao:
            os.system(self.adb + f'shell input tap {lis[0]} {lis[1]}')
            time.sleep(0.5)


    def ToShipShow(self):
        '''
        : 总览切换至 舰船 标签
        '''
        os.system(self.adb + 'shell input tap 799 20')
        time.sleep(0.5)
        os.system(self.adb + 'shell input tap 808 146')


    def GoHome(self):
        os.system(self.adb + 'shell input tap 21 147')


    def ActLowCao(self):
        '''
        : 激活低槽
        '''
        for lis in low_cao:
            os.system(self.adb + f'shell input tap {lis[0]} {lis[1]}')
            time.sleep(0.05)
