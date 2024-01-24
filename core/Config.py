import os
import os.path as op
import json
import shutil
import jsonpath as jsonpath

from tools.Tools import Tools
from log.Logger import Logger

screenshot_resolution = {
    (1920, 1080): (1542, 959, 1695, 996),
    (2560, 1440): (2093, 1281, 2275, 1332),
    # (2560, 1440): (1905, 1092, 2087, 1143),
    (3440, 1440): (2093, 1281, 2275, 1332),
    (1920, 1200): (1539, 1142, 1728, 1142),
    (2048, 1152): (1927, 1172, 2089, 1208)
}


class Config:
    """
        全局配置
    """

    def __init__(self, logger: Logger,
                 base_path='config\\',
                 ref_dir='ref\\',
                 use_ref_name='ref.txt',
                 default_ref_config_name='global_config'):

        self.base_path = None
        self.ref_dir = None
        self.ref_config_name = None
        self.use_ref_name = None
        self.config_path = None
        self.config_data = None

        self.desktop_width = None
        self.desktop_height = None
        self.game_width = None
        self.game_height = None
        self.refresh_buttons = []
        self.mouse_mover = None
        self.log_model = None
        self.game_solution = None
        self.mouse_mover_params = None
        self.select_gun_bbox = None
        self.image_path = None
        self.shake_gun_toggle = None

        self.logger = logger
        self.update(base_path, ref_dir, use_ref_name, default_ref_config_name)

    def update(self,
               base_path='config\\',
               ref_dir='ref\\',
               use_ref_name='ref.txt',
               default_ref_config_name='global_config'):
        """
            重新做一次初始化操作，复用init
        :param base_path:
        :param ref_dir:
        :param use_ref_name:
        :param default_ref_config_name:
        """
        self.base_path = base_path
        self.ref_dir = self.base_path + ref_dir
        self.ref_config_name = default_ref_config_name
        self.use_ref_name = use_ref_name
        self.config_data = self.read_config()
        self.init()

    def init(self):
        """
            配置初始化
        """

        x, y = Tools.get_resolution()
        # 分辨率
        self.desktop_width = self.get_config(self.config_data, 'desktop_width', x)
        self.desktop_height = self.get_config(self.config_data, 'desktop_height', y)
        self.logger.print_log(f"识别到桌面分辨率为:{self.desktop_width}x{self.desktop_height}")

        self.game_width = self.get_config(self.config_data, 'screen_width', self.desktop_width)
        self.game_height = self.get_config(self.config_data, 'screen_height',
                                           self.desktop_height)

        self.game_solution = (self.game_width, self.game_height)
        if self.game_solution in screenshot_resolution:
            self.select_gun_bbox = screenshot_resolution[
                self.game_solution]  # 选择枪械的区域
        else:
            self.select_gun_bbox = screenshot_resolution[(1920, 1080)]
        self.image_path = 'images/' + '{}x{}/'.format(*self.game_solution)  # 枪械图片路径

        self.refresh_buttons = self.get_config(self.config_data, 'refresh_buttons', ['1', '2', 'E'])

        self.mouse_mover = self.get_config(self.config_data, "mouse_mover", "win32api")
        self.mouse_mover_params = self.get_config(self.config_data, "mouse_mover_params", {
            "win32api": {},
            "km_box": {
                "VID/PID": "66882021"
            },
            "wu_ya": {
                "VID/PID": "26121701"
            }
        })
        self.log_model = self.get_config(self.config_data, "log_model", "window")
        self.shake_gun_toggle = self.get_config(self.config_data, "shake_gun_toggle", True)

    def get_config(self, read_config, pattern=None, default=None):
        """
            从配置中获取项值
        :param read_config:
        :param pattern:
        :param default:
        :return:
        """
        if pattern is not None:
            value = jsonpath.jsonpath(read_config, pattern)
            if value is None or not value:
                if default is not None:
                    read_config[pattern] = default
                    return default
                else:
                    return False
            if isinstance(value, list) and len(value) == 1:
                return value[0]
            else:
                return value
        else:
            return read_config

    def set_config(self, key, value):
        """
            配置选项变更
        :param key:
        :param value:
        """
        self.config_data[key] = value

    def save_config(self):
        """
            保存配置
        """
        with open(self.config_path, "w", encoding="utf8") as f:
            json.dump(self.config_data, f, ensure_ascii=False, indent=4)
        self.logger.print_log("保存配置文件到:{0}".format(self.config_path))
        self.init()

    def read_config(self):
        """
            根据当前配置名读取配置
        :return:
        """
        all_config_name = self.get_all_config_file_name()
        ref_config_name = self.read_config_file_name()
        if ref_config_name in all_config_name:
            self.logger.print_log("读取预设配置：{0}".format(ref_config_name))
            self.ref_config_name = ref_config_name

        self.config_path = '{0}{1}.json'.format(self.ref_dir, self.ref_config_name)
        if op.exists(self.config_path):
            with open(self.config_path, encoding='utf-8') as global_file:
                return json.load(global_file)
        return {}

    def get_all_config_file_name(self):
        """
            获取所有配置名
        :return:
        """
        directory = self.ref_dir
        # 获取指定目录下的所有文件和子目录
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        files = os.listdir(directory)
        files_name = []
        # 遍历所有文件和子目录
        for file in files:
            # 使用 os.path.join() 构建文件的完整路径
            file_path = os.path.join(directory, file)

            # 检查是否为文件
            if os.path.isfile(file_path):
                # 使用 os.path.splitext 分离文件名和扩展名
                filename, _ = os.path.splitext(file)
                files_name.append(filename)

        return files_name

    def read_config_file_name(self, default="global_config"):
        """
            从当前配置名称中加载配置
        :param default:
        :return:
        """
        file_path = self.base_path + self.use_ref_name
        try:
            if not os.path.exists(file_path):
                return default
            # 使用 open 函数打开文件
            with open(file_path) as file:
                # 读取文件内容
                return file.read()
        except FileNotFoundError:
            self.logger.print_log(f"文件 '{file_path}' 不存在.")
        except Exception as e:
            self.logger.print_log(f"发生错误: {e}")

    def writer_config_file_name(self):
        """
            修改当前配置文件名称
        """
        file_path = self.base_path + self.use_ref_name
        try:
            # 使用 open 函数以写入模式打开文件
            with open(file_path, 'w') as file:
                # 将内容写入文件
                file.write(self.ref_config_name)
            self.logger.print_log(f"成功写入文件: {file_path}")
        except Exception as e:
            self.logger.print_log(f"写入文件时发生错误: {e}")

    def copy_config(self, target):
        """
            复制当前配置文件到目标路径
        :param target:
        """
        try:
            source_path = '{0}{1}.json'.format(self.ref_dir, self.read_config_file_name())
            target_path = '{0}{1}.json'.format(self.ref_dir, target)
            # 使用 shutil.copy 复制文件
            shutil.copy(source_path, target_path)
            self.logger.print_log(f"成功复制文件: {source_path} 到 {target_path}")
        except Exception as e:
            self.logger.print_log(f"复制文件时发生错误: {e}")
