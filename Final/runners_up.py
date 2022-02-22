


#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: 10906673
#    Student name: Alex Tam
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Runners-Up
#
#  In this assignment you will combine your knowledge of HTML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application that allows the user to access online data.  See the
#  instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these functions
# only.  You can import other functions provided they are standard
# ones that come with the default Python/IDLE implementation and NOT
# functions from modules that need to be downloaded and installed
# separately.  Note that not all of the imported functions below are
# needed to successfully complete this assignment.

# The function for accessing a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen, Request

# The function for displaying a web document in the host
# operating system's default web browser.  We have given
# the function a distinct name to distinguish it from the
# built-in "open" function for opening local files.
# (You WILL need to use this function in your solution.)
from webbrowser import open as urldisplay

#Added function
import webbrowser
from webbrowser import open as webopen


# Import some standard Tkinter functions. (You WILL need to use
# some of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will try to hide its
#      identity from the web server. This can sometimes be used
#      to prevent the server from blocking access to Python
#      programs. However we do NOT encourage using this option
#      as it is both unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message above about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to open a local HTML file in your operating
# system's default web browser.  (Note that Python's "webbrowser"
# module does not guarantee to open local files, even if you use a
# 'file://..." address).  The file to be opened must be in the same
# folder as this module.
#
# Since this code is platform-dependent we do NOT guarantee that it
# will work on all systems.
#
def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import isfile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not isfile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

##### DEVELOP YOUR SOLUTION HERE #####

#Create a window
the_window = Tk()

#Give the window a title
the_window.title("Serving Up Second Place")
#Colouring the background colour
the_window.configure(background="beige")
# The main title in the GUI Window
# Centered, positioned at very top of window
title_label = Label(the_window, text = "Serving Up\nSecond Place", borderwidth = 2, font = ('Arial', 35), fg = 'black', background="beige")
title_label.grid(row = 0, column = 0)

#Import an image to display in the windows
trophy_image = PhotoImage(file = "2nd Place.gif")
#Add the image to the window as a Label widget
Label(the_window, image = trophy_image, background="beige").grid(row = 1, column = 0)

#Create two changeable label widget
changeable_label_1 = Label(the_window, text = "Nothing Selected.", font = ('Arial', 20), height = 3, width= 30, borderwidth = 2, relief = 'groove', background="beige")
changeable_label_2 = Label(the_window, text = "Nothing Selected.", font = ('Arial', 10), height = 20, width= 60, borderwidth = 2, relief = 'groove', background="beige")
changeable_label_1.grid(row = 0, column = 1)
changeable_label_2.grid(row = 1, column = 1)

#Introduce the variable whose value will be changed
option = IntVar()

#Fuction used to find top 10 Music Chart (LIVE CHART - Music Name and Artist)
def find_top_10_music():
    #Unblocking server security so we can use this url
    req_music_web = Request('http://www.popvortex.com/music/itunes-charts/top-100-songs-australia.php', headers={'User-Agent': 'Mozilla/5.0'})
    #Open the web document for reading
    music_web_page = urlopen(req_music_web)
    #Read the document's contents as a list of raw bytes
    music_web_page_bytes = music_web_page.read()
    #Convert the bytes to printable characters for display in the shell window
    music_web_page_chars = music_web_page_bytes.decode()
    #Close the connection to the web server
    music_web_page.close()
    #Finding pattern in the element code of the website (title)
    title_start_marker = '<cite class="title">'
    title_end_marker = '</cite>'
    title_end_position = 0
    title_start_position = music_web_page_chars.find(title_start_marker, title_end_position)
    title_end_position = music_web_page_chars.find(title_end_marker, title_start_position)
    #Finding pattern in the element code of the website (artist)
    artist_start_marker = '<em class="artist">'
    artist_end_marker = '</em>'
    artist_end_position = 0
    artist_start_position = music_web_page_chars.find(artist_start_marker, artist_end_position)
    artist_end_position = music_web_page_chars.find(artist_end_marker, artist_start_position)
    #Displaying the the Music Name and Artist (turns it into a list so it can be displayed into the tkinter label)
    list_music = []
    #Display ranked 2
    ranked_2_title = findall('<cite class="title">(.+)</cite>', music_web_page_chars)[1:2]
    ranked_2_artist = findall('<em class="artist">(.+)</em>', music_web_page_chars)[1:2]
    ranked_2_text = ranked_2_title + ranked_2_artist
    changeable_label_1['text'] = "2nd Place:\n" + " - ".join(ranked_2_text)
    #Picked these start and end position to these numbers in order for the list to stop at ranking 10. 
    while title_start_position <= 51000 and title_end_position <= 55000 and artist_start_position <= 51000 and artist_end_position <= 55000: 
        title = music_web_page_chars[title_start_position + len(title_start_marker) : title_end_position]
        title_start_position = music_web_page_chars.find(title_start_marker, title_end_position)
        title_end_position = music_web_page_chars.find(title_end_marker, title_start_position)
        artist = music_web_page_chars[artist_start_position + len(artist_start_marker) : artist_end_position]
        artist_start_position = music_web_page_chars.find(artist_start_marker, artist_end_position)
        artist_end_position = music_web_page_chars.find(artist_end_marker, artist_start_position)
        music_text = title + ' - ' + '('+artist+')' + '\n'
        list_music.append(music_text)
        #Function to change the label's text when a radiobuttion is selected
        changeable_label_2['text'] = "Top 10 Music Chart in Australia:\n" + "".join(list_music)


    
 #Fuction used to find top 10 Weekend Box Office Chart (LIVE CHART - Title and Rotten Tomatoes)
def find_top_10_WeekendBoxOffice():
    #Unblocking server security so we can use this url
    req_WeekendBoxOffice_web = Request('https://www.rottentomatoes.com/browse/box-office/', headers={'User-Agent': 'Mozilla/5.0'})
    #Open the web document for reading
    WeekendBoxOffice_web_page = urlopen(req_WeekendBoxOffice_web)
    #Read the document's contents as a list of raw bytes
    WeekendBoxOffice_web_page_bytes = WeekendBoxOffice_web_page.read()
    #Convert the bytes to printable characters for display in the shell window
    WeekendBoxOffice_web_page_chars = WeekendBoxOffice_web_page_bytes.decode()
    #Close the connection to the web server
    WeekendBoxOffice_web_page.close()
    #Finding pattern in the element code of the website (Title)
    title_start_marker = ' itemprop="url">'
    title_end_marker = '</a>'
    title_end_position = 0
    title_start_position = WeekendBoxOffice_web_page_chars.find(title_start_marker, title_end_position)
    title_end_position = WeekendBoxOffice_web_page_chars.find(title_end_marker, title_start_position)
    #Finding pattern in the element code of the website (Rotten Tomatoes)
    tomatoes_start_marker = '<span class="tMeterScore">'
    tomatoes_end_marker = '</span>'
    tomatoes_end_position = 0
    tomatoes_start_position = WeekendBoxOffice_web_page_chars.find(tomatoes_start_marker, tomatoes_end_position)
    tomatoes_end_position = WeekendBoxOffice_web_page_chars.find(tomatoes_end_marker, tomatoes_start_position)
    #Displaying the Title and Rotten Tomatoes (turns it into a list so it can be displayed into the tkinter label)
    list_boxoffice = []
    #Display ranked 2
    ranked_2_title = findall('<a class="" target="_top" data-pageheader="" href="/m/.+/" itemprop="url">(.+)</a></td> <td>7</td>', WeekendBoxOffice_web_page_chars)[0:1]
    ranked_2_artist = findall('<span title="Fresh" class="icon tiny fresh"></span> <span class="tMeterScore">(.+)</span> </span> </span></td> <td class="left"> <meta itemprop="position" value="1">', WeekendBoxOffice_web_page_chars)[0:1]
    print(ranked_2_artist)
    #print(ranked_2_artist)
    ranked_2_text = ranked_2_title + ranked_2_artist
    changeable_label_1['text'] = "2nd Place:\n" + " - ".join(ranked_2_text)
    #Picked these start and end position to these numbers in order for the list to stop at ranking 10.
    while title_start_position <= 43100 and title_end_position <= 43450 and tomatoes_start_position <= 42950 and tomatoes_end_position <= 43350:   
        title = WeekendBoxOffice_web_page_chars[title_start_position + len(title_start_marker) : title_end_position]
        title_start_position = WeekendBoxOffice_web_page_chars.find(title_start_marker, title_end_position)
        title_end_position = WeekendBoxOffice_web_page_chars.find(title_end_marker, title_start_position)
        tomatoes = WeekendBoxOffice_web_page_chars[tomatoes_start_position + len(tomatoes_start_marker) : tomatoes_end_position]
        tomatoes_start_position = WeekendBoxOffice_web_page_chars.find(tomatoes_start_marker, tomatoes_end_position)
        tomatoes_end_position = WeekendBoxOffice_web_page_chars.find(tomatoes_end_marker, tomatoes_start_position)
        boxoffice_text = title + ' - ' + '('+tomatoes+')' + '\n'
        list_boxoffice.append(boxoffice_text)
        #Function to change the label's text when a radiobuttion is selected
        changeable_label_2['text'] = "Top 10 Weekend Box Office Chart:\n" + "".join(list_boxoffice)

        
 #Fuction used to find top 10 most Covid-19 cases found in USA California (LIVE CHART - Country and Total Cases)
def find_top_10_Covid():
    #Unblocking server security so we can use this url
    req_Covid_web = Request('https://www.worldometers.info/coronavirus/usa/california/', headers={'User-Agent': 'Mozilla/5.0'})
    #Open the web document for reading
    Covid_web_page = urlopen(req_Covid_web)
    #Read the document's contents as a list of raw bytes
    Covid_web_page_bytes = Covid_web_page.read()
    #Convert the bytes to printable characters for display in the shell window
    Covid_web_page_chars = Covid_web_page_bytes.decode()
    #Close the connection to the web server
    Covid_web_page.close()
    #Finding pattern in the element code of the website (Team Name)
    country_start_marker = '<td style="font-weight: bold; font-size:15px; text-align:left;">'
    country_end_marker = '</td>'
    country_end_position = 0
    country_start_position = Covid_web_page_chars.find(country_start_marker, country_end_position)
    country_end_position = Covid_web_page_chars.find(country_end_marker, country_start_position)
     #Finding pattern in the element code of the website (Points)
    cases_start_marker = '<td style="font-weight: bold; text-align:right">'
    cases_end_marker = ' </td>'
    cases_end_position = 0
    cases_start_position = Covid_web_page_chars.find(cases_start_marker, cases_end_position)
    cases_end_position = Covid_web_page_chars.find(cases_end_marker, cases_start_position)
    #Displaying the Country and Total Cases (turns it into a list so it can be displayed into the tkinter label)
    list_covid = []
    #Display ranked 2
    ranked_2_title = findall('''<td style="font-weight: bold; font-size:15px; text-align:left;">
(.+) </td>''', Covid_web_page_chars)[1:2]
    ranked_2_artist = findall('<td style="font-weight: bold; text-align:right">(.+)</td>', Covid_web_page_chars)[1:2]
    ranked_2_text = ranked_2_title + ranked_2_artist
    changeable_label_1['text'] = "2nd Place:\n" + " - ".join(ranked_2_text)
    #Picked these start and end position to these numbers in order for the list to stop at ranking 10.    
    while country_start_position <= 24800 and country_end_position <= 25400 and cases_start_position <= 24900 and cases_end_position <= 25700: 
        country = Covid_web_page_chars[country_start_position + len(country_start_marker) : country_end_position]
        country_start_position = Covid_web_page_chars.find(country_start_marker, country_end_position)
        country_end_position = Covid_web_page_chars.find(country_end_marker, country_start_position)
        cases = Covid_web_page_chars[cases_start_position + len(cases_start_marker) : cases_end_position]
        cases_start_position = Covid_web_page_chars.find(cases_start_marker, cases_end_position)
        cases_end_position = Covid_web_page_chars.find(cases_end_marker, cases_start_position)
        covid_ranking_text = country + ' - ' + '('+cases+')' 
        list_covid.append(covid_ranking_text)
        #Function to change the label's text when a radiobuttion is selected
        changeable_label_2['text'] = "Top 10 Covid-19 Cases in California:" + "".join(list_covid)
    
#Fuction used to find top 10 Music Chart (DOWNLOADED CHART 12/10/2020 - Music Name and Artist)
def find_top_10_downloadedmusic():
    #Open the web document for reading
    downloaded_web_page = open('iTunes Australia Top 100 Songs 2020.html')
    #Read the document's contents as a list of raw bytes
    downloaded_web_page_bytes = downloaded_web_page.read()
    #Close the connection to the document
    downloaded_web_page.close()
    #Finding pattern in the element code of the website (Music Name)
    title_start_marker = '<cite class="title">'
    title_end_marker = '</cite>'
    title_end_position = 0
    title_start_position = downloaded_web_page_bytes.find(title_start_marker, title_end_position)
    title_end_position = downloaded_web_page_bytes.find(title_end_marker, title_start_position)
    #Finding pattern in the element code of the website (Artist)
    artist_start_marker = '<em class="artist">'
    artist_end_marker = '</em>'
    artist_end_position = 0
    artist_start_position = downloaded_web_page_bytes.find(artist_start_marker, artist_end_position)
    artist_end_position = downloaded_web_page_bytes.find(artist_end_marker, artist_start_position)
    #Helps display the Music Name and Artist (turns it into a list so it can be displayed into the tkinter label)
    list_downloaded_music = []
    #Display ranked 2
    ranked_2_title = findall('<cite class="title">(.+)</cite>', downloaded_web_page_bytes)[1:2]
    ranked_2_artist = findall('<em class="artist">(.+)</em>', downloaded_web_page_bytes)[1:2]
    ranked_2_text = ranked_2_title + ranked_2_artist
    #Function to change the label's text when a radiobuttion and then update button is selected
    changeable_label_1['text'] = "2nd Place:\n" + " - ".join(ranked_2_text)
    #Picked these start and end position to these numbers in order for the list to stop at ranking 10.
    while title_start_position <= 51000 and title_end_position <= 55000 and artist_start_position <= 51000 and artist_end_position <= 55000: 
        title = downloaded_web_page_bytes[title_start_position + len(title_start_marker) : title_end_position]
        title_start_position = downloaded_web_page_bytes.find(title_start_marker, title_end_position)
        title_end_position = downloaded_web_page_bytes.find(title_end_marker, title_start_position) 
        artist = downloaded_web_page_bytes[artist_start_position + len(artist_start_marker) : artist_end_position]
        artist_start_position = downloaded_web_page_bytes.find(artist_start_marker, artist_end_position)
        artist_end_position = downloaded_web_page_bytes.find(artist_end_marker, artist_start_position)
        downloaded_music_text = title + ' - ' + '('+artist+')' + '\n'
        list_downloaded_music.append(downloaded_music_text)
        #Function to change the label's text when a radiobuttion and then update button is selected
        changeable_label_2['text'] = "Top 10 Music Chart in Australia:\n" + "".join(list_downloaded_music)
        
#Update Button (Updates the sources into the label text)
def update_source():
    if option.get() == 1:
        find_top_10_music()
    elif option.get() == 2:
        find_top_10_WeekendBoxOffice()
    elif option.get() == 3:
        find_top_10_Covid()
    elif option.get() == 4:
        find_top_10_downloadedmusic()
    else:
        pass
update_source_button = Button(the_window, text = "Update", font = ('Arial', 15), command = update_source, background = "white")
update_source_button.grid(row = 5, column = 0)

#Create four distant lists
#3 Updated frequently 
Music_Chart = Radiobutton(the_window, text = "LIVE\niTunes (Aus) Music Chart\n[title and artist]", font = ('Arial', 15),fg = 'red', variable = option, value = 1, command = update_source_button, background="beige")
Movie_Chart = Radiobutton(the_window, text = "LIVE\nUS Weekend Box Office Chart\n[title and rotten tomatoes]", font = ('Arial', 15), fg = 'red',variable = option, value = 2, command = update_source_button, background="beige")
ASX_Chart = Radiobutton(the_window, text = "LIVE\nCovid-19 Cases in California Chart\n[country and total cases]", font = ('Arial', 15),fg = 'red', variable = option, value = 3, command = update_source_button, background="beige")
#1 Never Changes 
NotUpdated_Music_Chart = Radiobutton(the_window, text = "PREVIOUS\niTunes (Aus) Music Chart\n[12/10/2020]", font = ('Arial', 15), fg = 'dark blue',variable = option, value = 4,  command = update_source_button, background="beige")
#Griding the distant lists on the window
Music_Chart.grid(row = 3, column = 0)
Movie_Chart.grid(row = 3, column = 1)
ASX_Chart.grid(row = 4, column = 0)
NotUpdated_Music_Chart.grid(row = 4, column = 1)

#Soruce Button (Shows the website where the sources are found)
def show_source():
    if option.get() == 1:
        webbrowser.open("http://www.popvortex.com/music/itunes-charts/top-100-songs-australia.php")
    elif option.get() == 2:
        webbrowser.open("https://www.rottentomatoes.com/browse/box-office/")
    elif option.get() == 3:
        webbrowser.open("https://www.worldometers.info/coronavirus/usa/california/")
    elif option.get() == 4:
        webopen('iTunes Australia Top 100 Songs 2020.html')
    else:
        pass
show_source_button = Button(the_window, text = "Show Source", font = ('Arial', 15), command = show_source, background = "white")
show_source_button.grid(row = 5, column = 1)

    #Save Button (Store displayed data)
def save_data():
    if option.get() == 1:
        pass
    elif option.get() == 2:
        pass
    elif option.get() == 3:
        pass
    elif option.get() == 4:
        pass
    else:
        pass
save_data_button = Button(the_window, text = "Save", font = ('Arial', 15), command = save_data, background = "white")
save_data_button.grid(row = 6, column = 0)

# Start the event loop to react to user inputs
the_window.mainloop()
#Part B of Assignment
#Import the SQL functions
from sqlite3 import *
#Create a connection to the database
connection = connect(database = 'runners_up.db')
#Get a pointer into the database
runners_up_db = connection.cursor()

#Save Button (Store displayed data)
def save_data():
    if option.get() == 1:
        sql = """INSERT INTO runner_up(competitor, property)
                VALUES(title, artist)"""
        runners_up_db.execute(sql)
        connection.commit()
    elif option.get() == 2:
        sql = """INSERT INTO runner_up(competitor, property)
                VALUES(title, tomatoes)"""
        runners_up_db.execute(sql)
        connection.commit()
    elif option.get() == 3:
        sql = """INSERT INTO runner_up(competitor, property)
                VALUES(country, cases)"""
        runners_up_db.execute(sql)
        connection.commit()
    elif option.get() == 4:
        sql = """INSERT INTO runner_up(competitor, property)
                VALUES(title, artist)"""
        runners_up_db.execute(sql)
        connection.commit()
    else:
        pass
save_data_button = Button(the_window, text = "Save", font = ('Arial', 15), command = save_data, background = "white")
save_data_button.grid(row = 6, column = 0)

#Close the database
runners_up.db.close()
connection.close()
