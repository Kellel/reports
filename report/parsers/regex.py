
class REGEX:
    date = r"(\d{4}-\d{2}-\d{2} [A-Z]{3})"
    datetime = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [A-Z]{3})"
    datetime2 = r"(\d{2}\/\d{2}\/\d{4} \d{1,2}:\d{2})"
    datetime3 = r"(\d{2}\/\d{2}\/\d{4})"
    string_with_space = r"([\S ]*)"
    string = r"(\S*)"
    sku = r"([A-Z0-9]*)"
    integer = r"(\d+)"
    currency = r"([A-Z]{3})"
    float = r"(\d+\.\d+)"

    @staticmethod
    def join(list, sep=None):
        return sep.join(list)
