# written by:
# assisted by:
# debugged by: All members
# python3

"""
Get three kinds of indicators (ROC, OBV, MACD) and save them into csv file.

"""

from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import json, time


def ROCIndicator(StockName):
    ti = TechIndicators(key='GKLC3DF23TMWX8LS', output_format='pandas')
    time.sleep(15)  # The alpha_ventage API limit 5 calls per minute
    data, meta_data = ti.get_roc(symbol=StockName, interval='1min', time_period=60, series_type='close')
    # realdata = data.to_json(orient='table')
    # print(realdata)

    # json_path = './' + StockName +'ROC.json'
    # with open(json_path, "w") as f:
    # 	json.dump(realdata, f)
    # 	print("Complete...")

    # print(type(data))
    # # print(data)
    # data.plot()

    # plt.title('ROC indicator for '+ StockName+ ' stock (1 min)')
    # fig = plt.gcf()
    # plt.savefig("ROC.pdf")
    # plt.show()
    data.to_csv(StockName + '_ROC.csv', index=True, sep=',')

    print('Success')


def OBVIndicator(StockName):
    ti = TechIndicators(key='GKLC3DF23TMWX8LS', output_format='pandas')
    time.sleep(15)  # The alpha_ventage API limit 5 calls per minute
    data, meta_data = ti.get_obv(symbol=StockName, interval='1min')
    # realdata = data.to_json(orient='table')

    # json_path = './' + StockName +'OBV.json'
    # with open(json_path, "w") as f:
    # 	json.dump(realdata, f)
    # 	print("Complete...")

    # data.plot()

    # plt.title('OBV indicator for '+ StockName+ ' stock (1 min)')
    # fig = plt.gcf()
    # plt.savefig("OBV.pdf")
    # plt.show()
    data.to_csv(StockName + '_OBV.csv', index=True, sep=',')

    print('Success')



def MACDIndicator(StockName):
    ti = TechIndicators(key='GKLC3DF23TMWX8LS', output_format='pandas')
    time.sleep(15)  # The alpha_ventage API limit 5 calls per minute
    data, meta_data = ti.get_macd(symbol=StockName, interval='1min', series_type='close')
    # realdata = data.to_json(orient='table')
    # print(realdata)

    # # data.plot()
    # json_path = './' + StockName +'MACD.json'
    # with open(json_path, "w") as f:
    # 	json.dump(realdata, f)
    # 	print("Complete...")

    # plt.title('MACD indicator for '+ StockName+ ' stock (1 min)')
    # fig = plt.gcf()
    # plt.savefig("MACD.pdf")
    # plt.show()
    data.to_csv(StockName + '_MACD.csv', index=True, sep=',')

    print('Success')


def main():
    companyNameList = ["FB", "MSFT", "AMZN", "GOOG", "AAPL", "GE", "UBER", "SBUX", "COKE", "NKE"]
    for com in companyNameList:
        ROCIndicator(com)
        OBVIndicator(com)
        MACDIndicator(com)


if __name__ == '__main__':
    main()
