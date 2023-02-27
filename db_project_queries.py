import mysql.connector as mysql
import time
import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



mydb = mysql.connect(host='localhost', user='MatteoFerraresi', password='MySQL2022.', auth_plugin='mysql_native_password')
if mydb.is_connected():
        mycursor = mydb.cursor()
mycursor.execute("USE pizza_place_database")    

def load_data(dataset_1: str, dataset_2: str, dataset_3: str, dataset_4: str):
	print("I loaded the dataset and built the database!\n")
	# dump the database to a file
	pass 




def query_1():
    os.system('cls')
    max_price = input("\nPlease provide a maximum price: ")
	
	
    mycursor.execute(f'''select distinct pt.name, p.size, p.price from pizza_types as pt, pizzas as p where p.price < {max_price} and p.pizza_type_id = pt.pizza_type_id''')
	
    result=mycursor.fetchall()
    if result == []:
        result = [None]
    print(f"\nthe names and sizes of the pizzas with price smaller than '{max_price}' $ are: ")
    time.sleep(2)
    for row in result:
        print(row)
    time.sleep(3)




def query_2():
	os.system('cls')
	size = input("\nplease provide a size between S, M, L, XL, XLL: ")
	max_price = input("\nplease provide a maximum price: ")
	min_price = input("\nplease provide a minimum price: ")

	mycursor.execute(f'''SELECT DISTINCT name
                    FROM Pizza_types 
                    WHERE pizza_type_id IN
					                (SELECT pizza_type_id FROM pizzas WHERE size ='{size}' AND price BETWEEN {min_price} AND {max_price})''')

	result = mycursor.fetchall()
	if result == []:
		result = [None]
	print(f"\nthe name of the pizzas with size {size} and price between {min_price} and {max_price} are: \n")
	time.sleep(2)
	for row in result:
		print(row)
	time.sleep(3)




def query_3():
	os.system('cls')
	order = input('\nplease provide an order number (between 1 and 21350): ')

	mycursor.execute(f'''select od.pizza_id, od.quantity, o.date from orders_details as od, orders as o where od.order_id = {order} and o.order_id = {order}''')

	result = mycursor.fetchall()
	if result == []:
		result = [None]
	print(f"\nthe info about the order number {order} are: \n")
	time.sleep(2)
	for row in result:
		print(row)
	time.sleep(3)




def query_4():
	os.system('cls')
	ingredient = input('\nplease provide an ingredient you are interested in: ')
	ingredient = str(ingredient)
	mycursor.execute(f''' SELECT name, ingredients, CHAR_LENGTH(ingredients)+1 - CHAR_LENGTH(REPLACE(ingredients, ',', SPACE(LENGTH(',')-1))) AS 'number of ingredients' FROM pizza_types WHERE ingredients LIKE '%{ingredient}%' ''')

	result = mycursor.fetchall()
	if result == []:
		result = [None]
	print(f"\nthe name, ingredients and number of ingredients of pizzas having {ingredient} are: \n")
	time.sleep(2)
	for row in result:
		print(row)
	time.sleep(3)




def query_5():
    os.system('cls')
    order = input('\nselect the order of which you want to know the total bill (from 1 to 21350): ')
    mycursor.execute(f''' select distinct od.pizza_id, p.price 
	from orders_details as od, pizzas as p
	where od.order_id = '{order}' and od.pizza_id = p.pizza_id''')
    result = mycursor.fetchall()
    print(f"the bill having order number {order} is : ")
    time.sleep(2)
    for row in result:
        print(row)
    total_bill= sum(tup[1] for tup in result)
    time.sleep(2)
    print(f"\n the total cost of order number {order} is: {total_bill} $")




def query_6():
	os.system('cls')
	input_ = input('scatter(1) or boxplot(2)?: ')
	if input_ == '1':
		os.system('cls')
		mycursor.execute(f'''select pizza_id, price from pizzas''')
		result = [(x[0], x[1]) for x in mycursor]
		df = pd.DataFrame(result, columns=['pizza_id', 'price'])
		print(df.to_string)
		sns.scatterplot(data=df, x='pizza_id', y='price')
		plt.show()
	elif input_ == '2':
		os.system('cls')
		mycursor.execute(f'''select price from pizzas''')
		result = [x for x in mycursor]
		#print(result)
		df = pd.DataFrame(result, columns=['price'])
		print(df.to_string)
		plt.boxplot(df)
		plt.show()
	else:
		print('wrong input, try again')
		time.sleep(2)





# MAIN
if __name__ == "__main__":
	print("Welcome to our project!\n")
	load_data("order_details.csv", "orders.csv", "pizza_types.csv", "pizzas.csv")

	valid_choices = ['1', '2', '3', '4', '5', '6', 'quit']
	print('We implemented a few queries:')
	
	while True:
		time.sleep(2)
		choice = input('''\nChoose a query to execute by typing '1', '2', '3', '4', '5', '6' or type 'quit' to quit.\n
'1' -> Get all the pizza's names, sizes and prices with price greater than a given value
'2' -> Get the name for a pizza given a size and a price range
'3' -> Get all the id's of the pizzas ordered, the quantities and the date they were ordered in given an order number
'4' -> Get all the ingredients, the name of a pizza and the number of ingredients given the name of one ingredient
'5' -> Get the bill and the total cost for a given order
'6' -> Obtain a boxplot or a scatterplot of all the prices of pizzas 
 > ''')


		if choice not in valid_choices:
			print(f"Your choice '{choice}' is not valid. Please retry")
			continue

		if choice == "quit":
			os.system('cls')
			print("\nGoodbye!\n")
			time.sleep(2)
			break

		print(f"\nYou chose to execute query {choice}")
		if choice == '1':
			query_1()
		elif choice == '2':
			query_2()
		elif choice == '3':
			query_3()
		elif choice == '4':
			query_4()
		elif choice == '5':
			query_5()
		elif choice == '6':
			query_6()



		else:
			raise Exception("We should never get here!")


	#print("\nGoodbye!\n")