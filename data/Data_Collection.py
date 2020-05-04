from alpha_vantage.timeseries import TimeSeries
import pymysql.cursors
import pymysql
import csv
import time

def getRealtime(StockName):
    time.sleep(15) # The alpha_ventage API limit 5 calls per minute
    ts = TimeSeries(key='GKLC3DF23TMWX8LS', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol=StockName, interval='1min', outputsize='full')

    # data is a dataframe which needs to be converted into a csv file
    data.to_csv(StockName + '_Realtime.csv', index=True, sep=',')
    insertDatabase(StockName + '_Realtime')
    print(StockName+' realtime information is retrieved and stored in database.')

def getHistorical(StockName):
    time.sleep(15) # The alpha_ventage API limit 5 calls per minute
    ts = TimeSeries(key='GKLC3DF23TMWX8LS', output_format='pandas')
    data, meta_data = ts.get_daily(symbol=StockName, outputsize='full')

    # data is a dataframe which need to be converted into a csv file
    data.to_csv(StockName + '_Historical.csv', index=True, sep=',')
    insertDatabase(StockName + '_Historical')
    print(StockName+' historical information is retrieved and stored in database.')





def insertDatabase(TableName):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 passwd='123',
                                 db='mydb',
                                 port=3306,
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS " + TableName + ";")
            sql = """
                    CREATE TABLE """ + TableName + """(
			        time varchar(30) NOT NULL,
			        open varchar(15) NOT NULL,
                    high varchar(15) NOT NULL,
                    low varchar(15) NOT NULL,
                    close varchar(15) NOT NULL,
                    volume varchar(20) NOT NULL,
                    PRIMARY KEY (time))
                
			        ENGINE = InnoDB;"""
            csv_reader = csv.reader(open(TableName + '.csv', encoding='utf-8'))
            cursor.execute(sql)
            flag = 0
            # for row in range(0, 365):
            # i = 1
            for row in csv_reader:
                if flag != 0:
                    ROWstr = ''
                    ROWstr = (ROWstr + '"%s"' + ',') % (row[0])
                    ROWstr = (ROWstr + '"%s"' + ',') % (row[1])
                    ROWstr = (ROWstr + '"%s"' + ',') % (row[2])
                    ROWstr = (ROWstr + '"%s"' + ',') % (row[3])
                    ROWstr = (ROWstr + '"%s"' + ',') % (row[4])
                    ROWstr = (ROWstr + '"%s"' + ',') % (row[5])
                    cursor.execute("INSERT INTO %s VALUES (%s)" % (TableName, ROWstr[:-1]))
                # i = i + 1
                flag = flag + 1

        connection.commit()
    except pymysql.Error as e:
        print('Mysql Error %d: %s' % (e.args[0], e.args[1]))

    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    StocksList = ['FB', 'MSFT', 'AMZN', 'GOOG', 'BRKB', 'AAPL', 'GE', 'UBER', 'SBUX', 'COKE']
    for stock in StocksList:
        getRealtime(stock)
        getHistorical(stock)
