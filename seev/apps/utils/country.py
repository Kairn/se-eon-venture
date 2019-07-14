# Define country related utilities


class UnoCountry:
    US = 'US'
    AF = 'AF'
    AL = 'AL'
    DZ = 'DZ'
    AS = 'AS'
    AD = 'AD'
    AO = 'AO'
    AI = 'AI'
    AQ = 'AQ'
    AG = 'AG'
    AR = 'AR'
    AM = 'AM'
    AW = 'AW'
    AU = 'AU'
    AT = 'AT'
    AZ = 'AZ'

    DATA_DICT = {
        US: 'United States of America',
        AF: 'Afghanistan',
        AL: 'Albania',
        DZ: 'Algeria',
        AS: 'American Samoa',
        AD: 'Andorra',
        AO: 'Angola',
        AI: 'Anguilla',
        AQ: 'Antarctica',
        AG: 'Antigua and Barbuda',
        AR: 'Argentina',
        AM: 'Armenia',
        AW: 'Aruba',
        AU: 'Australia',
        AT: 'Austria',
        AZ: 'Azerbaijan',
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
