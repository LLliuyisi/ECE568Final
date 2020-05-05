# written by: ZE LIU
# assisted by: Xinyu Lyu
# debugged by: All members

from sklearn import svm
import csv
from sqlalchemy import create_engine
import pandas as pd
import json


def SVMPredict(StockName):
	engine = create_engine('mysql+pymysql://root:123@localhost:3306/stocks')
	df = pd.read_sql_query('SELECT * FROM '+StockName+'_Historical order by time', engine)
	newData = df.values.T.tolist()

	print('time: %s' % (newData[0]))
	# newData is a big list of the history price and we only need close price now
	ClosePrice = newData[4]
	for i in range(0, len(ClosePrice)):
		ClosePrice[i] = float(ClosePrice[i])
	
	print('Close: %s' % (ClosePrice))
	BigTimeData = []
	i = 1
	for r in range(0,len(ClosePrice)):
		SmallTimeData = [i]
		BigTimeData.append(SmallTimeData)
		i = i + 1

	# X = [[0], [2]]
	# y = [0.5, 2.5]
	# NextDay = [[1]]
	clf = svm.SVR()
	NextDay = [[len(ClosePrice)]]
	# clf.fit(X, y) 
	clf.fit(BigTimeData, ClosePrice) 
	# SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
	#     kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
	Result = clf.predict(NextDay)

	return Result


def main():
    # companyNameList = ['FB', 'MSFT', 'AMZN', 'GOOG', 'NKE', 'AAPL', 'GE', 'UBER', 'SBUX', 'COKE']
    companyNameList = ['FB']
    # print("Please input the company name: ")
    # name = input()
    # SVMPredict(name)
    for com in companyNameList:
    	print(com + " Next Day Value: %s" % (SVMPredict(com)))

if __name__ == '__main__':
	main()