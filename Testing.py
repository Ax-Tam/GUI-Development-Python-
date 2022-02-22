#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N9935924
#    Student name: Greyden Scott
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Online Shopper
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for aggregating product data published by a variety of
#  online shops.  See the instruction sheet accompanying this file
#  for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression.  (You do NOT need to
# use these functions in your solution, although you will find
# it difficult to produce a robust solution without using
# regular expressions.)
from re import findall, finditer

# Import the standard SQLite functions just in case they're
# needed.
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# URLS Stored in varible
ladies_dresses_url = 'http://www.joomlajingle.com/rss/catalog/new/store_id/1/'
shoes_url = 'https://www.shoes.com/rss-sale-shoes'
car_dvr_url = 'https://www.seicane.com/rss/catalog/category/cid/158/store_id/1/'
hats_url = 'https://feed.zazzle.com/rss?qs=hats'


# Function used to scrape images
# Check which store is loaded into the web page contents
# and performs the find all using the correct regex string for the corrosponding
# web page.
# Returns a list of image urls
def find_images(web_page_contents, store = 'none'):
	if store == 'ladies_dresses' or store == 'car_dvr' or store == 'hats':
		page_images = findall('src="([A-z _0-9-/:/.*]+)', web_page_contents)
	elif store == 'shoes':
		page_images = findall("src='([A-z _0-9-/:/.*]+)", web_page_contents)
	if store != 'none':
		return page_images

# Function used to scrape descriptions
# Check which store is loaded into the web page contents
# and performs the find all using the correct regex string for the corrosponding
# web page.
# Returns a list of descriptions
def find_titles(web_page_contents, store = "none"):
	if store == 'ladies_dresses':
		page_titles = findall('\<item\>\s*\<title\>\<\!\[CDATA\[(.*?)]]', web_page_contents)
	elif store == 'shoes':
		page_titles = findall('<title>([A-z 0-9^-]+)</title>', web_page_contents)
	elif store == 'car_dvr':
		page_titles = findall('\<item\>\n      \<title\>\<\!\[CDATA\[(.*?)]]', web_page_contents)
	elif store == 'hats':
		page_titles = findall('\<title\>\<\!\[CDATA\[(.*?)]]', web_page_contents)
	if store != 'none':
		return page_titles

# Function used to scrape prices
# Check which store is loaded into the web page contents
# and performs the find all using the correct regex string for the corrosponding
# web page.
# Returns a list of prices
def find_prices(web_page_contents, store = "none"):
	if store == 'ladies_dresses':
		page_prices = findall('id="old-price-[0-9^]+">\$([$0-9^.]+)', web_page_contents)
	elif store == 'shoes':
		page_prices = findall('Sale Price: \$([$0-9^.]+)', web_page_contents)
	elif store == 'car_dvr':
		page_prices = findall('price">US\$([$0-9^.]+)', web_page_contents)
	elif store == 'hats':
		page_prices = findall('price">\$([$0-9^.]+)', web_page_contents)
	if store != 'none':
		return page_prices

# Function used to update the progress label in the GUI
# with the passed text.
# Performs an update on the GUI window to show changs
def update_progress(text_to_display):
	progress_label.config(text = text_to_display)
	the_window.update()

# Function used to convert current the passed price 
# from Australian Dollars to American Dollars.
# Exchange rate set to a static 1.33
# Retuns a float of the rounded price 
def currency_conversion(price):
	us_dollar = 1.33
	converted_price = float(price) * float(us_dollar)
	return float(round(converted_price, 2))

# Function used to calculate the total price
# Takes a list of intergers that indicate the number of items
# From each URL to add up and a list of the actual items
# Returns a rounded total that has been passed through the 
# currency_conversion function
def calculate_total(items_to_display, items_to_write):
	# 1. sets total to 0.0
	total = 0.0
	# 2. For each category in range of the total number of items requested
	for category in range(len(items_to_display)):
		# 3. for each item in each category
		for item in range(int(items_to_display[category])):
			# 4. Obtain the price form the list of items to write
			price = items_to_write[category][2][item]
			# 5. Calculate the total and convert price to Australian Dollars
			total = total + currency_conversion(float(price))
	# Return the total, rounded up to the 2nd decimal place
	return round(total,2)

# Function used to save items written to invoice, into a Database
# Information is passed to the function using a global variable.
def save_items_in_db():
	# Global variables used to store number of items selected
	# and the item data which has been scraped from their respective stores
	global items_written 
	global items_displayed

	# Perform a check to make sure that items have been selected.
	# If they have not, update the GUI, Disable the Save Button
	# And return the function with None
	items_to_display = [int(laddies_dresses_spinbox.get()), int(shoes_spinbox.get()), int(car_dvr_spinbox.get()), int(hats_spinbox.get())]
	if items_to_display[0] == 0 and items_to_display[1] == 0 and items_to_display[2] == 0 and items_to_display[3] == 0:
		update_progress("No items selected")
		save_button.config(state = DISABLED)
		return None

	# Store the data from the global variables in to local variables
	items_to_write = items_written
	items_to_display = items_displayed

	# Connect to database
	connection = connect('shopping_trolley.db')
	shopping_trolley_db = connection.cursor()

	# Clear data base by performing a delete from execution.
	shopping_trolley_db.execute("""DELETE FROM Purchases""")

	# Store a string for inserting items into Data Base
	query = """INSERT INTO Purchases(Description, Price) VALUES ('{}', {})"""
	
	# Using a for loop, run through number of items to display for each category as 
	# and write to Data Base
	for category in range(len(items_to_display)):
		# double check that the number of items to display is definately greater than 0
		if items_to_display[category] > 0:
			# cycle through the number of items
			for count in range(items_to_display[category]):
				# write to the SQL file for each item, pulling the description, image url and price 
				# into the query string
				shopping_trolley_db.execute(query.format(items_to_write[category][0][count], currency_conversion(float(items_to_write[category][2][count]))))
				
				#Commit changes on each line entered.
				connection.commit()
	#Close connection to Data Base
	shopping_trolley_db.close()
	#Disable the Save Items Button
	save_button.config(state = DISABLED)
	#Update the GUI
	update_progress("Items Saved!")


# Generates the list of items to display by gathering the scraped data
# Stores the title, price and image url of each item in a list and compiles that list
def generate_items_to_write(items_to_display):
	update_progress("Gathering Items Requested")
	# 1. Setup required lists for the different store categories and urls
	item_types = ['ladies_dresses', 'shoes', 'car_dvr', 'hats']
	all_urls = [ladies_dresses_url, shoes_url, car_dvr_url, hats_url]
	# also required a counter for cycling through the urls 
	url_counter = 0
	# also required is empty list for each category to write into
	dresses_to_write, shoes_to_write, car_dvr_to_write, hats_to_write = [], [], [], []
	# 2. For each item in the list of items to display
	for item in items_to_display:
		# 3. Grab the URL in order 
		url_to_scrape = all_urls[url_counter]
		# 4. Set the correct store
		store = item_types[url_counter]
		# 5. Increase teh url counter by 1 so on the next iteration it uses the next
		# store
		url_counter = url_counter + 1
		# 6. if the number of items requested is no equl to 0
		# aka, the user actually requested an item
		if item != 0:
			# 7. Open the web web page, read and store the contents into a variable
			web_page_contents = urlopen(url_to_scrape).read()
			# 8. Scrape descriptions, image urls & prices and store them into individual 
			# variables using the web page contents and store provided
			images_grabbed = find_images(web_page_contents, store)
			titles_grabbed = find_titles(web_page_contents, store)
			prices_grabbed = find_prices(web_page_contents, store)

			# 9. Create a list of each item, and the corrosponding data associated with it
			if store == item_types[0]:
				dresses_to_write = [titles_grabbed, images_grabbed, prices_grabbed]
			elif store == item_types[1]:
				shoes_to_write = [titles_grabbed, images_grabbed, prices_grabbed]
			elif store == item_types[2]:
				car_dvr_to_write = [titles_grabbed, images_grabbed, prices_grabbed]
			elif store == item_types[3]:
				hats_to_write = [titles_grabbed, images_grabbed, prices_grabbed]
	# 10. Return a list of all the items for all teh categories to write
	return [dresses_to_write, shoes_to_write, car_dvr_to_write, hats_to_write]

# Function to create the physical invoice
# Takes a file name, list of items to display, items to write and the total price
def create_invoice(file_name, items_to_display, items_to_write, total):
	update_progress("Writing Invoice")

	# 1. create the invoice.html file by opening a file with the passed file name
	# and setting it to writeable 
	text_file = open(file_name, 'w')
	# 2. Write the HTML header of the file. Pass the total into the string
	text_file.write("""
<!DOCTYPE html>
<html>
<head>
	<title> Shop Smart, Shop S-Mart </title>
	<style>
		@import url('https://fonts.googleapis.com/css?family=Nunito+Sans|Patua+One');
		body {{
			background-image: url('http://www.horroremporium.com/wp-content/uploads/2014/10/The-Evil-Dead-Silhouette.jpg');
			background-repeat: no-repeat;
			background-attachment: fixed;
			background-position: right bottom;
			background-opacity: 0.5;
		}}
		h1 {{
			font-family: 'Patua One', cursive;
		    text-align: center;
		    font-size: 2em;
		}}
		#responsive_img {{
			width: 200px;
			height: auto;
		}}
		table {{
			background-color: white;
			border: 1px solid black;
			border-collapse: collapse;
			width: 30%;
			text-align: center;
			font-family: verdana;
		    font-size: 1em;
		    box-shadow: 10px 10px 5px #888888;
		}}
		#credits {{
			border: none;
			box-shadow: none;
		}}
		ul,li {{
			list-style-type: none;
			font-size: 1em;
			text-align: left;
		}}
	</style>
</head>
<body>
	<center><img src="http://www.lasersharkdesign.com/shop/image/cache/data/zorv/s-mart-800x1000.jpg" height="400" width="500"></center>
	<h1>Total for the purchases below:<br>{}</h1><br>""".format(str(total)))
	# 3. Create a variable of a template for building a table of each item
	invoice_items_to_print = '''
	<table align="center">
		<tr>
			<td><b> {} </b></td>
		</tr>
		<tr>
			<td><img src="{}" id="responsive_img"></td>
		</tr>
		<tr>
			<td>Our Price: {} AUD</td>
		</tr>
	</table>
	<br>'''
	# 4. For each category
	for category in range(len(items_to_display)):
		# double check that the number of items to display is definately greater than 0
		if items_to_display[category] > 0:
			# cycle through the number of items
			for count in range(items_to_display[category]):
				# write the table for each item, pulling the description, image url and price 
				# into the string
				text_file.write(invoice_items_to_print.format(items_to_write[category][0][count], items_to_write[category][1][count], str(currency_conversion(float(items_to_write[category][2][count])))))
	# 5. Write the bottom of the HTML file
	# adding the store urls to the bottom
	text_file.write("""
	<table align="center" id="credits">
		<tr>
			<td>
				<br>
				<b>S-Mart is proudly supported by: </b>
				<br>
				<br>
				<a href="{}">{}</a><br>
				<a href="{}">{}</a><br>
				<a href="{}">{}</a><br>
				<a href="{}">{}</a><br>
			</td>
		</tr>
	</table>
</body>
</html>""".format(ladies_dresses_url, ladies_dresses_url, shoes_url, shoes_url, car_dvr_url, car_dvr_url, hats_url, hats_url))
	text_file.close()

# Function to run when the print invoice button is pressed on the GUI
def print_invoice():
	# Global variables used to store number of items selected
	# and the item data which has been scraped from their respective stores
	global items_written
	global items_displayed

	# Contains the file name for the invoice to be created
	file_name = 'invoice.html'
	# creates the items_to_display list and populates it with the number of items selected 
	# in each spinbox on the gui for each category of store
	items_to_display = [int(laddies_dresses_spinbox.get()), int(shoes_spinbox.get()), int(car_dvr_spinbox.get()), int(hats_spinbox.get())]
	# if no items have been selected, updates the GUI
	# set the total to "No Charge"
	# generate an empty list of empty items to write
	if items_to_display[0] == 0 and items_to_display[1] == 0 and items_to_display[2] == 0 and items_to_display[3] == 0:
		update_progress("Nothing Selected \n")
		items_to_write = generate_items_to_write(items_to_display)
		calculated_total = "No Charge"
	# if items have been selected
	# create a list of items to write
	# calculate the total based on that list and the number of items selected
	# create the invoice
	else:
		items_to_write = generate_items_to_write(items_to_display)
		calculated_total = "$" + str(calculate_total(items_to_display, items_to_write)) + " AUD"
	create_invoice(file_name, items_to_display, items_to_write, calculated_total)

	# store the items to write and the items to display into a global varible to be
	# optionally used if data is to be written in data base
	items_written = items_to_write
	items_displayed = items_to_display
	#Enable Save Items Button
	save_button.config(state = NORMAL)

	#Update GUI
	update_progress("Done!")

# GUI
# Create the GUI Window utilsing tkinter
the_window = Tk()
# Set the title of the GUI Window
the_window.title('S-Mart')


# The main title in the GUI Window
# Centered, positioned at very top of window
title_label = Label(the_window, text = "Welcome to S-Mart \n Online Shop!", borderwidth = 2, font = ('Arial', 35), pady = 15, padx = 20, fg = 'blue')
title_label.grid(row = 0, column = 0, columnspan = 6)

# The sub-itle in the GUI Window
# Centered, positioned just below the main title
sub_title_label = Label(the_window, text = "Shop Smart, Shop S-Mart", borderwidth = 2, font = ('Arial', 14), padx = 20)
sub_title_label.grid(row = 1, column = 0, columnspan = 6)

# Instruction Text, Step 1
# Aligned Left, positioned below sub-title
header_one_label = Label(the_window, text = "Step 1. Choose your quantities", borderwidth = 2, font = ('Arial', 20), pady = 25, padx = 20, justify = CENTER, fg = 'dark green')
header_one_label.grid(row = 2, column = 0, columnspan = 6, sticky = W)

# Create the spin boxes and labels for each category
# Maximum of 5 items per spin box
laddies_dresses_label = Label(the_window, text = "Ladies\nDresses", borderwidth = 2, font = ('Arial', 10), pady = 25, padx = 20, justify = CENTER)
laddies_dresses_label.grid(row = 3, column = 1, columnspan=6, sticky = W)
laddies_dresses_spinbox = Spinbox(the_window,from_ = 0, to = 5, width = 2, state = 'readonly')
laddies_dresses_spinbox.grid(row = 3, column = 2, columnspan = 6, sticky = W)

shoes_label = Label(the_window, text = "Quality\nShoes", borderwidth = 2, font = ('Arial', 10), pady = 25, padx = 20, justify = CENTER, wraplength = 0)
shoes_label.grid(row = 3, column = 3, columnspan=6, sticky = W)
shoes_spinbox = Spinbox(the_window,from_ = 0, to = 5, width = 2, state = 'readonly')
shoes_spinbox.grid(row = 3, column = 4, columnspan = 6, sticky = W)

car_dvr_label = Label(the_window, text = "Car DVR", borderwidth = 2, font = ('Arial', 10), pady = 25, padx = 20, justify = CENTER)
car_dvr_label.grid(row = 4, column = 1, columnspan=6, sticky = W)
car_dvr_spinbox = Spinbox(the_window,from_ = 0, to = 5, width = 2, state = 'readonly')
car_dvr_spinbox.grid(row = 4, column = 2, columnspan = 6, sticky = W)

hats_label = Label(the_window, text = "Glorious\nHats", borderwidth = 2, font = ('Arial', 10), pady = 25, padx = 20, justify = CENTER)
hats_label.grid(row = 4, column = 3, columnspan=6, sticky = W)
hats_spinbox = Spinbox(the_window,from_ = 0, to = 5, width = 2, state = 'readonly')
hats_spinbox.grid(row = 4, column = 4, columnspan = 6, sticky = W)

# Instruction Text, Step 2
# Aligned Left, positioned below spinboxes and category text
header_two_label = Label(the_window, text = "Step 2. When ready, print your invoice", borderwidth = 2, font = ('Arial', 20), pady = 25, padx = 20, fg = 'dark green')
header_two_label.grid(row = 5, column = 0, columnspan = 6, sticky = W)

# Invoice Button, when pressed runs the print invoice function
# Aligned Center, positioned below instruction text
invoice_button = Button(the_window, text = 'Print Invoice', command = print_invoice)
invoice_button.grid(row = 6, column = 0, columnspan = 6)

# Instruction Text, Step 3
# Aligned Left, positioned below print invoice button
header_three_label = Label(the_window, text = "Step 3. Watch your order's progress", borderwidth = 2, font = ('Arial', 20), pady = 25, padx = 20, fg = 'dark green')
header_three_label.grid(row = 7, column = 0, columnspan = 6, sticky = W)

# Progress label, inititally set to "Ready"
# updated each time update_progress function is called
progress_label = Label(the_window, text = "Ready", borderwidth = 2, font = ('Arial', 20), pady = 25, padx = 20, fg='red')
progress_label.grid(row = 8, column = 0, columnspan = 6)

# Instruction Text, Step 2
# Aligned Left, positioned below spinboxes and category text
header_two_label = Label(the_window, text = "Step 4. Save to Shopping Trolley", borderwidth = 2, font = ('Arial', 20), padx = 20, fg = 'dark green')
header_two_label.grid(row = 9, column = 0, columnspan = 6, sticky = W)

# Invoice Button, when pressed runs the print invoice function
# Aligned Center, positioned below instruction text
save_button = Button(the_window, text = 'Save Items', command = save_items_in_db, pady = 25, padx = 20, state=DISABLED)
save_button.grid(row = 10, column = 0, columnspan = 6)

# Inititate the GUI
the_window.mainloop()
