def find_values_from_dict(numbers, number_map):
    # Initialize a list to hold the results
    results = []
    
    # Iterate through each number in the list of numbers
    for num in numbers:
        # Check if the number is in the dictionary
        if str(num) in number_map:
            # If yes, append the associated value to the results list
            results.append((str(num), number_map[str(num)]))
        else:
            # If no, append a message indicating the number is not in the dictionary
            results.append((str(num), "Not in dictionary"))
    return results


def findDic(indices: list):

    # Dictionary of numbers and their corresponding values
    with open('DataForOPL- camera mapping.json', '+r') as camera_file:
        data = camera_file.read()
        import json
        number_map = json.loads(data)

    # print(number_map)

    # number_map = {"0": 42, "1": 43, "2": 44, "3": 45, "4": 46, "5": 47, "6": 48, "7": 49, "8": 50, "9": 51, "10": 52, "11": 53, "12": 54, "13": 55, "14": 56, "15": 57, "16": 58, "17": 59, "18": 60, "19": 61, "20": 62, "21": 63, "22": 64, "23": 65, "24": 66, "25": 67, "26": 68, "27": 69, "28": 70, "29": 71, "30": 72, "31": 73, "32": 74, "33": 75, "34": 76, "35": 77, "36": 78, "37": 79, "38": 82, "39": 119, "40": 122, "41": 159, "42": 162, "43": 199, "44": 202, "45": 239, "46": 242, "47": 279, "48": 282, "49": 319, "50": 322, "51": 359, "52": 362, "53": 399, "54": 402, "55": 439, "56": 442, "57": 479, "58": 482, "59": 519, "60": 522, "61": 559, "62": 562, "63": 599, "64": 602, "65": 639, "66": 642, "67": 679, "68": 682, "69": 719, "70": 722, "71": 759, "72": 762, "73": 799, "74": 802, "75": 839, "76": 842, "77": 879, "78": 882, "79": 919, "80": 922, "81": 959, "82": 962, "83": 999, "84": 1002, "85": 1039, "86": 1042, "87": 1079, "88": 1082, "89": 1119, "90": 1122, "91": 1159, "92": 1162, "93": 1199, "94": 1202, "95": 1239, "96": 1242, "97": 1279, "98": 1282, "99": 1319, "100": 1322, "101": 1359, "102": 1362, "103": 1399, "104": 1402, "105": 1439, "106": 1442, "107": 1479, "108": 1482, "109": 1519, "110": 1522, "111": 1559, "112": 1562, "113": 1599, "114": 1602, "115": 1639, "116": 1642, "117": 1679, "118": 1682, "119": 1719, "120": 1722, "121": 1759, "122": 1762, "123": 1799, "124": 1802, "125": 1839, "126": 1842, "127": 1879, "128": 1882, "129": 1919, "130": 1922, "131": 1959, "132": 1962, "133": 1999, "134": 2002, "135": 2039, "136": 2042, "137": 2079, "138": 2082, "139": 2086, "140": 2087, "141": 2088, "142": 2089, "143": 2090, "144": 2091, "145": 2092, "146": 2093, "147": 2094, "148": 2095, "149": 2096, "150": 2097, "151": 2098, "152": 2099, "153": 2100, "154": 2101, "155": 2102, "156": 2103, "157": 2104, "158": 2105, "159": 2106, "160": 2107, "161": 2108, "162": 2109, "163": 2110, "164": 2111, "165": 2112, "166": 2113, "167": 2114, "168": 2115, "169": 2116, "170": 2119, "171": 2122, "172": 2126, "173": 2127, "174": 2128, "175": 2129, "176": 2130, "177": 2131, "178": 2132, "179": 2133, "180": 2134, "181": 2135, "182": 2136, "183": 2137, "184": 2138, "185": 2139, "186": 2140, "187": 2141, "188": 2142, "189": 2143, "190": 2144, "191": 2145, "192": 2146, "193": 2147, "194": 2148, "195": 2149, "196": 2150, "197": 2151, "198": 2152, "199": 2153, "200": 2154, "201": 2155, "202": 2156, "203": 2159, "204": 2162, "205": 2167, "206": 2168, "207": 2169, "208": 2170, "209": 2171, "210": 2172, "211": 2173, "212": 2174, "213": 2175, "214": 2176, "215": 2177, "216": 2178, "217": 2179, "218": 2180, "219": 2188, "220": 2189, "221": 2190, "222": 2191, "223": 2192, "224": 2193, "225": 2194, "226": 2195, "227": 2199, "228": 2202, "229": 2207, "230": 2208, "231": 2209, "232": 2210, "233": 2211, "234": 2212, "235": 2213, "236": 2214, "237": 2215, "238": 2216, "239": 2217, "240": 2218, "241": 2219, "242": 2220, "243": 2221, "244": 2239, "245": 2242, "246": 2247, "247": 2260, "248": 2261, "249": 2263, "250": 2279, "251": 2282, "252": 2287, "253": 2300, "254": 2301, "255": 2303, "256": 2319, "257": 2322, "258": 2327, "259": 2340, "260": 2341, "261": 2343, "262": 2359, "263": 2362, "264": 2367, "265": 2380, "266": 2381, "267": 2383, "268": 2399, "269": 2402, "270": 2407, "271": 2421, "272": 2423, "273": 2439, "274": 2442, "275": 2447, "276": 2479, "277": 2482, "278": 2487, "279": 2519, "280": 2522, "281": 2527, "282": 2546, "283": 2548, "284": 2559, "285": 2562, "286": 2567, "287": 2585, "288": 2586, "289": 2588, "290": 2599, "291": 2602, "292": 2607, "293": 2625, "294": 2626, "295": 2628, "296": 2639, "297": 2642, "298": 2647, "299": 2665, "300": 2666, "301": 2668, "302": 2679, "303": 2682, "304": 2687, "305": 2705, "306": 2706, "307": 2708, "308": 2719, "309": 2722, "310": 2727, "311": 2745, "312": 2746, "313": 2748, "314": 2759, "315": 2762, "316": 2767, "317": 2785, "318": 2786, "319": 2788, "320": 2799, "321": 2802, "322": 2807, "323": 2825, "324": 2826, "325": 2828, "326": 2839, "327": 2842, "328": 2847, "329": 2865, "330": 2866, "331": 2868, "332": 2879, "333": 2882, "334": 2887, "335": 2888, "336": 2889, "337": 2890, "338": 2891, "339": 2892, "340": 2893, "341": 2894, "342": 2895, "343": 2896, "344": 2897, "345": 2898, "346": 2899, "347": 2900, "348": 2901, "349": 2902, "350": 2903, "351": 2904, "352": 2905, "353": 2906, "354": 2908, "355": 2919, "356": 2922, "357": 2959, "358": 2962, "359": 2999, "360": 3002, "361": 3039, "362": 3042, "363": 3079, "364": 3082, "365": 3119, "366": 3122, "367": 3123, "368": 3124, "369": 3125, "370": 3126, "371": 3127, "372": 3128, "373": 3129, "374": 3130, "375": 3131, "376": 3132, "377": 3133, "378": 3134, "379": 3135, "380": 3136, "381": 3137, "382": 3138, "383": 3139, "384": 3140, "385": 3141, "386": 3142, "387": 3143, "388": 3144, "389": 3145, "390": 3146, "391": 3147, "392": 3148, "393": 3149, "394": 3150, "395": 3151, "396": 3152, "397": 3153, "398": 3154, "399": 3155, "400": 3156, "401": 3157, "402": 3158, "403": 3159}

    # Input from user, split by commas and stripped of extra spaces
    # user_input = input("Enter numbers separated by commas (e.g., 5, 7, 22): ")
    # numbers = [num.strip() for num in user_input.split(",")]

    # Get the values from the dictionary for the input numbers
    result = find_values_from_dict(indices, number_map)

    # Print the results
    for num, value in result:
        print(f"Number {num}: {value}")

    return result

