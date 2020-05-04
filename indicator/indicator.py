# written by:
# assisted by:
# debugged by: All members
# python3

"""
Get three kinds of indicators (ROC, OBV, MACD) and insert them into database.

"""
import pymysql, csv
from alpha_vantage.techindicators import TechIndicators
import matplotlib.pyplot as plt
import json, time


def ROCIndicator(StockName):
    ti = TechIndicators(key='GKLC3DF23TMWX8LS', output_format='pandas')
    time.sleep(15)  # The alpha_ventage API limit 5 calls per minute
    data, meta_data = ti.get_roc(symbol=StockName, interval='daily', series_type='close')
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

    print(StockName + '_ROC saved successfully.')
    insertDatabase(StockName + '_ROC')



def OBVIndicator(StockName):
    ti = TechIndicators(key='GKLC3DF23TMWX8LS', output_format='pandas')
    time.sleep(15)  # The alpha_ventage API limit 5 calls per minute
    data, meta_data = ti.get_obv(symbol=StockName, interval='daily')
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

    print(StockName + '_OBV saved successfully.')
    insertDatabase(StockName + '_OBV')


def MACDIndicator(StockName):
    ti = TechIndicators(key='GKLC3DF23TMWX8LS', output_format='pandas')
    time.sleep(15)  # The alpha_ventage API limit 5 calls per minute
    data, meta_data = ti.get_macd(symbol=StockName, interval='daily', series_type='close')
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

    print(StockName + '_MACD saved successfully.')
    insertDatabase(StockName + '_MACD')

def insertDatabase(com):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='123',
                                 db='mydb',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS " + com + ";")
            sql = """
                    CREATE TABLE """ + com + """ (
			        time varchar(30) NOT NULL,
			        indicator varchar(15) ,
                    PRIMARY KEY (time))
			        ENGINE = InnoDB;"""
            cursor.execute(sql)
            print('Table ' + com + 'created successfully.')

            csv_reader = csv.reader(open(com + '.csv', encoding='utf-8'))
            flag = 0
            for row in csv_reader:
                if flag != 0:
                    ROWstr = ''
                    ROWstr = (ROWstr + '"%s"' + ',') % (row[0])
                    ROWstr = (ROWstr + '"%s"' + ',') % (row[1])
                    cursor.execute("INSERT INTO %s VALUES (%s)" % (com, ROWstr[:-1]))
                flag = flag + 1
            print('Table' + com + ' data inserted successfully.')
            connection.commit()
    except pymysql.Error as e:
        print('Mysql Error %d: %s' % (e.args[0], e.args[1]))

    finally:
        cursor.close()
        connection.close()

def main():
    companyNameList = ["FB", "MSFT", "AMZN", "GOOG", "AAPL", "GE", "UBER", "SBUX", "COKE", "NKE"]
    for com in companyNameList:
        ROCIndicator(com)
        OBVIndicator(com)
        MACDIndicator(com)



if __name__ == '__main__':
    main()
