from dataclasses import fields


class Repo(object):
    pass

    def save():
        raise NotImplementedError()

    def read():
        raise NotImplementedError()

    def search(self, dataclass, arguments, search_set):
        class_fields = fields(dataclass)
        subset = set(search_set)
        for item in search_set:
            for field in class_fields:
                arg = arguments[field.name]
                prop = item.get_dict()[field.name]
                if arg and prop != arg:
                    subset.remove(item)
        return subset
