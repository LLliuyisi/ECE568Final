# written by: ZE LIU
# assisted by: Xinyu Lyu
# debugged by: All members

from sklearn import svm
import pandas as pd
from sqlalchemy import create_engine



def SVMPredict(StockName):
	engine = create_engine('mysql+pymysql://root:123@localhost:3306/stocks')

	df = pd.read_sql_query(
		'SELECT * FROM (SELECT * FROM ' + StockName + '_Historical ORDER BY time DESC LIMIT 100) as com ORDER BY time ASC;',
		engine)
	newData = df.values.T.tolist()

	# print('time: %s' % (newData[0]))
	# newData is a list of the history price and we choose only close price
	ClosePrice = newData[4]
	for i in range(0, len(ClosePrice)):
		ClosePrice[i] = float(ClosePrice[i])

	# print(StockName + ' Last Day Value: %s' % (ClosePrice[-1]))
	BigTimeData = []
	i = 1
	for r in range(0,len(ClosePrice)):
		SmallTimeData = [i]
		BigTimeData.append(SmallTimeData)
		i = i + 1

	clf = svm.SVR()
	NextDay = [[len(ClosePrice)]]
	# print('NextDay: %s' % (NextDay))
	# clf.fit(X, y) 
	clf.fit(BigTimeData, ClosePrice) 
	# SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
	#     kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
	Result = clf.predict(NextDay)
	return Result[0]


def main():
	companyNameList = ['FB', 'MSFT', 'AMZN', 'GOOG', 'NKE', 'AAPL', 'GE', 'UBER', 'SBUX', 'COKE']
	# companyNameList = ['FB']
	for com in companyNameList:
		res=SVMPredict(com)
		print(com + " Next Day Value: %s" % (res))

if __name__ == '__main__':
	main()