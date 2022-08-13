from fgoConst import *
from fgoDetect import *
from fgoLogging import getLogger
from fgoSchedule import schedule,ScriptStop
logger=getLogger('Kernel')

class ExpBall:
    def __init__(self,appoint=0):
        self.runOnce=True
        self.appoint=appoint

    def __call__(self):
        while True:
            SPACE.click(.5)
            if MAIN_SUMMON.appear():
                MAIN_SUMMON.click(5)
                BACK.wait(1)
            else:
                SPACE.click(.8)
            while not SUMMON_FP.appear():
                SUMMON_SWITCH.click(2.5)
            logger.info('FP summon')
            SUMMON_SUMMON.click(.8)
            while not SUMMON_SALE.appear():
                SUMMON_SUBMIT.click(3)
                while not SUMMON_CONTINUE.appear():
                    SPACE.click(.4)
                if t:=Detect().findSpecial():
                    Detect.cache.save()
                    if Detect.cache.countSpecial()>1:
                        raise ScriptStop('Lot of Special Summoned')
                    logger.warning('Special Summoned')
                    Button(t).click(2)
                    Button((32,180)).click(1)
                    BACK.click(1.5)
                SUMMON_CONTINUE.click(.8)
            logger.info('FP summon finished')
            SUMMON_SALE.click(4)
            SELECT_FINISH.wait(1)
            SELECT_SERVANT.click(2)
            logger.info('sell servant')
            if self.runOnce: # 每行7个 获得顺序 智能筛选
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                SORT_SORT.click(.8)
                SORT_BYTIME.click(.5)
                while not SORT_FILTER_ON.appear():
                    SORT_FILTER_ON.click(.8)
                SORT_SUBMIT.click(.8)
            self.sell()
            logger.info('sell servant finished')
            SELECT_REISOU.click(2)
            logger.info('sell reisou')
            if self.runOnce: # 每行7个 3星 智能筛选
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                FILTER_FILTER.click(.8)
                FILTER_RESET.click(.5)
                FILTER_STAR_3.click(.5)
                FILTER_SUBMIT.click(.8)
                SORT_SORT.click(.8)
                while not SORT_FILTER_ON.appear():
                    SORT_FILTER_ON.click(.8)
                SORT_SUBMIT.click(.8)
            self.sell()
            logger.info('sell reisou finished')
            SELECT_CODE.click(2)
            logger.info('sell command code')
            if self.runOnce: # 每行7个 12星
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                FILTER_FILTER.click(.8)
                FILTER_RESET.click(.5)
                FILTER_STAR_1.click(.5)
                FILTER_STAR_2.click(.5)
                FILTER_SUBMIT.click(.8)
            self.sell()
            logger.info('sell command code finished')
            BACK.click(3)
            SPACE.click(.5)
            MAIN_SYNTHESIS.click(4)
            SYNTHESIS_BEGIN.click(3)
            logger.info('reisou select')
            SYNTHESIS_LOAD.wait().click(3)
            if self.runOnce: # 每行7个 1星 等级顺序 智能筛选 降序
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                FILTER_FILTER.click(.8)
                FILTER_RESET.click(.5)
                FILTER_STAR_1.click(.5)
                FILTER_SUBMIT.click(.8)
                SORT_SORT.click(.8)
                SORT_BYLEVEL.click(.5)
                while not SORT_FILTER_ON.appear():
                    SORT_FILTER_ON.click(.8)
                SORT_SUBMIT.click(.8)
                while SORT_INC.appear():
                    SORT_INC.click(.8)
            if not SELECT_LOCK.appear():
                SYNTHESIS_LOCK.click(1)
                SELECT_LOCK.offset((60,0)).click(1)
                SYNTHESIS_SELECT.click(1)
            SELECT_LOCK.offset((60,0)).click(1.5)
            BACK.wait(.5)
            logger.info('reisou synthesis')
            SYNTHESIS_ENTER.click(1)
            SELECT_FINISH.wait(1)
            if self.runOnce: # 每行7个 12星 稀有度顺序 智能筛选 降序
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                FILTER_FILTER.click(.8)
                FILTER_RESET.click(.5)
                FILTER_STAR_1.click(.5)
                FILTER_STAR_2.click(.5)
                FILTER_SUBMIT.click(.8)
                SORT_SORT.click(.8)
                SORT_BYRANK.click(.5)
                while not SORT_FILTER_ON.appear():
                    SORT_FILTER_ON.click(.8)
                SORT_SUBMIT.click(.8)
                while SORT_INC.appear():
                    SORT_INC.click(.8)
            while True:
                self.selectAll()
                if SELECT_FINISH.appear():
                    break
                SELECT_FINISH.click(1)
                SELECT_FINISH.click(.5)
                SUMMON_SUBMIT.click(2)
                while not BACK.appear():
                    SPACE.click(.2)
                if SYNTHESIS_LOAD.appear():
                    logger.warning('ExpBall Created')
                    break
                SYNTHESIS_ENTER.click(1)
                SELECT_FINISH.wait(1)
            logger.info('reisou synthesis finished')
            BACK.click(1).click(2).wait()
            self.appoint-=1
            if not self.appoint:
                break
            self.runOnce=False

    def selectAll(self):
        for i in range(4):
            for j in range(7):
                Button((133+133*j,253+140*i)).click(.15)
        schedule.sleep(1)

    def sell(self):
        while True:
            self.selectAll()
            if SELECT_FINISH.appear():
                break
            SELECT_FINISH.click(1)
            SORT_SUBMIT.click(1)
            SELL_RESULT.click(1)
            SELECT_FINISH.wait(1)
