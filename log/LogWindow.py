import os
import threading
import time
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QWidget, QApplication, QPushButton

from log.Logger import Logger
from tools.Tools import Tools


class LogWindow(QMainWindow, Logger):
    """
        日志窗口
    """
    # 类变量用于保存单例实例
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        if not hasattr(self, 'log_text'):
            self.log_text = None
            self.config = None
            self.reload_recoils_config_button = None
            self.recoils_config = None
            self.log_queue = Tools.GetBlockQueue(name='log_queue', maxsize=1000)
            self.init_ui()
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            threading.Thread(target=self.consume_log).start()
        self.show()

    def set_config(self, config):
        """
            设置全局配置类
        :param config:
        """
        self.config = config

    def set_recoils_config(self, recoils_config):
        """
            设置压枪数据配置类
        :param recoils_config:
        """
        self.recoils_config = recoils_config

    def init_ui(self):
        """
            初始化UI
        """
        self.setWindowTitle("Apex gun")
        self.setGeometry(100, 100, 600, 300)

        self.reload_recoils_config_button = QPushButton('重新加载压枪数据', self)
        self.reload_recoils_config_button.clicked.connect(self.reload_recoils_config)
        # 创建 QTextEdit 组件用于显示日志
        self.log_text = QTextEdit()
        self.log_text.document().setMaximumBlockCount(1000)
        self.log_text.setReadOnly(True)

        # 添加 QTextEdit 组件到主窗口
        layout = QVBoxLayout()
        layout.addWidget(self.reload_recoils_config_button)
        layout.addWidget(self.log_text)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def reload_recoils_config(self):
        """
            重新加载压枪数据
        """
        if self.recoils_config is not None:
            self.recoils_config.load()

    def print_log(self, log):
        """
            打印日志
        :param log:
        """
        self.log_queue.put(log)

    def closeEvent(self, event):
        """
            关闭事件
        :param event:
        """
        self.config.save_config()
        QApplication.quit()
        os._exit(0)

    def consume_log(self):
        """
            避免多线程影响ui，在一个线程中启动队列消费打印
        """
        self.real_print("打印日志线程启动")
        while True:
            try:
                log = self.log_queue.get()
                self.real_print(log)
            except Exception as e:
                print(e)
                traceback.print_exc()
                time.sleep(0.1)

    def real_print(self, log):
        """
            真实打印函数
        :param log:
        """
        self.log_text.append(log)
        self.log_text.moveCursor(self.log_text.textCursor().End)
        super().print_log(text=log)
