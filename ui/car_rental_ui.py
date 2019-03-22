from ui.menu import Menu
from datetime import datetime
# This class holds costructor functions for menus
# It uses data from the controller it is attatched to
# To make these generic menus
# Examples of a generic menu include:
#   Search results, edit model object, delete model object,
#   confirmation screen


class CarRentalUI(object):
    def __init__(self, back_callback, stop_callback):
        self.__back = back_callback
        self.__stop = stop_callback

    def get_search_result_menu(self, results, header_message,
                               callback_function):
        header = "{} -> Leit".format(header_message)
        header += "\nFann {} niðurstöður:".format(len(results))
        option_list = list()
        for item in results:
            item_option = {"description": item,
                           "value": callback_function}
            option_list.append(item_option)
        result_menu = Menu(
            header=header, options=option_list, back_function=self.__back,
            stop_function=self.__stop, max_options_per_page=5
        )
        return result_menu

    def get_model_object_options_menu(self, model_object, object_name,
                                      header_message, edit_callback,
                                      delete_callback,
                                      order_history_callback=None):
        header = "{} -> Leit -> Val".format(header_message)
        header += "\nÞú valdir: {}".format(object_name)
        for key, value in model_object.csv_repr().items():
            try:
                datetime.fromisoformat(value)
                value = value.replace("T", " ")
            except ValueError:
                pass
            header += "\n\t{}: {}".format(key, value)
        edit_text = "Breyta: {}".format(object_name)
        delete_text = "Eyða: {}".format(object_name)
        options = [
            {"description": edit_text, "value": edit_callback},
            {"description": delete_text, "value": delete_callback},
        ]
        if order_history_callback is not None:
            options.append(
                {"description": "Skoða pöntunarsögu",
                    "value": order_history_callback}
            )
        return Menu(header=header, options=options, back_function=self.__back,
                    stop_function=self.__stop)

    def get_edit_report_menu(self, model_object, controller_name,
                             restart_callback):
        message = "{} uppfærð!\nHlutinum hefur verið breytt."
        message = message.format(controller_name)
        return self.get_report_menu(
            model_object, controller_name, restart_callback, message
        )

    def get_creation_report_menu(self, model_object, controller_name,
                                 restart_callback, can_go_back=False,
                                 pop_after_create=False):
        message = "{} uppfærð!\nNýja hlutinum hefur verið bætt við."
        message = message.format(controller_name)
        return self.get_report_menu(
            model_object, controller_name, restart_callback, message,
            can_go_back, pop_after_create
        )

    def get_report_menu(self, model_object, return_location,
                        restart_callback, message, can_go_back=True,
                        pop_after_report=False):
        message += "\nNýju gildin eru:"
        for key, value in model_object.get_dict().items():
            message += "\n\t{}: {}".format(key, value)
        if not pop_after_report:
            options = [{"description": "Aftur í {}".format(return_location),
                        "value": restart_callback}]
        else:
            options = [
                {"description": "Halda áfram í leiguferli",
                    "value": restart_callback}
                ]
        report_menu = Menu(
            header=message, options=options, back_function=self.__back,
            stop_function=self.__stop, can_go_back=can_go_back
        )
        return report_menu

    def get_edit_menu(self, model_object, object_name,
                      header_message, submit_callback=None):
        inputs = list()
        header = "{} -> Leit -> Val: {} -> Breyta\nSkráðu gildi fyrir {}"
        header = header.format(header_message, object_name, object_name)
        for key, value in model_object.csv_repr().items():
            input_type = key
            input_dict = {"prompt": key, "value": value, "type": input_type}
            inputs.append(input_dict)
        edit_menu = Menu(
            header=header, inputs=inputs, back_function=self.__back,
            stop_function=self.__stop, submit_function=submit_callback,
            can_go_back=False
        )
        return edit_menu

    def get_deletion_menu(self, model_object, object_name, controller_message,
                          deletion_callback):
        header = "{} -> Leit -> Val -> Eyða"
        header += "\nErtu vissu um að þú viljir eyða {}?"
        header = header.format(controller_message, object_name)
        options = [{"description": "Eyða {}".format(object_name), "hotkey": 0,
                    "value": deletion_callback}]
        deletion_menu = Menu(header=header, options=options,
                             back_function=self.__back,
                             stop_function=self.__stop)
        return deletion_menu

    def get_delete_feedback_menu(self, object_name, controller_message,
                                 restart_callback):
        header = "{}\n{} hefur verið eytt."
        header = header.format(controller_message, object_name)
        options = [{"description": "Aftur í " + controller_message,
                    "value": restart_callback}]
        delete_feedback_menu = Menu(header=header, can_go_back=False,
                                    options=options, stop_function=self.__stop)
        return delete_feedback_menu

    def get_new_model_object_menu(self, controller_header, fields, type_str,
                                  submit_callback):
        header = controller_header + " -> Nýr"
        header += "\nSláðu inn upplýsingarnar fyrir nýja {}:"
        header = header.format(type_str)
        inputs = [{"prompt": field} for field in fields]
        new_model_object_menu = Menu(
            header=header, inputs=inputs, back_function=self.__back,
            stop_function=self.__stop, submit_function=submit_callback
        )
        return new_model_object_menu

    def get_edit_by_field_menu(self, fields, object_name,
                               header_message, submit_callback):
        inputs = list()
        header = "{} -> Leit -> Val: {} -> Breyta\nSkráðu gildi fyrir {}"
        header = header.format(header_message, object_name, object_name)
        for key, value in fields.items():
            input_type = key
            input_dict = {"prompt": key, "value": value, "type": input_type}
            inputs.append(input_dict)
        edit_menu = Menu(
            header=header, inputs=inputs, back_function=self.__back,
            stop_function=self.__stop, submit_function=submit_callback
        )
        return edit_menu

    def get_order_history_menu(
            self, header_str, orders, model_object, callback
            ):
        options = list()
        header = "{} -> Leit -> Val -> Pöntunarsaga\nPöntunarsaga {}"
        header = header.format(header_str, model_object.get_name())
        for order in orders:
            options.append(
                {"description": order, "value": callback}
            )
        order_history_menu = Menu(
            header=header_str, back_function=self.__back,
            stop_function=self.__stop, options=options
        )
        return order_history_menu
