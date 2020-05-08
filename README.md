# ECE568Final
Final Project of Rutgers ECE568: Stock Prices Prediction

Group 8: Xiao Liu, Yujia Fan, Tien-Chi Lee, Haodong Lu 

Dictionary Description: 
-> “app” : contains back-end and front-end files. Inside the “app” file, it contains flask, ANN predictor, LSTM predictor, SVM predictor and the Indicator function. Flask is used to do the registration and login in. When user want to apply for a new account, we will save his Email and corresponding password into the MySQL table: “user”. And also create a table using the email of user to save the company he/she like. It also contains the whole project of the web service. Below is the description of our web service.

Programming language: Python 3.7
IDE:Pycharm
Framework:Flask

The folder contains both the source code of the web service interface and the whole web project of the web interface.
The file "routes.py" contains all the Get functions along with the URL of Restful functions. The functions respond to different client requests by calling the specific URL/path. Then it gives the response to the client with the specific message the client requested before in JSON format files. We implement the query functions to fully satisfy the Query functions on the final project requirement, such as show the list of all companies in the database along with their latest price. Besides, in order to draw the stock history/real price diagrams, we implement the functions to return the JSON files containing the history/real-time stock information to the clients. And the basic functions include all the query functions in final project requirement. Also, in order to draw the stock history/real price diagrams, we implement the functions to return the JSON files containing the history/real-time stock information to the clients.

Run our project, make sure you already install all the packages, otherwise use pip to install it. Change the chrome driver path in our code with yours.

The file Stock Data contains 10 companies’ stock information.The real time data contains the latest day’s price and the time slice between two real-time points is about 1 minutes.
