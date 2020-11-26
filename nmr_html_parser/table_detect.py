from nmr_html_parser import souping
import re
def table_detect(soup, d2list, float_d2list):
    """Takes soup object, 2dlist of column cells, 2dlist of cell floats. Uses regex/string arguments and calculates float averages to detect and return table type"""
    # TODO: If use this, can do soup.find("th",string=re.compile("δ")).find("sub",string=re.compile("C"))
    Carbon = soup.find("sub", string=re.compile("C"))
    Proton = soup.find("sub", string=re.compile("H"))
    if Carbon and Proton:
        return "Both H1/C13 NMR Table Detected!"
    elif Carbon:
        return "C13 NMR Table Detected!"
    elif Proton:
        return "H1 NMR Table Detected!"
    else:
        for item in d2list:
            for value in item:
                if re.search(
                    r"(\d*[0-9]\.\d*[0-9]\,\s{1}\w*[s,t,d,m,q,b,r]\s{1})|(\([0-9]+\.[0-9]\)|\([0-9]+\.[0-9](?:\,\s{1}[0-9]+\.[0-9])*\))",
                    value,
                ):
                    HNMR_Search = True
                elif re.search(
                    r"(\d*[0-9]\.\d*[0-9])(\,\sCH3|\,\sCH2|\,\sCH|\,\sC)", value
                ):
                    CNMR_Search = True
                else:
                    continue
        if HNMR_Search and CNMR_Search:
            return "Both H1/C13 NMR Detected! - From Cells!"
        elif HNMR_Search and not CNMR_Search:
            return "H1 NMR Detected! -  From Cells!"
        elif CNMR_Search and not HNMR_Search:
            return "H1 NMR Table Detected! - From cells"
        else:
            average_list = []
            for item in float_d2list:
                value_list = []
                for value in item:
                    if type(value) == float:
                        value_list.append(value)
                if souping.all_same(value_list) == False:
                    average = sum(value_list) / len(value_list)
                    average_list.append(average)
                    print(average_list)
                    if 14.0 <= average <= 250.0:
                        CNMR = True
                        continue
                    elif 0.0 <= average <= 13.5:
                        HNMR = True
                        continue
            if CNMR and HNMR == True:
                return "Both H1/C13 NMR Detected! - From chemical shifts!"
            elif HNMR and not CNMR:
                return "H1 NMR Detected! -  From chemical shifts!"
            elif CNMR and not HNMR:
                return "H1 NMR Table Detected! - From chemical shifts!"
            else:
                return None