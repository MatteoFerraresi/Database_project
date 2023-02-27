#IMPORT THE LIBRARIES
import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
import os
pd.set_option('max_colwidth', -1)

#READ THE DATASET
df_order_details=pd.read_csv('order_details.csv')
df_order=pd.read_csv('orders.csv')
df_pizza_types=pd.read_csv('pizza_types.csv',encoding='unicode_escape')
df_pizzas=pd.read_csv('pizzas.csv')

#CREATE THE DATABASE
db_name='pizza_place_database'
try:
    mydb = mysql.connect(host='localhost', user='MatteoFerraresi', password='MySQL2022.', auth_plugin='mysql_native_password') # you can add the auth_plugin here too (ref line 26)
    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute('SHOW DATABASES')
        result = mycursor.fetchall()
        print(result)
        for x in result:
            if db_name == x[0]:
                mycursor.execute('DROP DATABASE ' + db_name) # delete old database
                mydb.commit() # make the changes official
                print("The database already exists! The old database has been deleted!)")
        
        mycursor.execute("CREATE DATABASE "+ db_name)
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)

mycursor.execute("USE " + db_name)  #USE THE DATABASE

### CREATE ALL THE TABLES
mycursor.execute(
      '''
        CREATE TABLE Orders (
            order_id INTEGER PRIMARY KEY,
            date DATE,
            time TIME
        );
      '''
      )

mycursor.execute("DESC Orders ")
result_orders = mycursor.fetchall()
print(result_orders)

mycursor.execute(
      '''
        CREATE TABLE Pizza_types (
          pizza_type_id VARCHAR(50) PRIMARY KEY,
          name VARCHAR(50),
          category VARCHAR(50),
          ingredients VARCHAR(250)
        );
      '''
      )
      
mycursor.execute("DESC Pizza_types ")
result_pizza_types = mycursor.fetchall()
print(result_pizza_types)

mycursor.execute(
      '''
        CREATE TABLE Pizzas (
          pizza_id VARCHAR(50) PRIMARY KEY,
          pizza_type_id VARCHAR(50), 
          size VARCHAR(3),
          price FLOAT,
          FOREIGN KEY(pizza_type_id) REFERENCES Pizza_types(pizza_type_id)
        );
      '''
      )

mycursor.execute("DESC Pizzas ")
result_pizzas = mycursor.fetchall()
print(result_pizzas)

mycursor.execute(
      '''
        CREATE TABLE Orders_details (
          orders_details_id INTEGER,
          order_id INTEGER,
          pizza_id VARCHAR(50),
          quantity VARCHAR(3),
          PRIMARY KEY(orders_details_id),
          FOREIGN KEY(order_id) REFERENCES Orders(order_id),
          FOREIGN KEY(pizza_id) REFERENCES Pizzas(pizza_id)
        );
      '''
      )

mycursor.execute("DESC Orders_details ")
result_Orders_details = mycursor.fetchall()
print(result_Orders_details)


### INSERT DATA IN EACH TABLE

for i,row in df_order.iterrows():
    sql = "INSERT IGNORE INTO pizza_place_database.Orders VALUES (%s,%s,%s)"
    mycursor.execute(sql, tuple([row['order_id'], row['date'], row['time']]))
    mydb.commit()

mycursor.execute("SELECT * FROM Orders")
result = mycursor.fetchall()
#print(result)

for i,row in df_pizza_types.iterrows():
    sql = "INSERT IGNORE INTO pizza_place_database.Pizza_types VALUES (%s,%s,%s,%s)"
    mycursor.execute(sql, tuple([row['pizza_type_id'], row['name'], row['category'], row['ingredients']]))
    mydb.commit()

mycursor.execute("SELECT * FROM Pizza_types")
result = mycursor.fetchall()
print(result)

for i,row in df_pizzas.iterrows():
    sql = "INSERT IGNORE INTO pizza_place_database.Pizzas VALUES (%s,%s,%s,%s)"
    mycursor.execute(sql, tuple([row['pizza_id'], row['pizza_type_id'], row['size'], row['price']]))
    mydb.commit()

mycursor.execute("SELECT * FROM Pizzas")
result = mycursor.fetchall()
print(result)

for i,row in df_order_details.iterrows():
    sql = "INSERT INTO pizza_place_database.Orders_details VALUES (%s,%s,%s,%s)"
    mycursor.execute(sql, tuple([row['order_details_id'], row['order_id'], row['pizza_id'], row['quantity']]))
    mydb.commit()

mycursor.execute("SELECT * FROM Orders_details")
result = mycursor.fetchall()
#print(result)