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

pd.options.display.float_format = '{:.2f}'.format

# Setting the openai key
st.set_page_config(layout="wide",page_title='EDA Module')
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')


#######################################################################

# Title and header
st.title("FetchMatchAI Offer Search")
st.subheader("Using Large Language Models (LLMs) and Prompt Engineering to perform offer search")
st.write("This demo will pull ongoing offers based on any user input keyword.")
st.markdown("<hr>", unsafe_allow_html=True)

############################################################################

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

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

#Take user input:
st.write("Enter Search Keyword for Relevant Offers: ")
user_input = st.text_input("")
button_clicked = st.button("OK")


# Defining Functions and Prompts


#Create LLM Generators that will use the above prompt

def search_query_generator(user_input,offer_retailer):

    search_query_output = ""

    offer_search_prompt_string = PromptTemplate(
    input_variables = ['user_input','offer_retailer'],
    template = """
        
        -------------------------------------------------------------
        # Role and Responsibility
        -------------------------------------------------------------
        
        GOAL: Find the column in {offer_retailer} that contains the string or sub-string of {user_input}
        
        -------------------------------------------------------------
        # Process
        -------------------------------------------------------------
        
        Step 1: Perform a similar, case insensitive search match for {user_input} in {offer_retailer}
        Step 2: Return the column name from {offer_retailer}
        
        -------------------------------------------------------------
        # Data To Be Used
        -------------------------------------------------------------
        
        Dataset to Use:
        **********************
        {offer_retailer}
        
        Columns to Use:
        **********************
        1) Retailer
        2) Brand
        3) Category
        4) Product
        

        -------------------------------------------------------------
        # Conditions
        ------------------------------------------------------------- 
        - Only return ONE FINAL COLUMN NAME
        
       
        -------------------------------------------------------------
        # IMPORTANT INSTRUCTIONS
        -------------------------------------------------------------
        
        RETURN THE FINAL OUTPUT AS THE NAME OF THE COLUMN FROM {offer_retailer}
        FINAL RESULT SHOULD BE ONLY ONE WORD
        
        EXAMPLE 1:
        ^^^^^^^^^^^
        If the right column to search {user_input} in is "Brand", then:
        Your Answer: "Brand"
        
        
        EXAMPLE 2:
        ^^^^^^^^^^^^
        If the right column to search {user_input} in is "Product", then:
        Your Answer: "Product"
            
        EXAMPLE 3:
        ^^^^^^^^^^^^
        If the right column to search {user_input} in is "Category", then:
        Your Answer: "Category"
        
        
        Column Name:
        ....
       
        """
    )

    # Create LLMChain associated with offer search prompt
    search_query_generator_string = LLMChain(
        llm=ChatOpenAI(model_name='gpt-3.5-turbo-16k', temperature=0.2, max_tokens=10000), 
        prompt=offer_search_prompt_string
    )

    #Call associated Search Query Generator to run on user input and offer_retailer data
    search_query_output = search_query_generator_string.run({
            
            'user_input': user_input,
            'offer_retailer': offer_retailer
        })

    return search_query_output

#Creating a python agent on the associated dataframe
def create_python_agent(df):
    python_agent = 0
    python_agent = create_pandas_dataframe_agent(OpenAI(temperature=0.2), df, verbose=True)
    return python_agent


def display_code_with_delay(text, delay):
    display_code = ""
    for char in text:
        display_code += char
        st.markdown(f'<pre style="display:inline">{display_code}</pre>', unsafe_allow_html=True)
        time.sleep(delay)



#Creating wrapper functions for associated Python Code
# Following function will return the final list of offers if found by Python DF Agents
def offer_search_output_list(user_input,offer_retailer):

    # Converting user input to lower case format
    user_input = user_input.lower()

    # Creating a Python DF Agent on a dataset with all small values
    py_df_agent_analyzer = create_python_agent(offer_retailer)

    # Running the Python DF Agent on the output returned by above prompt
    Offer_pull_list = py_df_agent_analyzer.run("GOAL: To find a list of offers. \n" +
                                           "that contain the keyword " + user_input
                                          )

    st.write("Offers Pulled: \n")

    non_existant_string_check = "no offers that contain"
    #There are no offers that contain the keyword cake.
    if non_existant_string_check not in Offer_pull_list:
        st.write(Offer_pull_list)

    else:
        #Part 2: Search the keyword in a particular column, then use that column as a filter to search for all the offers
        Right_Column_to_Search = search_query_generator(user_input,offer_retailer)

        # Running the Python DF Agent on the output returned by above prompt
        Offer_pull_list = py_df_agent_analyzer.run("GOAL: To find a list of offers. \n" +
                                               "Step 1: Find a fuzzy match for the string: \n"
                                               + user_input +
                                               "\n in the column : " + Right_Column_to_Search +"\n"
                                               + "The offer should contain: " + user_input 
                                               + "Step 2: Return a list of offers."
                                               + "NOTE: Ignore Null values."
                                              )
        
        if non_existant_string_check not in Offer_pull_list:
            st.write(Offer_pull_list)
        else:
            st.write("Apologies! No offers found")


offer_search_output_list(user_input,offer_retailer)





    
###########################################################################






    

    
