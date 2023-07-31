#!/usr/bin/env python
# coding: utf-8

# Importing the necessary libraries
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import pandas as pd

#Import Python DF Agent Related libraries
from langchain.agents import create_pandas_dataframe_agent
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.llms import OpenAI
import openai
import contextlib
import io
import os
from IPython.display import display, HTML
from services import  redirect

pd.options.display.float_format = '{:.2f}'.format

# Setting the openai key
st.set_page_config(layout="wide",page_title='EDA Module')
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

###############################################s#################################################
# Title and header

st.title("Ask me Anything!")
st.write("The FetchMatchAI agent can answer any business questions based on the offer data")
st.markdown("<hr>", unsafe_allow_html=True)


# Read the dataset as input
brand_category = pd.read_csv('Brand_Category.csv')
categories = pd.read_csv('Categories.csv')
offer_retailer = pd.read_csv('Offer_Retailer.csv')
    
# Joining all dataframes to get a final table
offers_brand_w_category = pd.merge(offer_retailer,brand_category, on="BRAND", how='left')
offers_brand_w_category_w_Deets=pd.merge(offers_brand_w_category,categories, left_on="BRAND_BELONGS_TO_CATEGORY", right_on="IS_CHILD_CATEGORY_TO", how='left')

# Turn all values to lower case
offers_brand_w_category_w_Deets = offers_brand_w_category_w_Deets.applymap(lambda s: s.lower() if type(s) == str else s) 

# Dropping certain columns and re-naming a few other columns
offer_retailer = offers_brand_w_category_w_Deets.drop(columns=['IS_CHILD_CATEGORY_TO'])
offer_retailer.rename(columns = {'BRAND_BELONGS_TO_CATEGORY':'Category',
                                                  'PRODUCT_CATEGORY':'Product'},
                                       inplace = True)


##############################################################################################
# Defining the functions

#creating a python agent on the associated dataframe
def create_python_agent(df):
    python_agent = 0
    python_agent = create_pandas_dataframe_agent(OpenAI(temperature=0.4), df, verbose=True)
    return python_agent

###################################################################################################



# Creating a Python DF Agent
py_df_agent_analyzer = create_python_agent(offer_retailer)

# Crating a text area for user input
user_input = st.text_input('Ask FetchMatchAI: ')
submit = st.button('Submit')

if submit:
    st.write("**Model's thoughts:**")
    with redirect.stdout:
        st.write(py_df_agent_analyzer.run(user_input))







    # submit = st.form_submit_button(label="Ask")

    # if submit:
    #     py_df_agent_analyzer.run(user_input)

    