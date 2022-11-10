from fgoConst import *
from fgoDetect import *
from fgoLogging import getLogger
from fgoSchedule import schedule,ScriptStop
logger=getLogger('Kernel')

class ExpBall:
    def __init__(self,appoint=0,special=None):
        self.runOnce=True
        self.appoint=appoint
        self.special={}if special is None else special

    def __call__(self):
        while True:
            logger.info('FP summon')
            SPACE.click(.5)
            if MAIN_SUMMON.appear():
                MAIN_SUMMON.click(5)
                BACK.wait()
            else:
                SPACE.click(.8)
            while not SUMMON_FP.appear():
                SUMMON_SWITCH.click(1.5)
            SUMMON_SUMMON.click(.8)
            while not SUMMON_SALE.appear():
                SUMMON_SUBMIT.click(3)
                while not SUMMON_CONTINUE.appear():
                    SPACE.click(.4)
                if t:=Detect().findSpecial():
                    Detect.cache.save('fgoLog/Special')
                    if Detect.cache.countSpecial()>1:
                        raise ScriptStop('Lot of Special Summoned')
                    logger.warning(f'Special Summoned {t[0]}')
                    if self.special.setdefault(t[0],0)==1:
                        raise ScriptStop(f'Special Summoned {t[0]} count achieved')
                    self.special[t[0]]-=1
                    Button(t[1]).click(2)
                    Button((32,180)).click(1)
                    BACK.click(1.5)
                SUMMON_CONTINUE.click(.8)
            logger.info('Sell servant')
            SUMMON_SALE.click(3)
            SELECT_FINISH.wait()
            SELECT_SERVANT.click(2)
            if self.runOnce: # 每行7个 获得顺序 智能筛选
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                SORT_SORT.click(.8)
                SORT_BYTIME.click(.5)
                while not SORT_FILTER_ON.appear():
                    SORT_FILTER_ON.click(.8)
                SORT_SUBMIT.click(.8)
            self.sell()
            logger.info('Sell reisou')
            SELECT_REISOU.click(2)
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
            logger.info('Sell command code')
            SELECT_CODE.click(2)
            if self.runOnce: # 每行7个 12星
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                FILTER_FILTER.click(.8)
                FILTER_RESET.click(.5)
                FILTER_STAR_1.click(.5)
                FILTER_STAR_2.click(.5)
                FILTER_SUBMIT.click(.8)
            self.sell()
            BACK.click(3)
            logger.info('Reisou select')
            SPACE.click(.5)
            MAIN_SYNTHESIS.click(3)
            BACK.wait()
            SYNTHESIS_SYNTHESIS.click(3)
            SYNTHESIS_LOAD.wait().click(3)
            if self.runOnce: # 每行7个 全部 1星 等级顺序 智能筛选 降序
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                while FILTER_EVENT.appear():
                    FILTER_EVENT.click(.8)
                FILTER_FILTER.click(.8)
                FILTER_RESET.click(.5)
                FILTER_STAR_1.click(.5)
                FILTER_SUBMIT.click(.8)
                SORT_SORT.click(.8)
                SORT_BYLEVEL.click(.5)
                while not SORT_FILTER_ON.appear():
                    SORT_FILTER_ON.click(.8)
                SORT_SUBMIT.click(.8)
                while not SORT_DEC.appear():
                    SORT_DEC.click(.8)
            for i,j in((i,j)for i in range(4)for j in range(7)):
                if not SELECT_LOCK.offset(133*j,142*i).appear():
                    SYNTHESIS_LOCK.click(1)
                    SELECT_LOCK.offset(133*j,142*i).offset(60,0).click(1)
                    SYNTHESIS_SELECT.click(1)
                SELECT_LOCK.offset(133*j,142*i).offset(60,0).click(1.5)
                BACK.wait()
                if not SORT_DEC.appear():
                    break
            else:
                raise ScriptStop('No Synthesis Material')
            logger.info('Reisou synthesis')
            SYNTHESIS_ENTER.click(1)
            SELECT_FINISH.wait()
            if self.runOnce: # 每行7个 全部 12星 稀有度顺序 智能筛选 降序
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                while FILTER_EVENT.appear():
                    FILTER_EVENT.click(.8)
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
                while not SORT_DEC.appear():
                    SORT_DEC.click(.8)
            while True:
                self.selectAll()
                if SELECT_FINISH.appear():
                    break
                SELECT_FINISH.click(1)
                SELECT_FINISH.click(.5)
                SUMMON_SUBMIT.click(2)
                while not BACK.appear():
                    SPACE.click(.4)
                if SYNTHESIS_LOAD.appear():
                    logger.warning('ExpBall Created')
                    break
                SYNTHESIS_ENTER.click(1)
                SELECT_FINISH.wait()
            BACK.click(1).wait().click(1).wait()
            logger.info('Archive')
            SPACE.click(.5)
            MAIN_ARCHIVE.click(3)
            BACK.wait()
            ARCHIVE_ARCHIVE.click(3)
            SELECT_FINISH.wait()
            if self.runOnce: # 每行7个 经验值 芙芙
                while not SELECT_GIRD.appear():
                    SELECT_GIRD.click(2)
                FILTER_FILTER.click(.8)
                FILTER_RESET.click(.5)
                FILTER_SCROLL.click(.5)
                FILTER_EXP.click(.5)
                FILTER_FOU.click(.5)
                FILTER_SUBMIT.click(.8)
            while True:
                self.selectAll()
                if SELECT_FINISH.appear():
                    break
                SELECT_FINISH.click(1)
                ARCHIVE_SUBMIT.click(2)
                SELECT_FINISH.wait()
                ARCHIVE_RESULT.click(1)
            BACK.click(1).wait()
            logger.info('Garbage Collection')
            SPACE.click(.5)
            MAIN_MAIN.click(6)
            BACK.wait(4)
            self.appoint-=1
            logger.info(f'Cycle left {"infinity"if self.appoint<0 else self.appoint}')
            if not self.appoint:
                break
            self.runOnce=False
        logger.warning('Done')

    def selectAll(self):
        for i,j in((i,j)for i in range(4)for j in range(7)):
            Button((133+133*j,253+142*i)).click(.15)
        schedule.sleep(1)

    def sell(self):
        while True:
            self.selectAll()
            if SELECT_FINISH.appear():
                break
            SELECT_FINISH.click(1)
            SORT_SUBMIT.click(1)
            SELL_RESULT.wait().click(1)
            SELECT_FINISH.wait()
