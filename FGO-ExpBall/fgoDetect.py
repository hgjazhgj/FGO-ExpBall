import cv2
import numpy
import os
import time
from fgoLogging import getLogger,logMeta,logit
from fgoFuse import fuse
from fgoSchedule import schedule

logger=getLogger('Detect')


class Button:
    device=None
    def __init__(self,center,img=None,size=(0,0),threshold=.08,padding=2):
        self.center=center
        if img is not None:
            img=cv2.imread(f'fgoImage/{img}.png')
            self.img=img[center[1]-size[1]:center[1]+size[1],
                         center[0]-size[0]:center[0]+size[0]]
            self.threshold=threshold
            self.slice=(slice(center[1]-size[1]-padding,center[1]+size[1]+padding),
                        slice(center[0]-size[0]-padding,center[0]+size[0]+padding))

    def wait(self,afterDelay=.5,interval=.2):
        while not self.appear(interval):pass
        schedule.sleep(afterDelay)
        return self

    def appear(self,afterDelay=0):
        screen=self.device.screenshot()
        schedule.sleep(afterDelay)
        # logger.debug(numpy.min(cv2.matchTemplate(screen[self.slice],self.img,cv2.TM_SQDIFF_NORMED)))
        if numpy.min(cv2.matchTemplate(screen[self.slice],self.img,cv2.TM_SQDIFF_NORMED))<self.threshold:
            fuse.reset()
            return True
        else:
            fuse.increase()
            return False

    def click(self,afterDelay=0):
        self.device.touch(self.center)
        schedule.sleep(afterDelay)
        return self

    def offset(self,x,y):
        result=Button((self.center[0]+x,self.center[1]+y))
        result.img=self.img
        result.threshold=self.threshold
        result.slice=(slice(self.slice[0].start+y,self.slice[0].stop+y),
                      slice(self.slice[1].start+x,self.slice[1].stop+x))
        return result

SPACE=Button((1231,687))
BACK=Button((38,43),'summon_continue',(10,10))
MAIN_MAIN=Button((137,596))
MAIN_ARCHIVE=Button((304,596))
MAIN_SYNTHESIS=Button((472,596))
MAIN_SUMMON=Button((640,596),'main',(25,25))
SUMMON_FP=Button((672,42),'summon_continue',(15,15))
SUMMON_SWITCH=Button((45,360))
SUMMON_SUMMON=Button((733,526))
SUMMON_SUBMIT=Button((837,564),'summon_submit',(27,14))
SUMMON_CONTINUE=Button((762,673),'summon_continue',(104,14))
SUMMON_SALE=Button((345,477),'summon_sale',(27,14))
SELECT_SERVANT=Button((101,128))
SELECT_REISOU=Button((288,128))
SELECT_CODE=Button((475,128))
SELECT_GIRD=Button((28,677),'sort',(21,21))
SELECT_FINISH=Button((1153,673),'lock',(27,12))
SELECT_LOCK=Button((74,246),'lock',(6,8),.13,4)
FILTER_EVENT=Button((804,130),'lock',(80,18))
FILTER_FILTER=Button((980,130))
FILTER_STAR_3=Button((642,235))
FILTER_STAR_2=Button((831,235))
FILTER_STAR_1=Button((1019,235))
FILTER_SCROLL=Button((1135,565))
FILTER_EXP=Button((639,385))
FILTER_FOU=Button((852,385))
FILTER_RESET=Button((227,641))
FILTER_SUBMIT=Button((1054,638),'filter',(20,65))
FILTER_CANCEL=Button((820,638))
SORT_SORT=Button((1128,130))
SORT_DEC=Button((1248,132),'sort',(15,12))
SORT_BYTIME=Button((742,384))
SORT_BYLEVEL=Button((318,232))
SORT_BYRANK=Button((430,322))
SORT_FILTER_ON=Button((578,474),'sort',(12,12))
SORT_SUBMIT=Button((853,638))
SELL_RESULT=Button((640,629),'result',(40,20))
SYNTHESIS_SYNTHESIS=Button((958,474))
SYNTHESIS_LOAD=Button((195,382),'synthesis',(80,80))
SYNTHESIS_SELECT=Button((30,240))
SYNTHESIS_LOCK=Button((30,354))
SYNTHESIS_ENTER=Button((864,242))
ARCHIVE_ARCHIVE=Button((958,627))
ARCHIVE_SUBMIT=Button((836,602))
ARCHIVE_RESULT=Button((637,602))

SPECIAL=[(i[:-4],cv2.imread(f'fgoImage/special/{i}'))for i in os.listdir('fgoImage/special') if i.endswith('.png')]
class Detect(metaclass=logMeta(logger)):
    cache=None
    screenshot=None
    def __init__(self):
        self.im=self.screenshot()
        Detect.cache=self
        self.time=time.time()
        fuse.increase()
    def _crop(self,rect):
        return self.im[rect[1]:rect[3],rect[0]:rect[2]]
    # @logit(logger)
    def _loc(self,img,rect=(0,0,1280,720)):return cv2.minMaxLoc(cv2.matchTemplate(self._crop(rect),img,cv2.TM_SQDIFF_NORMED))
    def _find(self,img,rect=(0,0,1280,720),threshold=.03):return(lambda loc:((rect[0]+loc[2][0]+(img.shape[1]>>1),rect[1]+loc[2][1]+(img.shape[0]>>1)),fuse.reset(self))[0]if loc[0]<threshold else None)(self._loc(img,rect))
    def _count(self,img,rect=(0,0,1280,720),threshold=.03):return cv2.connectedComponents((cv2.matchTemplate(self._crop(rect),img,cv2.TM_SQDIFF_NORMED)<threshold).astype(numpy.uint8))[0]-1
    def save(self,name='Capture',rect=(0,0,1280,720),appendTime=True):return cv2.imwrite(name:=time.strftime(f'{name}{f"_%Y-%m-%d_%H.%M.%S.{round(self.time*1000)%1000:03}"if appendTime else""}.png',time.localtime(self.time)),self._crop(rect),[cv2.IMWRITE_PNG_COMPRESSION,9])and name

    def findSpecial(self):
        for i,j in SPECIAL:
            if t:=self._find(j,(82,184,1202,592)):
                return i,t
    def countSpecial(self):
        return sum(self._count(i,(82,184,1202,592))for i in SPECIAL)
