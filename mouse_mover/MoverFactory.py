from log.Logger import Logger
from mouse_mover.KmBoxMover import KmBoxMover
from mouse_mover.Win32ApiMover import Win32ApiMover
from mouse_mover.WuYaMover import WuYaMover


def get_mover(logger: Logger, mouse_model, mouse_mover_params):
    mouse_mover_param = mouse_mover_params[mouse_model]
    if mouse_mover_param is None:
        logger.print_log(f"鼠标模式:[{mouse_model}]不可用")
    else:
        logger.print_log(f"初始化鼠标模式：[{mouse_model}]")
    if mouse_model == 'win32api':
        return Win32ApiMover(logger, mouse_mover_param)
    elif mouse_model == "km_box":
        return KmBoxMover(logger, mouse_mover_param)
    elif mouse_model == "wu_ya":
        return WuYaMover(logger, mouse_mover_param)
