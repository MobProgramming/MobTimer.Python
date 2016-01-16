


class ImageUtility(object):
    def __init__(self, theme_manager):
        self.theme_manager = theme_manager

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def load(self, image_path, width=50, height=50, normalize_color=True):
        import platform

        if platform.system() == 'Darwin':
            return None

        from PIL import Image
        from PIL import ImageTk
        background_color = ImageUtility.hex_to_rgb(self.theme_manager.background_color)
        highlight_color = ImageUtility.hex_to_rgb(self.theme_manager.highlight_color)
        original = Image.open(image_path)
        resized = original.resize((width, height), Image.ANTIALIAS)

        if normalize_color:
            pixel_access = resized.load()
            for y in range(resized.size[1]):
                for x in range(resized.size[0]):
                    pixel = pixel_access[x, y]
                    if pixel[0] < 50:
                        pixel_access[x, y] = (background_color[0] + pixel_access[x, y][0],
                                              background_color[1] + pixel_access[x, y][1],
                                              background_color[2] + pixel_access[x, y][2])
                    elif pixel[0] > 50:
                        pixel_access[x, y] = (int(highlight_color[0] * pixel_access[x, y][0] / 255),
                                              int(highlight_color[1] * pixel_access[x, y][1] / 255),
                                              int(highlight_color[2] * pixel_access[x, y][2] / 255))

        return ImageTk.PhotoImage(resized)
