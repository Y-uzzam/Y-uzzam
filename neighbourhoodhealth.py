"""CSC108: Fall 2022 -- Assignment 3: Hypertension and Low Income

This code is provided solely for the personal and private use of
students taking the CSC108/CSCA08 course at the University of
Toronto. Copying for purposes other than this use is expressly
prohibited. All forms of distribution of this code, whether as given
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Jacqueline Smith and David Liu
"""
from typing import TextIO
import statistics  # Note that this requires Python 3.10

ID = "id"
HT_KEY = "hypertension"
TOTAL = "total"
LOW_INCOME = "low_income"

# Indexes in the inner lists of hypertension data in CityData
# HT is an abbreviation of hypertension, NBH is an abbreviation of neighbourhood
HT_20_44 = 0
NBH_20_44 = 1
HT_45_64 = 2
NBH_45_64 = 3
HT_65_UP = 4
NBH_65_UP = 5

# columns in input files
ID_COL = 0
NBH_NAME_COL = 1
POP_COL = 2
LI_POP_COL = 3

SAMPLE_DATA = {
    "West Humber-Clairville": {
        "id": 1,
        "hypertension": [703, 13291, 3741, 9663, 3959, 5176],
        "total": 33230,
        "low_income": 5950,
    },
    "Mount Olive-Silverstone-Jamestown": {
        "id": 2,
        "hypertension": [789, 12906, 3578, 8815, 2927, 3902],
        "total": 32940,
        "low_income": 9690,
    },
    "Thistletown-Beaumond Heights": {
        "id": 3,
        "hypertension": [220, 3631, 1047, 2829, 1349, 1767],
        "total": 10365,
        "low_income": 2005,
    },
    "Rexdale-Kipling": {
        "id": 4,
        "hypertension": [201, 3669, 1134, 3229, 1393, 1854],
        "total": 10540,
        "low_income": 2140,
    },
    "Elms-Old Rexdale": {
        "id": 5,
        "hypertension": [176, 3353, 1040, 2842, 948, 1322],
        "total": 9460,
        "low_income": 2315,
    },
}

SAMPLE_DATA2 = {
    "Milliken": {
        "id": 130, "hypertension": [417, 8970, 2574, 8183, 3864, 5274],
        "total": 26585,
        "low_income": 7240,
    },
    "Rouge": {
        "id": 131, "hypertension": [967, 16028, 5561, 13670, 4976, 6640],
        "total": 46495,
        "low_income": 4770,
    },
    "Malvern": {
        "id": 132, "hypertension": [995, 16526, 5151, 12696, 4866, 6418],
        "total": 43795,
        "low_income": 9195,
    },
    "Centennial Scarborough": {
        "id": 133, "hypertension": [211, 4261, 1384, 4143, 1712, 2449],
        "total": 13370,
        "low_income": 920,
    },
    "Highland Creek": {
        "id": 134, "hypertension": [209, 4432, 1601, 3993, 1831, 2453],
        "total": 12500,
        "low_income": 1355,
    },
}


# This function is provided for use in Tasks 3 and 4. You should not change it.
def get_age_standardized_ht_rate(ndata: 'CityData', name: str) -> float:
    """Return the age standardized hypertension rate from the neighbourhood in
    ndata matching the given name.

    Precondition: name is in ndata

    >>> get_age_standardized_ht_rate(SAMPLE_DATA, 'Elms-Old Rexdale')
    24.44627521389894
    >>> get_age_standardized_ht_rate(SAMPLE_DATA, 'Rexdale-Kipling')
    24.72562462246556
    """
    rates = calculate_ht_rates_by_age_group(ndata, name)

    # These rates are normalized for only 20+ ages, using the census data
    # that our datasets are based on.
    canada_20_44 = 11_199_830 / 19_735_665  # Number of 20-44 / Number of 20+
    canada_45_64 = 5_365_865 / 19_735_665  # Number of 45-64 / Number of 20+
    canada_65_plus = 3_169_970 / 19_735_665  # Number of 65+ / Number of 20+

    return (rates[0] * canada_20_44
            + rates[1] * canada_45_64
            + rates[2] * canada_65_plus)


# Task 1
def converttodigit(string: str) -> int:
    """Return an integer based on a string made of digits.
    """
    if string.isdigit():
        return int(string)
    else:
        return string


def clean_data(data: list[list]) -> None:
    """Clean the data, replacing digit strings in the data with
    their respective integers
    """
    for item in data:
        i = 0
        new_num = 0
        while i < len(item):
            new_num = converttodigit(item[i])
            item[i] = new_num
            new_num = 0
            i = i + 1


def prepare_data(filename: str) -> list[list]:
    """Return the data found in the file, where each inner list
    represents a row
    """
    info = read_data(filename)
    list1 = []
    list2 = []
    word = ''
    for item in info:
        i = 0
        while i < len(item[0]):
            if item[0][i] != ',' and item[0][i] != '\n':
                word = word + item[0][i]
            else:
                list2.append(word)
                word = ''
            i = i + 1
        if len(list2) < 8:
            list2.append(word)
        list1.append(list2)
        list2 = []
    i = 0
    clean_data(list1)
    return list1
    
    
def read_data(filename: str) -> list[list[str]]:
    """Return the data found in the file, where each inner list
    contains strings composed of information from their respective
    rows.
    """
    returnlist = []
    emptylist = []
    line = filename.readline()
    while line != '':
        emptylist.append(line)
        returnlist.append(emptylist)
        line = filename.readline()
        emptylist = []
    return returnlist


def get_hypertension_data(z: dict, filename: TextIO) -> None:
    """Modify the given dictionary to include the information
    from the given hypertension data file.
    """
    innerdict = {}
    data = prepare_data(filename)
    i = 1
    while i < len(data):
        if data[i][1] in z:
            innerdict = z[data[i][1]]        
            innerdict[ID] = data[i][0]
            innerdict[HT_KEY] = data[i][2:8]
            z[data[i][1]] = innerdict
            innerdict = {}
        else:
            innerdict[ID] = data[i][0]
            innerdict[HT_KEY] = data[i][2:8]
            z[data[i][1]] = innerdict
            innerdict = {} 
        i = i + 1
    

def get_low_income_data(z: dict, filename: TextIO) -> None:
    """Modify the given dictionary to include the information
    from the given low income data file.
    """
    innerdict = {}
    data = prepare_data(filename)
    i = 1
    while i < len(data):
        if data[i][1] in z:
            innerdict = z[data[i][1]]
            innerdict[ID] = data[i][0]
            innerdict[TOTAL] = data[i][2]
            innerdict[LOW_INCOME] = data[i][3]
            z[data[i][1]] = innerdict
            innerdict = {}
        else:
            innerdict[ID] = data[i][0]
            innerdict[TOTAL] = data[i][2]
            innerdict[LOW_INCOME] = data[i][3]
            z[data[i][1]] = innerdict
            innerdict = {}        
        i = i + 1


# Task 2
def get_bigger_neighbourhood(data: dict, n1: str, n2: str) -> str:
    """Return the neighbourhood with the larger population from 
    low income data.
    
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Rexdale-Kipling', 'Elms-Old Rexdale')
    'Rexdale-Kipling'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Elms-Old Rexdale', 'Rexdale-Kipling')
    'Rexdale-Kipling'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Niagara', 'Rouge')
    'Niagara'
    >>> get_bigger_neighbourhood(SAMPLE_DATA, 'Rouge', 'Niagara')
    'Rouge'
    """
    if n1 in data:
        n1info = data[n1]
        n1pop = n1info[TOTAL]
    else:
        n1pop = 0
    if n2 in data:
        n2info = data[n2]
        n2pop = n2info[TOTAL]
    else:
        n2pop = 0
    if n1pop >= n2pop:
        return n1
    elif n2pop > n1pop:
        return n2
    else:
        return None


def get_ht_ratio(list1: list) -> float:
    """Return the ratio of total number of people with hypertension
    to the total population based on hypertension rate file data.
    
    >>> get_ht_ratio([703, 13291, 3741, 9663, 3959, 5176])
    0.2987202275151084
    >>> get_ht_ratio([789, 12906, 3578, 8815, 2927, 3902])
    0.28466612028255867
    """
    num1 = 0
    i = 1
    while i < len(list1):
        num1 = num1 + list1[i]
        i = i + 2
    num2 = 0
    i = 0
    while i < len(list1):
        num2 = num2 + list1[i]
        i = i + 2
    return num2 / num1


def get_low_income_ratio(num1: int, num2: int) -> float:
    """Return the ratio of total number of low income classified
    people to the total population
    
    >>> get_low_income_ratio(5950, 33230)
    0.1790550707192296
    >>> get_low_income_ratio(9690, 32940)
    0.2941712204007286
    """
    return num1 / num2


def get_high_hypertension_rate(data: 'CityData', threshold: float) \
        -> list[tuple[str, float]]:
    """Return a list containing tuples containing neighbourhoods in
    the 0 index and the hypertension ratio in the 1 index, where the
    hypertension ratio is above a certain threshold.
    
    >>> get_high_hypertension_rate(SAMPLE_DATA, 0.3)
    [('Thistletown-Beaumond Heights', 0.31797739151574084), \
('Rexdale-Kipling', 0.3117001828153565)]
    >>> get_high_hypertension_rate(SAMPLE_DATA, 0.1)
    [('West Humber-Clairville', 0.2987202275151084), ('Mount Olive-Si\
lverstone-Jamestown', 0.28466612028255867), ('Thistletown-Beaumond Heig\
hts', 0.31797739151574084), ('Rexdale-Kipling', 0.3117001828153565), ('E\
lms-Old Rexdale', 0.2878808035120394)]
    """
    list1 = []
    tup = ()
    for item in data:
        hyprate = get_ht_ratio(data[item][HT_KEY])
        if hyprate >= threshold:
            tup = (item, hyprate)
            list1.append(tup)
            tup = ()
    return list1


def get_ht_to_low_income_ratios(data: 'CityData') -> dict[str, float]:
    """Return a dictionary containing neighbourhoods as keys and
    hypertension to low income ratios.
    
    >>> get_ht_to_low_income_ratios(SAMPLE_DATA)
    {'West Humber-Clairville': 1.6683148168616895, 'Mount Olive-Silverst\
one-Jamestown': 0.9676885451091314, 'Thistletown-Beaumond Heights': 1\
.6438083107534431, 'Rexdale-Kipling': 1.5351962275111484, 'Elms-Old Re\
xdale': 1.1763941257986577}
    >>> get_ht_to_low_income_ratios(SAMPLE_DATA2)
    {'Milliken': 1.1223656703751177, 'Rouge': 3.085856493188285, 'Malve\
rn': 1.4716390538213993, 'Centennial Scarborough': 4.4282075883646685\
, 'Highland Creek': 3.0877515063071206}
    """
    dictionary = {}
    for item in data:
        ratio = get_ht_ratio(data[item][HT_KEY]) / \
            get_low_income_ratio(data[item][LOW_INCOME], data[item][TOTAL])                                                                  
        dictionary[item] = ratio
    return dictionary


def calculate_ht_rates_by_age_group(data: 'CityData', area: str) \
        -> tuple[float, float, float]:
    """Return a tuple containing the hypertension rates of each
    age group based on hypertension data
    
    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'Rexdale-Kipling')
    (5.478331970564186, 35.119231960359244, 75.13484358144552)
    >>> calculate_ht_rates_by_age_group(SAMPLE_DATA, 'Elms-Old Rexdale')
    (5.24903071875932, 36.593947923997185, 71.70953101361573)
    """
    info = [-1] * 6
    for item in data:
        if area in item:
            info = data[item][HT_KEY]
    val1 = (info[0] / info[1]) * 100
    val2 = (info[2] / info[3]) * 100
    val3 = (info[4] / info[5]) * 100
    tup = (val1, val2, val3)
    if tup == [100.0, 100.0, 100.0]:
        return None
    else:
        return tup


# Task 3
def get_stats_summary(data: 'CityData') -> float:
    """Return the correlation between age standardized hypertension
    rates and low income rates across all neighbourhoods.
    
    >>> get_stats_summary(SAMPLE_DATA)
    0.28509539188554994
    >>> get_stats_summary(SAMPLE_DATA2)
    -0.1545398309223986
    """
    htlist = []
    lilist = []
    for item in data:
        htlist.append(get_age_standardized_ht_rate(data, item))
        lowincomeratio = data[item][LOW_INCOME] / data[item][TOTAL]
        lilist.append(lowincomeratio)
    return statistics.correlation(htlist, lilist)


# Task 4
def order_by_ht_rate(data: 'CityData') -> list[str]:
    """Return a list of the names of the neighbourhoods, ordered 
    from lowest to highest age-standardized hypertension rate.
    
    >>> order_by_ht_rate(SAMPLE_DATA)
    ['Elms-Old Rexdale', 'Rexdale-Kipling', 'Thistletown-Beaumond Height\
s', 'West Humber-Clairville', 'Mount Olive-Silverstone-Jamestown']
    >>> order_by_ht_rate(SAMPLE_DATA2)
    ['Milliken', 'Centennial Scarborough', 'Highland Creek', 'Rouge', 'Malvern']
    """
    htlist = []
    for item in data:
        htlist.append(get_age_standardized_ht_rate(data, item))
    htlist.sort()
    for item in data:
        value = get_age_standardized_ht_rate(data, item)
        i = 0
        while i < len(htlist):
            if htlist[i] == value:
                htlist[i] = item
            i = i + 1
    return htlist
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Using the small data files
    small_data = {}

    # Add hypertension data
    ht_file = open("hypertension_data_small.csv")
    get_hypertension_data(small_data, ht_file)
    ht_file.close()

    # Add low income data
    li_file = open("low_income_small.csv")
    get_low_income_data(small_data, li_file)
    li_file.close()

    # Created dictionary should be the same as SAMPLE_DATA
    print(small_data == SAMPLE_DATA)
