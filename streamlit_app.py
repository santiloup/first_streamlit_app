import pandas
import streamlit
import requests
import snowflake.connector
from urllib.error import URLError

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

# function to get fruityvoice data for a fruit_request
def get_fruityvoice_data(fruit_request):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_request)
    # preetify fruityvice output & display
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# incorporate frutyvice request in streamlit
streamlit.header("Fruityvice Fruit Advice!")
try: 
  # get the fruit choice from user
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error('Please select a fruit to get information. ')
  else:
    streamlit.write('The user entered ', fruit_choice)
    streamlit.dataframe(get_fruityvoice_data(fruit_choice))

except URLError as e:
  streamlit.error()

# Adding snowflake connection, bring in fruit load list

# get fruit list as UDF
def get_fruit_load_list():
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute("SELECT * FROM fruit_load_list")
    my_data_rows = my_cur.fetchall()
    return my_data_rows

# Add an action button to load the fruit list
if streamlit.button('Get Fruit Load List'):
    streamlit.header("The fruit load list contains:")
    streamlit.dataframe(get_fruit_load_list())

# UDF to add fruit
def add_fruit_to_list(new_fruit):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    fruit_add_query = "insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit + "')"
    streamlit.write(fruit_add_query)
    my_cur.execute(fruit_add_query)
    return

# Adding a new fruit from fruityvice menu into snowflake list
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
new_fruit = streamlit.selectbox("What fruit would you like to add to the fruit load list?", list(my_fruit_list.Fruit))
# Button to add list only with user action
if streamlit.button('Add this fruit: ' + new_fruit + '!'):
    streamlit.write('New fruit selected: ', new_fruit)
    add_fruit_to_list(new_fruit)

# improving control flow, temporarily stopping here
streamlit.stop()
