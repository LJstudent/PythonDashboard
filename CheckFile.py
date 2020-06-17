import datetime


now = datetime.datetime.now()
list = []
list_of_years = [int(now.year -1), int(now.year - 2), int(now.year -3), int(now.year -4), int(now.year -5)]
list_of_years_stock = []


def dividend(Dividend):

    list.clear()
    list_of_years_stock.clear()

    for item in Dividend:
        thisdict = {
            "date":item['date'],
            "divi":item['adjDividend']
        }
        list.append(thisdict)

    totalDiv = 0
    for s in list:
        list_of_years_stock.append(int(s.get("date")[0:4]))
        if int(now.year - 1) == int(s.get("date")[0:4]):
            div = s.get("divi")
            totalDiv+=div

    result = all(elem in list_of_years_stock for elem in list_of_years)



    enddict = {
        "dividend": float("{0:.2f}".format(totalDiv)),
        "5year": str(result),
    }

    return enddict
