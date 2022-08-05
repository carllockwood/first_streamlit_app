import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError
streamlit.title('Breakfast Favorites')

streamlit.header('Breakfast Menu')
streamlit.text ('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text ('🥬Kale, Spinish & Rocket Smottie')
streamlit.text ('🐔Hard-Bolied Free-Range Egg')
streamlit.text ('🥑🍞Advocado Toast')

streamlit.header('🍌🍓Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  
  if not fruit_choice:
    streamlit.error("Please select a fruit")
  else:
    
    #import requests
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    # not executed streamlit.text(fruityvice_response.json())
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
except URLError as e:
    streamlit.error()
    
# frames the response
streamlit.dataframe(fruityvice_normalized)

streamlit.stop()

#import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.header("The first recordContains:")
streamlit.text(my_data_row)

my_data_rows = my_cur.fetchall()
streamlit.header("The fruit Load List Contains:")
streamlit.dataframe(my_data_rows)
