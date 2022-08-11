from os import stat
from cnocr import CnOcr
import datetime

img_fp = './test6.png'
ocr = CnOcr(rec_model_name='densenet_lite_136-gru')
start = datetime.datetime.now()
out = ocr.ocr(img_fp)
end = datetime.datetime.now()
print(out)
print(end - start)
