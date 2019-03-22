import os
from ui.input_line import InputLine
from ui.option import MenuOption
from ui.readkey import readkey

# This is the menu class.
# It creates menus based on the constructor input.
# Calling get_input() on the menu activates it.
# Then it will read input from the user and print to the screen.
# it returns the users input, both from options and input_lines

BACK = "B"
QUIT = "Q"
SUBMIT = "S"
NEXT_PAGE = ">"
LAST_PAGE = "<"
FULL_QUIT = "Hætta"
NORMAL_QUIT = "Hætta: Aftur í aðalvalmynd"


class Menu(object):
    __CURSOR = "→"

    def __init__(self, header="", errors=list(), inputs=dict(),
                 options=list(), footer="", page=0, max_options_per_page=11,
                 can_go_back=True, stop_function=None, back_function=None,
                 submit_function=None, can_submit=True, full_quit=False):
        self.__header = header
        self.__footer = footer
        self.__current_page_number = page
        self.__cursor_position = 0
        self.__inputs = self.__process_inputs(inputs)
        self.__options = list()
        self.__pages = list()
        self.__can_go_back = can_go_back
        self.__can_submit = can_submit
        self.__max_options_per_page = max_options_per_page
        self.__selected_input = None
        self.__selection = None
        self.__errors = errors
        self.__stop_function = stop_function
        self.__back_function = back_function
        self.__submit_function = submit_function
        self.__quit_string = FULL_QUIT if full_quit else NORMAL_QUIT
        self.__process_options(options)
        self.__process_pages()
        self.__move_cursor()

    def __process_inputs(self, inputs):
        """Take list of input dicts and process into a list of InputLines."""
        processed = list()
        for an_input in reversed(inputs):
            prompt = an_input["prompt"]
            default_text = an_input.get("value", "")
            input_type = an_input.get("type", "text")
            input_line = InputLine(prompt, default_text, input_type)
            processed.append(input_line)
        return processed

    def __process_options(self, options):
        counter = 1
        for primitive_option in options:
            description = primitive_option["description"]
            hotkey = primitive_option.get("hotkey", counter)
            value = primitive_option.get("value", None)
            option = MenuOption(value, description, hotkey)
            self.__options.append(option)
            if hotkey == counter:
                counter += 1
        self.__options.reverse()

    def __get_foot_options(self):
        quit_str = self.__quit_string
        quit_option = MenuOption(self.__stop_function, quit_str, QUIT)
        back_option = MenuOption(self.__back_function, "Til baka", BACK)
        submit_option = MenuOption(self.__submit_function, "Staðfesta", SUBMIT)
        foot_options = [quit_option]
        if self.__can_go_back:
            foot_options.insert(0, back_option)
        if self.__inputs and self.__can_submit:
            foot_options.insert(0, submit_option)
        return foot_options

    def __process_pages(self):
        foot_options = self.__get_foot_options()
        last_page_option = MenuOption(LAST_PAGE, "Fletta til baka")
        next_page_option = MenuOption(NEXT_PAGE, "Fletta áfram")
        seperator = list()
        if self.__inputs and self.__options:
            seperator.append("")
        lines = self.__options + seperator + self.__inputs
        self.__add_page(lines, last_page_option, next_page_option,
                        foot_options)
        while lines:
            self.__add_page(lines, last_page_option,
                            next_page_option, foot_options)

    def __add_page(self, lines, last_page_option,
                   next_page_option, foot_options):
        page = list()
        for i in range(self.__max_options_per_page):
            try:
                line = lines.pop()
            except IndexError:
                break
            page.append(line)
        page.append("")
        if lines:
            page.append(next_page_option)
        if self.__pages:
            page.append(last_page_option)
        for option in foot_options:
            page.append(option)
        self.__pages.append(page)

    def __display(self):
        display_string = "{}\n\n".format(self.__header)
        if self.__errors:
            display_string += "Villa:\n"
        for error in self.__errors:
            display_string += "{}\n".format(error)
        display_string += self.__page_string()
        display_string += self.__page_number_string()
        display_string += "\n" + self.__footer
        self.__clear_screen()
        print(display_string.strip())  # Print the entire menu

    def __page_string(self):
        cursor_filler = " " * (len(self.__CURSOR) + 1)
        page = self.__pages[self.__current_page_number]
        page_string = ""
        for i, line in enumerate(page):
            start = cursor_filler
            if self.__cursor_position == i:
                start = self.__CURSOR
            elif not line:
                start = ""
            page_string += "{}{}\n".format(start, str(line))
        return page_string.strip("\n\r")

    def __page_number_string(self):
        if len(self.__pages) > 1:
            return "\nSíða {} af {}\n".format(
                self.__current_page_number + 1,
                len(self.__pages)
            )
        else:
            return ""

    def get_input(self):
        self.__select_input_by_cursor()
        self.__selection = None
        while self.__selection is None:
            self.__display()
            key = readkey()
            self.__process_input(key)
        # return the selection and any input lines values
        values = self.__get_input_values()
        if not values:
            values = self.__selection.get_description()
        return self.__selection.get_value(), values

    def __get_input_values(self):
        values = dict()
        for input_line in reversed(self.__inputs):
            values[input_line.get_key()] = input_line.get_input()
        return values

    def __process_input(self, key):
        if key == 10080:  # arrow down
            self.__move_cursor(1)
        elif key == 10072:  # arrow up
            self.__move_cursor(-1)
        elif key == 10075 and self.__selected_input is None:
            # arrow left
            self.__previous_page()
        elif key == 10077 and self.__selected_input is None:
            # arrow right
            self.__next_page()
        elif key == 27:  # escape
            if self.__selected_input is None:
                if self.__back_function is not None:
                    self.__selection = MenuOption(
                        self.__back_function, ""
                    )
            else:
                self.__move_cursor()
        elif key == 9:  # tab
            self.__move_cursor(1)
            self.__select_input_by_cursor()
        elif key == 13:  # return
            self.__handle_return()
        elif self.__selected_input is not None:
            self.__selected_input.keypress(chr(key))
        else:
            self.__handle_hotkey(key)

    def __handle_return(self):
        page = self.__pages[self.__current_page_number]
        cursor_input = page[self.__cursor_position]
        if type(cursor_input) == InputLine:
            if cursor_input == self.__selected_input:
                self.__move_cursor(1)
            self.__select_input_by_cursor()
        else:
            selection = cursor_input.get_value()
            if selection == NEXT_PAGE:
                self.__next_page()
            elif selection == LAST_PAGE:
                self.__previous_page()
            else:
                self.__selection = cursor_input

    def __handle_hotkey(self, key):
        hotkey = chr(key)
        if hotkey == NEXT_PAGE:
            self.__next_page()
            return
        elif hotkey == LAST_PAGE:
            self.__previous_page()
            return
        page = self.__pages[self.__current_page_number]
        for item in page:
            if type(item) == MenuOption:
                if item.get_hotkey().upper() == hotkey.upper():
                    self.__selection = item
                    break

    def __next_page(self):
        self.__change_page(self.__current_page_number + 1)

    def __previous_page(self):
        self.__change_page(self.__current_page_number - 1)

    def __change_page(self, page_number):
        page_number %= len(self.__pages)
        if page_number != self.__current_page_number:
            self.__current_page_number = page_number
            self.__cursor_position = 0
            self.__move_cursor()

    def __select_input_by_cursor(self):
        page = self.__pages[self.__current_page_number]
        cursor_input = page[self.__cursor_position]
        if type(cursor_input) == InputLine:
            self.__selected_input = cursor_input
            cursor_input.set_active(True)

    def __move_cursor(self, distance=0):
        direction = distance >= 0    # True if down, False if up
        distance = abs(distance)
        cursor = self.__cursor_position
        page = self.__pages[self.__current_page_number]
        if page[cursor] in ["", "\n"]:
            cursor += 1
            cursor %= len(page)
        while distance != 0:
            cursor += 1 if direction else -1
            cursor %= len(page)
            if page[cursor] not in ["", "\n"]:
                distance -= 1
        self.__cursor_position = cursor
        if self.__selected_input is not None:
            self.__selected_input.set_active(False)
            self.__selected_input = None

    def set_errors(self, errors: list):
        self.__errors = errors

    def __clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
