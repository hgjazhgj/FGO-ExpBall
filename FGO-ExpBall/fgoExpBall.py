import argparse,cmd,functools,os,platform,re,signal,time
import fgoDevice
from fgoConst import VERSION
import fgoLogging
from fgoFuse import fuse
import fgoKernel
from fgoSchedule import ScriptStop,schedule
logger=fgoLogging.getLogger('Cli')

def wrapTry(func):
    @functools.wraps(func)
    def wrapper(self,*args,**kwargs):
        try:return func(self,*args,**kwargs)
        except ArgError as e:
            if e.args[0]is not None:logger.error(e)
        except KeyboardInterrupt:logger.critical('KeyboardInterrupt')
        except BaseException as e:logger.exception(e)
        finally:self.prompt=f'FGO-ExpBall@{fgoDevice.device.name}> '
    return wrapper
def countdown(x):
    timer=time.time()+x
    while(rest:=timer-time.time())>0:
        print((lambda sec:f'{sec//3600:02}:{sec%3600//60:02}:{sec%60:02}')(round(rest)),end=' \r')
        time.sleep(min(1,max(0,rest)))

class Cmd(cmd.Cmd,metaclass=lambda name,bases,attrs:type(name,bases,{i:wrapTry(j)if i.startswith('do_')else j for i,j in attrs.items()})):
    intro=f'''
FGO-ExpBall {VERSION}, Copyright (c) 2019-2022 hgjazhgj

Connect device first, then type main to make ExpBall.
Type help or ? to list commands, help <command> to get more information.
Some commands support <command> [<subcommand> ...] {{-h, --help}} for further information.
'''
    prompt='FGO-ExpBall@Device> '
    def __init__(self):
        super().__init__()
        fgoDevice.Device.enumDevices()
    def emptyline(self):return
    def precmd(self,line):
        if line:logger.info(line)
        return line
    def completenames(self,text,*ignored):return[f'{i} 'for i in super().completenames(text,*ignored)]
    def completecommands(self,table,text,line,begidx,endidx):return sum([[f'{k} 'for k in j if k.startswith(text)]for i,j in table.items()if re.match(f'{i}$',' '.join(line.split()[1:None if begidx==endidx else -1]))],[])
    def do_exec(self,line):exec(line)
    def do_shell(self,line):os.system(line)
    def do_exit(self,line):
        'Exit FGO-ExpBall'
        return True
    def do_EOF(self,line):return self.do_exit(line)
    def do_version(self,line):
        'Show FGO-ExpBall version'
        print(VERSION)
    def do_connect(self,line):
        'Connect to a device'
        arg=parser_connect.parse_args(line.split())
        if arg.list:return print(*fgoDevice.Device.enumDevices(),sep='\n')
        fgoDevice.device=fgoDevice.Device(arg.name)
    def complete_connect(self,text,line,begidx,endidx):
        return self.completecommands({
            '':['wsa','win']+[f'/{i}'for i in fgoDevice.helpers]+fgoDevice.Device.enumDevices()
        },text,line,begidx,endidx)
    def do_main(self,line):
        'Make several ExpBalls endlessly'
        arg=parser_main.parse_args(line.split())
        self.work=fgoKernel.ExpBall(arg.appoint,dict(arg.count))
        self.do_continue(f'-s {arg.sleep}')
    def do_continue(self,line):
        'Continue execution after abnormal break'
        arg=parser_main.parse_args(line.split())
        assert fgoDevice.device.available
        countdown(arg.sleep)
        try:
            signal.signal(signal.SIGINT,lambda*_:schedule.stop())
            if platform.system()=='Windows':signal.signal(signal.SIGBREAK,lambda*_:schedule.pause())
            self.work()
        except ScriptStop as e:
            logger.critical(e)
        except KeyboardInterrupt:
            raise
        except BaseException as e:
            logger.exception(e)
        finally:
            signal.signal(signal.SIGINT,signal.SIG_DFL)
            if platform.system()=='Windows':signal.signal(signal.SIGBREAK,signal.SIG_DFL)
            fuse.reset()
            schedule.reset()
    def do_screenshot(self,line):
        'Take a screenshot'
        assert fgoDevice.device.available
        fgoKernel.Detect(0).save()
    def do_169(self,line):
        'Adapt none 16:9 screen'
        arg=parser_169.parse_args(line.split())
        assert fgoDevice.device.available
        getattr(fgoDevice.device,f'{arg.action}169')()
    def complete_169(self,text,line,begidx,endidx):
        return self.completecommands({
            '':['invoke','revoke']
        },text,line,begidx,endidx)

ArgError=type('ArgError',(Exception,),{})
def validator(type,func,desc='\b'):
    def f(x):
        if not func(x:=type(x)):raise ValueError
        return x
    f.__name__=desc
    return f
class ArgParser(argparse.ArgumentParser):
    def exit(self,status=0,message=None):raise ArgError(message)
class ArgStruct:
    def __init__(self,*args):
        def infIter(iterable):
            while True:yield from iterable
        self.it=infIter(args)
        self.repr=f'{type(self).__name__}{args}'
    def __call__(self,x):
        return next(self.it)(x)
    def __repr__(self):
        return self.repr

parser_main=ArgParser(prog='main',description=Cmd.do_main.__doc__)
parser_main.add_argument('-s','--sleep',help='Sleep before run (default: %(default)s)',type=validator(float,lambda x:x>=0,'nonnegative'),default=0)
parser_main.add_argument('-a','--appoint',help='Cycle limit (default: %(default)s for no limit)',type=validator(int,lambda x:x>=0,'nonnegative int'),default=0)
parser_main.add_argument('-c','--count',help='Stop after Special Drop count',action='append',type=ArgStruct(str,validator(int,lambda x:x>0,'positive int')),default=[],nargs=2)

parser_connect=ArgParser(prog='connect',description=Cmd.do_connect.__doc__)
parser_connect.add_argument('-l','--list',help='List all available devices',action='store_true')
parser_connect.add_argument('name',help='Device name (default to the last connected one)',default='',nargs='?')

parser_169=ArgParser(prog='169',description=Cmd.do_169.__doc__)
parser_169.add_argument('action',help='Action',type=str.lower,choices=['invoke','revoke'])

def main(args):Cmd().cmdloop()

if __name__=='__main__':
    # fgoLogging.logging.getLogger('fgo').handlers[-1].setLevel('DEBUG')
    main([])
