class MenuOption(object):
    def __init__(self, value, description, hotkey=None):
        self.__value = value
        self.__description = description
        if hotkey is None:
            self.__hotkey = str(value)[0]
        else:
            self.__hotkey = str(hotkey)

    def __str__(self):
        return "[{}] {}".format(self.__hotkey, str(self.__description))

    def get_hotkey(self):
        return self.__hotkey

    def get_value(self):
        return self.__value

    def get_description(self):
        return self.__description
