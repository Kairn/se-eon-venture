# Define state related utilities


class UnoState:
    AL = 'AL'

    DATA_DICT = {
        AL: 'Alabama',
    }

    def __init__(self):
        pass

    @staticmethod
    def get_st_code_list():
        data_list = []

        for i, j in UnoState.DATA_DICT.items():
            st = (i, j)
            data_list.append(st)

        return data_list
