import pandas
import streamlit
import requests
import snowflake.connector

# Main menu
streamlit.title("My Mom's new healthy Diner")
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# fruit list
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
# Let's put a pick list here so they can pick the fruit they want to include 
fruit_selection = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.Fruit), ['Avocado', 'Strawberries'])
# ingredients list
my_fruit_list = my_fruit_list.set_index('Fruit')
streamlit.dataframe(my_fruit_list.loc[fruit_selection])

# incorporate frutyvice request in streamlit
streamlit.header("Fruityvice Fruit Advice!")
# get the fruit choice from user
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# preetify fruityvice output & display
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

# Adding snowflake connection, test bringing in account metadata
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Adding a new fruit from fruityvice menu into snowflake list
new_fruit = streamlit.select("What fruit would you like to add to the fruit load list?", list(my_fruit_list.Fruit))
streamlit.write('New fruit selected: ', new_fruit)
fruit_add_query = "insert into pc_rivery_db.public.fruit_load_list values (" & new_fruit & ")"
streamlit.write(fruit_add_query)
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values (" & new_fruit & ")")
