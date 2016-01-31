from screeninfo import Monitor, get_monitors

from Infrastructure.PlatformUtility import PlatformUtility


class ScreenUtility():
    @staticmethod
    def get_monitors_or_default(tkroot=None):
        result = None
        if PlatformUtility.platform_is_mac() and tkroot is None:
            result = [Monitor(0, 0, 1920, 1080)]
        elif PlatformUtility.platform_is_mac() and tkroot is not None:
            result = [Monitor(0, 0, tkroot.winfo_screenwidth(), tkroot.winfo_screenheight())]
        else:
            result = get_monitors()
        return result

    @staticmethod
    def get_num_monitors(tkroot=None):
        return ScreenUtility.get_monitors_or_default(tkroot).__len__()
