#!/usr/bin/env python
# !encoding=utf-8

import sys, os, time, atexit, string, ConfigParser, commands, subprocess
from signal import SIGTERM

PID_FILE = "./SqyDaemon.pid"
CONFIG_FILE = "SqyDaemon.ini"
SECTION = "Monitor"
SECTION_KEY = "Process"


class Daemon:
    def __init__(self, configFile, pidfile):
        self.pidfile = pidfile
        self.configFile = configFile
        cfg = ConfigParser.ConfigParser()
        try:
            cfg.read(self.configFile)
            allprocesses = cfg.get(SECTION, SECTION_KEY)
            if '#' in allprocesses:
                position1 = allprocesses.find('#')
                self.processes = allprocesses[:position1]
            else:
                self.processes = allprocesses
            self.processes = self.processes.strip()
            self.monitorProcess = self.processes.split(',')
        except Exception, e:
            print e

    def _daemonize(self):
        try:
            pid = os.fork()

            if pid > 0:
                sys.exit(0)  # 退出主进程
        except OSError, e:
            print "fork failed!\nError is:", e.strerror
            sys.exit(1)
        os.setsid()
        os.umask(0)
        # 创建子进程
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            print "fork failed!\nError is:", e.strerror
            sys.exit(1)
            # 创建processid文件
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write('%s\n' % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        # 检查pid文件是否存在以探测是否存在进程
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if pid:
            print "pidfile %s already exist. SqyDaemon already running?\n" % self.pidfile
            sys.exit(1)
            # 启动监控
        self._daemonize()
        self._run()

    def stop(self):
        # 从pid文件中获取pid
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None
        if not pid:
            if "-r" == sys.argv[1]:
                print "SqyDaemon restart and monitor related process!"
            else:
                message = 'pidfile %s does not exist. SqyDaemon not running?\n'
                sys.stderr.write(message % self.pidfile)
            return  # 重启不报错
        elif "-r" == sys.argv[1]:
            print "%s is runing,now restart!" % sys.argv[0]
        elif "-k" == sys.argv[1]:
            print "all processes are killed!"
            # 杀进程
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
                for tmpprocees in self.monitorProcess:
                    processname = os.path.basename(tmpprocees)
                    os.system("killall %s" % processname)
        except OSError, err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def _run(self):
        while True:
            for tmpprocees in self.monitorProcess:
                processname = os.path.basename(tmpprocees)
                fullpath = os.path.abspath(tmpprocees)
                count = commands.getoutput("ps -elf | grep %s | grep -v %s | wc -l" % (processname, "grep"))
                if 0 == int(count):
                    os.system(tmpprocees + " 1>/dev/null 2>/dev/null &")  # 标准输出和错误输出重定向到/dev/null
                else:
                    continue
            time.sleep(2)


def help():
    print "Usage:"
    print "%s -m            ---monitor all processes" % sys.argv[0]
    print "%s -k            ---kill all processes" % sys.argv[0]
    print "%s -r            ---restart all processes" % sys.argv[0]


if __name__ == '__main__':
    daemon = Daemon(CONFIG_FILE, PID_FILE)
    if len(sys.argv) == 2:
        if '-m' == sys.argv[1]:
            daemon.start()
        elif '-k' == sys.argv[1]:
            daemon.stop()
        elif '-r' == sys.argv[1]:
            daemon.restart()
        else:
            print 'Unknown command'
            help()
            sys.exit(2)
        sys.exit(0)
    else:
        help()
        sys.exit(2)