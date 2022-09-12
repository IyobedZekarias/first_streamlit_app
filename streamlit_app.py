import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])

def get_fruityvice(fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  return pandas.json_normalize(fruityvice_response.json())

def get_fruitLoadList():
  with my_cnx.cursor as my_cur:
    my_cur.execute('SELECT * FROM FRUIT_LOAD_LIST')
    return my_cur.fetchall()

streamlit.title("My parent's new healthy Diner")
streamlit.header("Breakfast Menu")
streamlit.text("🥣Omega-3 Blueberry Oatmeal")
streamlit.text("🥗Kale, Spinach, and Rocket Smoothie")
streamlit.text("🐔Hard-Boiled Free-Range Egg")
streamlit.text("🥑🍞Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice: 
    streamlit.error('Please select a fruit to get information about')
  else: 
    norm_resp = get_fruityvice(fruit_choice)
    streamlit.dataframe(norm_resp)
except URLError as e:
  streamlit.error()



if streamlit.button('Get Fruit Load List'):
  my_data_rows = get_fruitLoadList()
  streamlit.header("Data from Fruit Load List")
  streamlit.dataframe(my_data_rows)

fruit_choice = streamlit.text_input('What fruit would you like to add', 'jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)

##my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ()")

