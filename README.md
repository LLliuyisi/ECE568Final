# ECE568Final
Final Project of Rutgers ECE568: Stock Prices Prediction

Group 8: Xiao Liu, Yujia Fan, Tien-Chi Lee, Haodong Lu 

Dictionary Description: 
-> “app” : contains back-end and front-end files. Inside the “app” file, it contains flask, ANN predictor, LSTM predictor, SVM predictor and the Indicator function. Flask is used to do the registration and login in. When user want to apply for a new account, we will save his Email and corresponding password into the MySQL table: “user”. And also create a table using the email of user to save the company he/she like. It also contains the whole project of the web service. Below is the description of our web service.

For routes.py:
  ->index(): The index page showing availalbe companies.

  ->login(): The login page where user logs in our resgister as new user.

  ->logout(): Log out current user and redirects to log in page.

  ->register(): Register new user and save to user table in database.

  ->query(): Using sql queries to obtain the listed requirements.

  ->realtime(company): Get real time data of a certain company from database and render on webpage.

  ->historical(company): Get history data of a certain company from database and render on webpage.

  ->predictions(company): Predicts the stock price of a certain company next day using 3 methods lstm, svm and bayesian curve fitting.

  ->portfolio(): Supports the user to add (redirect to revise) or delete (redirect to delete) stock to favorite. Also shows the current favorite stocks.

  ->indicators(company): Show the 3 indicators roc, obv, and macd of a certain company.

  ->revise():User can input desired stock to be added to favorite. Existing stock will result in a success. Non-existing or already included stocks will result in an error.If successful, add the user/stock pair to the portfolio table.

  ->delete(company, userid): Remove the user/stock pair from portvolio table upon remove action.

Programming language: Python 3.7
IDE:Pycharm
Framework:Flask

The folder contains both the source code of the web service interface and the whole web project of the web interface.
The file "routes.py" contains all the Get functions along with the URL of Restful functions. The functions respond to different client requests by calling the specific URL/path. Then it gives the response to the client with the specific message the client requested before in JSON format files. We implement the query functions to fully satisfy the Query functions on the final project requirement, such as show the list of all companies in the database along with their latest price. Besides, in order to draw the stock history/real price diagrams, we implement the functions to return the JSON files containing the history/real-time stock information to the clients. And the basic functions include all the query functions in final project requirement. Also, in order to draw the stock history/real price diagrams, we implement the functions to return the JSON files containing the history/real-time stock information to the clients.

Run our project, make sure you already install all the packages, otherwise use pip to install it. Change the chrome driver path in our code with yours.

The file Stock Data contains 10 companies’ stock information.The real time data contains the latest day’s price and the time slice between two real-time points is about 1 minutes.
