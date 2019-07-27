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
    BH = 'BH'
    BD = 'BD'
    BB = 'BB'
    BY = 'BY'
    BE = 'BE'
    BZ = 'BZ'
    BJ = 'BJ'
    BM = 'BM'
    BT = 'BT'
    BW = 'BW'
    BV = 'BV'
    BR = 'BR'
    BN = 'BN'
    BG = 'BG'
    BF = 'BF'
    BI = 'BI'
    CV = 'CV'
    KH = 'KH'
    CM = 'CM'
    CA = 'CA'
    TD = 'TD'
    CL = 'CL'
    CN = 'CN'
    CX = 'CX'
    CO = 'CO'
    CG = 'CG'
    CR = 'CR'
    HR = 'HR'
    CU = 'CU'
    CY = 'CY'
    CZ = 'CZ'
    DK = 'DK'
    DJ = 'DJ'
    DM = 'DM'
    DO = 'DO'
    EC = 'EC'
    EG = 'EG'
    SV = 'SV'
    GQ = 'GQ'
    ER = 'ER'
    EE = 'EE'
    SZ = 'SZ'
    ET = 'ET'
    FJ = 'FJ'
    FI = 'FI'
    FR = 'FR'
    GF = 'GF'
    PF = 'PF'
    GA = 'GA'
    GM = 'GM'
    GE = 'GE'
    DE = 'DE'
    GH = 'GH'
    GI = 'GI'
    GR = 'GR'
    GL = 'GL'
    GD = 'GD'
    GP = 'GP'
    GU = 'GU'
    GT = 'GT'
    GG = 'GG'
    GN = 'GN'
    GY = 'GY'
    HT = 'HT'
    HN = 'HN'
    HK = 'HK'
    HU = 'HU'
    IS = 'IS'
    IN = 'IN'
    ID = 'ID'
    IR = 'IR'
    IQ = 'IQ'
    IE = 'IE'
    IM = 'IM'
    IL = 'IL'
    IT = 'IT'

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
        BH: 'Bahrain',
        BD: 'Bangladesh',
        BB: 'Barbados',
        BY: 'Belarus',
        BE: 'Belgium',
        BZ: 'Belize',
        BJ: 'Benin',
        BM: 'Bermuda',
        BT: 'Bhutan',
        BW: 'Botswana',
        BV: 'Bouvet Island',
        BR: 'Brazil',
        BN: 'Brunei Darussalam',
        BG: 'Bulgaria',
        BF: 'Burkina Faso',
        BI: 'Burundi',
        CV: 'Cabo Verde',
        KH: 'Cambodia',
        CM: 'Cameroon',
        CA: 'Canada',
        TD: 'Chad',
        CL: 'Chile',
        CN: 'China',
        CX: 'Christmas Island',
        CO: 'Colombia',
        CG: 'Congo',
        CR: 'Costa Rica',
        HR: 'Croatia',
        CU: 'Cuba',
        CY: 'Cyprus',
        CZ: 'Czechia',
        DK: 'Denmark',
        DJ: 'Djibouti',
        DM: 'Dominica',
        DO: 'Dominican Republic',
        EC: 'Ecuador',
        EG: 'Egypt',
        SV: 'El Salvador',
        GQ: 'Equatorial Guinea',
        ER: 'Eritrea',
        EE: 'Estonia',
        SZ: 'Eswatini',
        ET: 'Ethiopia',
        FJ: 'Fiji',
        FI: 'Finland',
        FR: 'France',
        GF: 'French Guiana',
        PF: 'French Polynesia',
        GA: 'Gabon',
        GM: 'Gambia',
        GE: 'Georgia',
        DE: 'Germany',
        GH: 'Ghana',
        GI: 'Gibraltar',
        GR: 'Greece',
        GL: 'Greenland',
        GD: 'Grenada',
        GP: 'Guadeloupe',
        GU: 'Guam',
        GT: 'Guatemala',
        GG: 'Guernsey',
        GN: 'Guinea',
        GY: 'Guyana',
        HT: 'Haiti',
        HN: 'Honduras',
        HK: 'Hong Kong',
        HU: 'Hungary',
        IS: 'Iceland',
        IN: 'India',
        ID: 'Indonesia',
        IR: 'Iran',
        IQ: 'Iraq',
        IE: 'Ireland',
        IM: 'Isle of Man',
        IL: 'Israel',
        IT: 'Italy',
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
