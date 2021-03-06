#  written by:
#  assisted by:
#  debugged by:

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from sqlalchemy import create_engine
import json
from keras.models import load_model


def LSTMPredict(Stockname):
    # FOR REPRODUCIBILITY
    np.random.seed(7)

    engine = create_engine('mysql+pymysql://root:123@localhost:3306/stocks')

    df = pd.read_sql_query(
        'SELECT * FROM (SELECT * FROM ' + Stockname + '_Historical ORDER BY time DESC LIMIT 100) as com ORDER BY time ASC;', engine)
    newData = df.values.T.tolist()
    print(newData[0])
    ClosePrice = newData[4]
    print(ClosePrice)
    # dataset = pd.read_csv('/Users/xiaoliu/PycharmProjects/ECE568Final2/data/' + Stockname + '_Historical.csv', usecols=[1, 2, 3, 4])
    # print(df)
    # IMPORTING DATASET
    # dataset=df[['R_Price']]
    dataset = df[['open', 'high', 'low', 'close']]
    # dataset.columns = ["open", "high", "low", "close"]
    # print(dataset)
    dataset = dataset.apply(pd.to_numeric)
    dataset = dataset.reindex(index=dataset.index[::-1])
    # CREATING OWN INDEX FOR FLEXIBILITY
    obs = np.arange(1, len(dataset) + 1, 1)

    # TAKING DIFFERENT INDICATORS FOR PREDICTION

    OHLC_avg = dataset.mean(axis=1)
    HLC_avg = dataset[['high', 'low', 'close']].mean(axis=1)
    close_val = dataset[['close']]

    # PREPARATION OF TIME SERIES DATASE
    OHLC_avg = np.reshape(OHLC_avg.values, (len(OHLC_avg), 1))  # 1664
    scaler = MinMaxScaler(feature_range=(0, 1))
    OHLC_avg = scaler.fit_transform(OHLC_avg)

    # TRAIN-TEST SPLIT
    train_OHLC = int(len(OHLC_avg) * 0.75)
    test_OHLC = len(OHLC_avg) - train_OHLC
    train_OHLC, test_OHLC = OHLC_avg[0:train_OHLC, :], OHLC_avg[train_OHLC:len(OHLC_avg), :]

    # TIME-SERIES DATASET (FOR TIME T, VALUES FOR TIME T+1)
    trainX, trainY = new_dataset(train_OHLC, 1)
    testX, testY = new_dataset(test_OHLC, 1)

    # RESHAPING TRAIN AND TEST DATA
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    step_size = 1

    # LSTM MODEL
    model = Sequential()
    model.add(LSTM(32, input_shape=(1, step_size), return_sequences=True))
    model.add(LSTM(16))
    model.add(Dense(1))
    model.add(Activation('linear'))

    # MODEL COMPILING AND TRAINING
    model.compile(loss='mean_squared_error', optimizer='adagrad')  # Try SGD, adam, adagrad and compare!!!
    model.fit(trainX, trainY, epochs=100, batch_size=1, verbose=0)
    # if verbose is 0, it will not display the process
    # model.fit(trainX, trainY, epochs=50, batch_size=1, verbose=2)
    # PREDICTION
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)

    # DE-NORMALIZING FOR PLOTTING
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform([trainY])
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform([testY])

    # TRAINING RMSE
    trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredict[:, 0]))
    # print('Train RMSE: %.2f' % (trainScore))

    # TEST RMSE
    testScore = math.sqrt(mean_squared_error(testY[0], testPredict[:, 0]))
    # print('Test RMSE: %.2f' % (testScore))

    # print(mean_absolute_error(testY[0], testPredict[:,0]))

    # CREATING SIMILAR DATASET TO PLOT TRAINING PREDICTIONS
    trainPredictPlot = np.empty_like(OHLC_avg)
    trainPredictPlot[:, :] = np.nan
    trainPredictPlot[step_size:len(trainPredict) + step_size, :] = trainPredict

    # CREATING SIMILAR DATASSET TO PLOT TEST PREDICTIONS
    testPredictPlot = np.empty_like(OHLC_avg)
    testPredictPlot[:, :] = np.nan
    testPredictPlot[len(trainPredict) + (step_size * 2) + 1:len(OHLC_avg) - 1, :] = testPredict
    avg = testPredict.mean(axis=1)
    av = avg.mean(axis=0)
    # DE-NORMALIZING MAIN DATASET
    OHLC_avg = scaler.inverse_transform(OHLC_avg)

    # PLOT OF MAIN OHLC VALUES, TRAIN PREDICTIONS AND TEST PREDICTIONS
    # plt.plot(OHLC_avg, 'g', label = 'original dataset')
    # plt.plot(trainPredictPlot, 'r', label = 'training set')
    # plt.plot(testPredictPlot, 'b', label = 'predicted stock price/test set')
    # plt.legend(loc = 'upper right')
    # plt.xlabel('Time in Days')
    # plt.ylabel('OHLC Value of Stocks')
    # plt.show()

    # PREDICT FUTURE VALUES
    last_val = testPredict[-1]
    last_val_scaled = last_val / last_val
    next_val = model.predict(np.reshape(last_val_scaled, (1, 1, 1)))
    # print ("Last Day Value:", np.asscalar(last_val))

    # print ("Next Day Value:", np.asscalar(last_val*next_val))
    # print np.append(last_val, next_val)
    # print(testScore/av)
    key = Stockname + " Next Day Value"
    json_data = {
        key: np.asscalar(last_val * next_val)
    }
    print(json_data)

    # Json result: {'Next Day Value': Price}

    # json_path = './LSTM prediction.json'
    # with open(json_path, "w") as f:
    #     json.dump(json_data, f)
    #     print("Complete...")

    # SAVE THE MODEL
    model.save("/Users/xiaoliu/PycharmProjects/ECE568Final2/models/" + Stockname + "_LSTM.h5")
    del model
    print("Saved model " + Stockname + "_LSTM to disk")


# FUNCTION TO CREATE 1D DATA INTO TIME SERIES DATASET
# THIS FUNCTION CAN BE USED TO CREATE A TIME SERIES DATASET FROM ANY 1D ARRAY
def new_dataset(dataset, step_size):
    data_X, data_Y = [], []
    for i in range(len(dataset) - step_size - 1):
        a = dataset[i:(i + step_size), 0]
        data_X.append(a)
        data_Y.append(dataset[i + step_size, 0])
    return np.array(data_X), np.array(data_Y)

def LoadLSTM(model, Stockname):
    engine = create_engine('mysql+pymysql://root:123@localhost:3306/mydb')

    df = pd.read_sql_query('SELECT * FROM (SELECT * FROM ' + Stockname + '_Historical ORDER BY time DESC LIMIT 100) as com ORDER BY time ASC;', engine)
    newData = df.values.T.tolist()
    # print(newData[0])
    ClosePrice = newData[4]
    # print(ClosePrice)
    print(Stockname + ' Last Day Value: %s' % (ClosePrice[-1]))
    # print('dataset: %s' % (dataset))

    dataset = df[['open', 'high', 'low', 'close']]
    dataset = dataset.apply(pd.to_numeric)
    dataset = dataset.reindex(index=dataset.index[::-1])
    # CREATING OWN INDEX FOR FLEXIBILITY
    obs = np.arange(1, len(dataset) + 1, 1)

    OHLC_avg = dataset.mean(axis=1)

    # PREPARATION OF TIME SERIES DATASE
    OHLC_avg = np.reshape(OHLC_avg.values, (len(OHLC_avg), 1))
    scaler = MinMaxScaler(feature_range=(0, 1))
    OHLC_avg = scaler.fit_transform(OHLC_avg)

    # TRAIN-TEST SPLIT
    train_OHLC = int(len(OHLC_avg) * 0.75)
    test_OHLC = len(OHLC_avg) - train_OHLC
    train_OHLC, test_OHLC = OHLC_avg[0:train_OHLC, :], OHLC_avg[train_OHLC:len(OHLC_avg), :]

    # TIME-SERIES DATASET (FOR TIME T, VALUES FOR TIME T+1)
    testX, testY = new_dataset(test_OHLC, 1)

    # RESHAPING TRAIN AND TEST DATA
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    step_size = 1
    # print('testX = %s' % testX)
    testPredict = model.predict(testX)
    # print('testPredict = %s' % testPredict)

    # DE-NORMALIZING
    testPredict = scaler.inverse_transform(testPredict)
    last_val = testPredict[-1]
    last_val_scaled = last_val / last_val
    next_val = model.predict(np.reshape(last_val_scaled, (1, 1, 1)))
    # print(Stockname + " Next Day Value: %f" % (np.asscalar(last_val * next_val)))
    return np.asscalar(last_val * next_val)



def main():
    companyNameList = ['FB', 'MSFT', 'AMZN', 'GOOG', 'NKE', 'AAPL', 'GE', 'UBER', 'SBUX', 'COKE']
    # companyNameList = ['FB']
    # LSTMPredict(name)
    for com in companyNameList:
        # Train models and save them
        # LSTMPredict(com) # annotate this when just using model
        # load model
        model = load_model('models/' + com + '_LSTM.h5')
        print(com + " Next Day Value: %f" % (LoadLSTM(model, com)))

if __name__ == '__main__':
    main()
