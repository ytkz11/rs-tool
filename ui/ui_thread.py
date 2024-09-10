# from new_func.print_log import log
from PyQt5.QtCore import QThread, pyqtSignal


class Worker(QThread):

    finished = pyqtSignal()  # 定义一个无参数的信号

    def __init__(self, func):
        super(Worker, self).__init__()
        self.func = func

    def run(self):
        try:
            self.func()  # 执行你的任务
        finally:
            self.finished.emit()  # 发射结束信号
            print(f"{self.func.__name__}线程启动并完成任务")


    def stop(self):
        # 停止线程的方法
        self.quit()
        self.wait()
        print(f"{self.func}线程结束")

from PyQt5.QtCore import QThread, pyqtSignal

