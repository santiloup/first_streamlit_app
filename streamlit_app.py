import pandas
import streamlit

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
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_response.json()) # raw json response

# preetify fruityvice output & display
fruityvice_normalized = pandas.json_normalize(fruityvice_response)
streamlit.text(fruityvice_normalized)
