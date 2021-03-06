"""
Define country related utilities
"""


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
    JM = 'JM'
    JP = 'JP'
    JE = 'JE'
    JO = 'JO'
    KZ = 'KZ'
    KE = 'KE'
    KI = 'KI'
    KP = 'KP'
    KR = 'KR'
    KW = 'KW'
    KG = 'KG'
    LA = 'LA'
    LV = 'LV'
    LB = 'LB'
    LS = 'LS'
    LR = 'LR'
    LY = 'LY'
    LI = 'LI'
    LT = 'LT'
    LU = 'LU'
    MO = 'MO'
    MG = 'MG'
    MW = 'MW'
    MY = 'MY'
    MV = 'MV'
    ML = 'ML'
    MT = 'MT'
    MQ = 'MQ'
    MR = 'MR'
    MU = 'MU'
    YT = 'YT'
    MX = 'MX'
    MC = 'MC'
    MN = 'MN'
    ME = 'ME'
    MS = 'MS'
    MA = 'MA'
    MZ = 'MZ'
    MM = 'MM'
    NA = 'NA'
    NR = 'NR'
    NP = 'NP'
    NL = 'NL'
    NC = 'NC'
    NZ = 'NZ'
    NI = 'NI'
    NE = 'NE'
    NG = 'NG'
    NU = 'NU'
    NF = 'NF'
    NO = 'NO'
    OM = 'OM'
    PK = 'PK'
    PW = 'PW'
    PS = 'PS'
    PA = 'PA'
    PG = 'PG'
    PY = 'PY'
    PE = 'PE'
    PH = 'PH'
    PN = 'PN'
    PL = 'PL'
    PT = 'PT'
    PR = 'PR'
    QA = 'QA'
    RO = 'RO'
    RU = 'RU'
    RW = 'RW'
    LC = 'LC'
    PM = 'PM'
    WS = 'WS'
    SM = 'SM'
    SA = 'SA'
    SN = 'SN'
    RS = 'RS'
    SC = 'SC'
    SL = 'SL'
    SG = 'SG'
    SK = 'SK'
    SI = 'SI'
    SB = 'SB'
    SO = 'SO'
    ZA = 'ZA'
    SS = 'SS'
    ES = 'ES'
    LK = 'LK'
    SD = 'SD'
    SR = 'SR'
    SE = 'SE'
    CH = 'CH'
    SY = 'SY'
    TW = 'TW'
    TJ = 'TJ'
    TZ = 'TZ'
    TH = 'TH'
    TG = 'TG'
    TK = 'TK'
    TO = 'TO'
    TT = 'TT'
    TN = 'TN'
    TR = 'TR'
    TM = 'TM'
    TV = 'TV'
    UG = 'UG'
    UA = 'UA'
    AE = 'AE'
    GB = 'GB'
    UY = 'UY'
    UZ = 'UZ'
    VU = 'VU'
    VE = 'VE'
    VN = 'VN'
    WF = 'WF'
    EH = 'EH'
    YE = 'YE'
    ZM = 'ZM'
    ZW = 'ZW'

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
        JM: 'Jamaica',
        JP: 'Japan',
        JE: 'Jersey',
        JO: 'Jordan',
        KZ: 'Kazakhstan',
        KE: 'Kenya',
        KI: 'Kiribati',
        KP: 'North Korea',
        KR: 'South Korea',
        KW: 'Kuwait',
        KG: 'Kyrgyzstan',
        LA: 'Laos',
        LV: 'Latvia',
        LB: 'Lebanon',
        LS: 'Lesotho',
        LR: 'Liberia',
        LY: 'Libya',
        LI: 'Liechtenstein',
        LT: 'Lithuania',
        LU: 'Luxembourg',
        MO: 'Macao',
        MG: 'Madagascar',
        MW: 'Malawi',
        MY: 'Malaysia',
        MV: 'Maldives',
        ML: 'Mali',
        MT: 'Malta',
        MQ: 'Martinique',
        MR: 'Mauritania',
        MU: 'Mauritius',
        YT: 'Mayotte',
        MX: 'Mexico',
        MC: 'Monaco',
        MN: 'Mongolia',
        ME: 'Montenegro',
        MS: 'Montserrat',
        MA: 'Morocco',
        MZ: 'Mozambique',
        MM: 'Myanmar',
        NA: 'Namibia',
        NR: 'Nauru',
        NP: 'Nepal',
        NL: 'Netherlands',
        NC: 'New Caledonia',
        NZ: 'New Zealand',
        NI: 'Nicaragua',
        NE: 'Niger',
        NG: 'Nigeria',
        NU: 'Niue',
        NF: 'Norfolk Island',
        NO: 'Norway',
        OM: 'Oman',
        PK: 'Pakistan',
        PW: 'Palau',
        PS: 'Palestine',
        PA: 'Panama',
        PG: 'Papua New Guinea',
        PY: 'Paraguay',
        PE: 'Peru',
        PH: 'Philippines',
        PN: 'Pitcairn',
        PL: 'Poland',
        PT: 'Portugal',
        PR: 'Puerto Rico',
        QA: 'Qatar',
        RO: 'Romania',
        RU: 'Russia',
        RW: 'Rwanda',
        LC: 'Saint Lucia',
        PM: 'Saint Pierre and Miquelon',
        WS: 'Samoa',
        SM: 'San Marino',
        SA: 'Saudi Arabia',
        SN: 'Senegal',
        RS: 'Serbia',
        SC: 'Seychelles',
        SL: 'Sierra Leone',
        SG: 'Singapore',
        SK: 'Slovakia',
        SI: 'Slovenia',
        SB: 'Solomon Islands',
        SO: 'Somalia',
        ZA: 'South Africa',
        SS: 'South Sudan',
        ES: 'Spain',
        LK: 'Sri Lanka',
        SD: 'Sudan',
        SR: 'Suriname',
        SE: 'Sweden',
        CH: 'Switzerland',
        SY: 'Syria',
        TW: 'Taiwan',
        TJ: 'Tajikistan',
        TZ: 'Tanzania',
        TH: 'Thailand',
        TG: 'Togo',
        TK: 'Tokelau',
        TO: 'Tonga',
        TT: 'Trinidad and Tobago',
        TN: 'Tunisia',
        TR: 'Turkey',
        TM: 'Turkmenistan',
        TV: 'Tuvalu',
        UG: 'Uganda',
        UA: 'Ukraine',
        AE: 'United Arab Emirates',
        GB: 'United Kingdom',
        UY: 'Uruguay',
        UZ: 'Uzbekistan',
        VU: 'Vanuatu',
        VE: 'Venezuela',
        VN: 'Vietnam',
        WF: 'Wallis and Futuna',
        EH: 'Western Sahara',
        YE: 'Yemen',
        ZM: 'Zambia',
        ZW: 'Zimbabwe',
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

    @staticmethod
    def get_country_by_code(code):
        try:
            return UnoCountry.DATA_DICT[code]
        except:
            return ''
