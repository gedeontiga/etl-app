import csv
# from hmac import new
import os
import tkinter as tk
from tkinter import ttk
# from tokenize import String
# from turtle import title
import mysql.connector as mc
from numpy import add

#Create a connection
conn = mc.connect(
    host="localhost",
    user="root",
    password="",
    database="tpinf351"
)

#Define the schema
# schema  = {
#     'Title': str,
#     'Author': str, 
#     'Establishment': str,
#     'Town': str,
#     'Country': str,
#     'Year': int
# }

def create_database(directory):
    cursor = conn.cursor()
    with open(directory, 'r') as file:
        queries = file.read()
        list_query = queries.split(';')
        for query in list_query:
            if query.strip():
                cursor.execute(query)
    conn.commit()
    conn.close

    return True;

def delete_data():

    if(create_database_() == False):
        create_database_()

    cursor = conn.cursor()

    alter_query1 = "ALTER TABLE article AUTO_INCREMENT=0"
    alter_query2 = "ALTER TABLE auteur AUTO_INCREMENT=0"
    alter_query3 = "ALTER TABLE affiliation AUTO_INCREMENT=0"

    delete_query1 = "DELETE FROM article"
    delete_query2 = "DELETE FROM auteur"
    delete_query3 = "DELETE FROM affiliation"
    delete_query4 = "DELETE FROM auteuraffiliation"
    delete_query5 = "DELETE FROM auteurarticle"
    delete_query6 = "DELETE FROM affiliationarticle"

    cursor.execute(delete_query1)
    cursor.execute(delete_query2)
    cursor.execute(delete_query3)
    cursor.execute(delete_query4)
    cursor.execute(delete_query5)
    cursor.execute(delete_query6)

    cursor.execute(alter_query1)
    cursor.execute(alter_query2)
    cursor.execute(alter_query3)
    return True

def extract_data(directory, year):

    cursor = conn.cursor()

    add_query1 = "INSERT INTO article(titre_article, idDate) SELECT %s, idDate FROM date d WHERE d.annee=%s"
    add_query2 = "INSERT INTO auteur(nom_encode) VALUES (%s)"
    add_query3 = "INSERT INTO affiliation(etablissement, ville, pays, idContinant) SELECT %s, %s, %s, idContinant FROM continant c WHERE c.nom=%s"
    add_query4 = "INSERT INTO auteurAffiliation SELECT a1.idAuteur, a2.idAffiliation FROM auteur a1, affiliation a2 WHERE a1.nom_encode=%s AND a2.etablissement=%s"
    add_query5 = "INSERT INTO auteurArticle SELECT a1.idAuteur, a2.idArticle FROM auteur a1 JOIN article a2 ON a2.titre_article=%s WHERE a1.nom_encode =%s"
    add_query6 = "INSERT INTO affiliationArticle SELECT a1.idArticle, a2.idAffiliation FROM article a1 JOIN affiliation a2 ON a1.titre_article=%s WHERE a2.etablissement =%s"

    #Iterate for each directory
    i = 0
    article_title = []
    for filename in os.listdir(directory):

        if filename.endswith('csv'):
            filepath = os.path.join(directory, filename)
            print(filepath)
            #Open the CSV file
            with open(filepath, 'r', encoding='utf-8') as file:
                #Create a CSV reader object
                file_content = file.read()

            standard_content = file_content.replace('|', '\n')
            reader = csv.reader(standard_content.splitlines())

            #Iterate over each row in the CSV file
            for index, row in enumerate(reader):
                if index == 0:
                    # col0 = schema['Title'](row[0])
                    article_title.insert(i, row[index])
                    i = i+1
                    cursor.execute(add_query1, (row[index], year))
                    # print(f"Title : {col0}")
                elif index == 1:
                    name_author = row[0]
                    split_name_author = row[0].split(' ')
                    decrease_name = name_author[0]+". "+split_name_author[-1]
                    row[0] = decrease_name.upper()
                    auth_name = row[0]
                    establishment = row[1]

                    if row[3] == ' United States':
                        row[3] = ' USA'
                    elif row[3] == ' The Netherlands':
                        row[3] = ' Netherlands'

                    # col4 = schema['Country'](row[3])
                    cursor.execute(add_query2, (row[0],))

                    if row[3] == " USA" or row[3] == " CA" or row[3] == " Canada" or row[3] == " Brazil":
                        cursor.execute(add_query3, (row[1], row[2], row[3], "America"))
                    elif row[3] == " Australia":
                        cursor.execute(add_query3, (row[1], row[2], row[3], "Oceania"))
                    elif  row[3] == " Japan" or row[3] == " China" or row[3] == " India" or row[3] == " Singapore" or row[3] == " Hong Kong" or  row[3] == " Vietnam" or row[3] == " South Korea"  or row[3] == " Israel":
                        cursor.execute(add_query3, (row[1], row[2], row[3], "Asia"))
                    else:
                        cursor.execute(add_query3, (row[1], row[2], row[3], "Europe"))

                    cursor.execute(add_query4, (auth_name, establishment))
                    cursor.execute(add_query5, (article_title[i-1], auth_name))
                    cursor.execute(add_query6, (article_title[i-1], establishment))
                    data_table.insert('', tk.END, values=[row[0], row[1], row[2], row[3], year])
            
            #Center align the contents of the cells
            for col in data_table['columns']:
                data_table.heading(col, anchor='center')
                data_table.column(col, anchor='center')

    resize_table()
    #Commit the changes
    conn.commit()

    cursor.close()
    # conn.close()

def resize_table(event=None):
    table_width = window.winfo_width() - 4 #----------->Adjust for border
    column_width = table_width//5 #-------------------->Divide equaly among columns
    data_table.column('Author', width=column_width)
    data_table.column('Establishment', width=column_width)
    data_table.column('Town', width=column_width)
    data_table.column('Country', width=column_width)
    data_table.column('Year', width=column_width)
    table_height = (window.winfo_height() - 100)//20 #->Adjust for other widgets and row height
    data_table.configure(height=table_height)

def create_database_():
    return create_database('tpinf351.sql')

def display_data():
    
    if(create_database_() == False):
        create_database_()
    
    if(delete_data() == False):
        delete_data()

    extract_data("Articles_TP_INF351_Data\\Articles_2014_textes", "2014")
    extract_data("Articles_TP_INF351_Data\\Articles_2015_textes", "2015")
    extract_data("Articles_TP_INF351_Data\\Articles_2016_textes", "2016")
    extract_data("Articles_TP_INF351_Data\\Articles_2017_textes", "2017")

#Create the main window
window = tk.Tk()
window.title('Extract Data Viewer')
#Default size of window
window.geometry('720x480')

button_frame = tk.Frame(window)
button_frame.pack(side=tk.TOP)
#Create a button to read data
create_button = tk.Button(button_frame, text="Create Database", command=create_database_)
create_button.pack(side=tk.LEFT, padx=30, pady=20)
delete_button = tk.Button(button_frame, text="Clear Database ", command=delete_data)
delete_button.pack(side=tk.LEFT, padx=30, pady=20)
read_button = tk.Button(button_frame, text="Extract Data", command=display_data)
read_button.pack(side=tk.LEFT, padx=30, pady=20)

#Create a table to display the data
data_table = ttk.Treeview(window, columns=('Author', 'Establishment', 'Town', 'Country', 'Year'), show='headings')
data_table.heading('Author', text='Author')
data_table.heading('Establishment', text='Establishment')
data_table.heading('Town', text='Town')
data_table.heading('Country', text='Country')
data_table.heading('Year', text='Year')
data_table.pack()

#Bind the resize_table funtion to the window's configure event
window.bind('<Configure>', resize_table)

#Start the GUI event loop
window.mainloop()