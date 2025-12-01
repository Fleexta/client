#  Copyright (c) 2025 Timofei Kirsanov


class Themes:

    class COMMON:

        ERROR_COLOR = "#ff6b6b"

        def __str__(self):
            return Themes().__str__() + "." + self.__class__.__name__

    class LIGHT:
        BACKGROUND_COLOR_BACK = "#f0f0f5"
        BACKGROUND_COLOR_FRONT = "#e0e0e8"
        BACKGROUND_COLOR_DOWNLOAD = "#d0d0da"
        BACKGROUND_COLOR_FRAME = "#f5f5fa"
        TIME_COLOR = "#5a5a65"
        TEXT = "#202020"
        TEXT_MAIN = "#000000"
        TEXT_SUPPORT = "#555555"

        def __str__(self):
            return Themes().__str__() + "." + self.__class__.__name__

    class DARK:
        BACKGROUND_COLOR_BACK = "#2a2a32"
        BACKGROUND_COLOR_FRONT = "#3a3a46"
        BACKGROUND_COLOR_DOWNLOAD = "#4a4a5a"
        BACKGROUND_COLOR_FRAME = "#23232b"
        TIME_COLOR = "#969ba5"
        TEXT = "#e0e0e0"
        TEXT_MAIN = "#ffffff"
        TEXT_SUPPORT = "#cccccc"

        def __str__(self):
            return Themes().__str__() + "." + self.__class__.__name__

    class SYSTEM:
        def __str__(self):
            return Themes().__str__() + "." + self.__class__.__name__

    def __str__(self):
        return self.__class__.__name__
