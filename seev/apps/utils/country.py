# Define country related utilities


class UnoCountry:
    US = 'US'

    DATA_DICT = {
        US: 'United States of America',
    }

    def __init__(self):
        pass

    @staticmethod
    def get_cty_code_list():
        data_list = []

        for i, j in UnoCountry.DATA_DICT.items():
            cty = (i, j)
            data_list.append(cty)

        return data_list

    @staticmethod
    def get_default_cty():
        return (UnoCountry.US, UnoCountry.DATA_DICT[UnoCountry.US])
