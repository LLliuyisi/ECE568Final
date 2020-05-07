import numpy as np
import math
import pandas as pd
from sqlalchemy import create_engine


def baysian_curve_fitting(StockName):
    engine = create_engine('mysql+pymysql://root:123@localhost:3306/mydb')
    df = pd.read_sql_query(
        'SELECT * FROM (SELECT * FROM ' + StockName + '_Historical ORDER BY time DESC LIMIT 100) as com ORDER BY time ASC;',
        engine)
    newData = df.values.T.tolist()
    time, price = [], []


    date = 0
    for data in newData:
        if date > 0 and data[4] is not None:
            # Encode the date into integer from 1 ~ 30
            # skip the 1st row: titles of columns
            time.append(date)
            price.append(float(data[1]))
        date += 1
    test_val = time[-1]

    M = 4
    beta = 12
    alpha = 0.1

    # Calculate 𝜑T(x)
    a = [[math.pow(test_val, i) for i in range(M + 1)]]
    matrix_a = np.matrix(a)

    # Calculate alpha * I
    I = [[0 for _ in range(M + 1)] for _ in range(M + 1)]
    for i in range(M + 1):
        I[i][i] = alpha
    matrix_I = np.matrix(I)

    # Calculate sum-𝜑(xn)
    b = [[0] for _ in range(M + 1)]
    for j in range(len(time) - 1):
        for i in range(M + 1):
            b[i][0] += math.pow(time[j], i)
    matrix_b = np.matrix(b)

    # Calculate Matrix S
    matrix_S_1 = matrix_b * matrix_a * beta + matrix_I
    matrix_S = np.linalg.inv(matrix_S_1)

    # Calculate sum-[𝜑(xn)*tn]
    c = [[0] for _ in range(M + 1)]
    for i in range(len(time) - 1):
        for j in range(M + 1):
            c[j][0] += (math.pow(time[i], j) * price[i])
    matrix_c = np.matrix(c)

    # Calculate mean
    mean_matrix = matrix_a * matrix_S * matrix_c * beta
    mean = mean_matrix.item(0)

    # Calculate 𝜑(x)
    d = [[0] for _ in range(M + 1)]
    for i in range(M + 1):
        d[i][0] = math.pow(test_val, i)
    matrix_d = np.matrix(d)

    # Calculate variance
    variance = math.sqrt((matrix_a * matrix_S * matrix_d)[0][0] + (1 / beta))


    # print("Predicted Val   : {:.4f}".format(mean))
    # print("Actual Val      : {:.4f}".format(price[-1]))
    # print("Range Prediction : [{:.4f}, {:.4f}]".format(mean - 3 * variance, mean + 3 * variance))
    # print("Absolute Error  : {:.4f}".format(abs(price[-1] - mean)))
    # print("Relative Error  : {:.4f}%".format(abs(price[-1] - mean) / price[-1] * 100))
    return mean




if __name__ == "__main__":
    companyNameList = ['FB', 'MSFT', 'AMZN', 'GOOG', 'NKE', 'AAPL', 'GE', 'UBER', 'SBUX', 'COKE']
    for com in companyNameList:
        print(com + " Next Day Value: %s" % (baysian_curve_fitting(com)))
