import platform


class PlatformUtility():
    @staticmethod
    def platform_is_mac():
        return platform.system() == 'Darwin'