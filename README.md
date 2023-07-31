# FetchMatchAI Prompt_Engineering Demo

This repository contains detailed information on the FetchMatchAI Streamlit Web App built to:
- Use any keyword to search for relevant offers
- Ask any question to the app based on the Fetch Offer data

## Instructions and Set of Responsibilities



The objective of this Take Home test is to take a string as an input and give the list of all of the offers that matches to the string.

**The acceptance criteria must contain the requirements below:**
- If a user searches for a category (ex. diapers) the tool should return a list of offers that are relevant to that category.
- If a user searches for a brand (ex. Huggies) the tool should return a list of offers that are relevant to that brand.
- If a user searches for a retailer (ex. Target) the tool should return a list of offers that are relevant to that retailer.
- The tool should also return the score that was used to measure the similarity of the text input with each offer

**The submission must include:**
- A link to a GitHub repository containing your code
- A link to a hosted version of your tool (if applicable)
- A brief writeup of your approach to the problem, including any assumptions you made and any tradeoffs you considered
- Instructions on how to run your tool locally, if applicable

**Hints on what this submission needs:**
- Detailed responses to each problem, with a focus on the production pipeline surrounding the model. 
- Identifies several useful techniques to approach eReceipt classification and entity extraction. 
- Demonstrate a knowledge of recent innovations in NLP and a willingness to think about the problem in terms of software engineering rather than an academic exercise.

## **Solution**

Please find the following deliverables attached in this GitHub repository:
- Video demonstrating all functionalities of FetchMatchAI StreamLit Web App
- Repository hosting all code to run .py and streamlit app

## Installation
In order to run this app successfully, please download the packages below:

```bash
pip install langchain
pip install openai
pip install ipynb
pip install fuzzywuzzy
```
    
## API Reference

#### Use an OpenAI API Key

```http
https://platform.openai.com/account/api-keys
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Requires**. Your API key |

Note: For the purpose of this demo, I have used my personal OpenAI API Key.



## Next Steps

- In order to scale this solution, we can productionalize it by hosting massive data on vector databases like PineCone, ChromaDB, Weaviate, etc.
- Using similarity search on text embeddings, we can retrieve a subset of this vector database to work with
- Once we have our targeted DB subset, we can use prompt engineering and LLMs to retrieve relevant information in the form of offers, brands, categories and products. 

**Set of instructions in the attached code as per the cell number**


**Python Cell 1:**

- The first cell identifies all of the relevant packages that need to be installed and loaded in our environment in order to run the code successfully.

**Jupyter Cell 2:**
- In this cell, I am loading all required datasets into the notebook
- I have also performed certain join, and lower case functions on the dataset to create only one data frame from all of the different input .csv files.

**Jupyter Cell 3:**
- In this cell, I have written relevant prompts and built the required Python DF Agent in order to run the LLM model (GPT 3.5 - 16K Context Token Length) on the offer data.

**Juppyter Cell 4:**

This is the cell that hosts the final function to call Python agents on various user inputs to return a list of offers based on an input user keyword.

**Jupyter Cell 5:** 

This cell includes an additional section where we can ask the Python DF Agent any question on the offer data. These questions could be related to the offers, brands, products, categories or receipt and it will provide the relevant information.

## Challenges
- The major challenge is that, as of March 1, 2023, OpenAI no longer retains customer API data. This means that any data provided by the user via the API is not kept by OpenAI beyond the immediate processing of the API request. However, they might change it in the near future, in that case, the entire strategy needs to be revised if that happens.
- Since OpenAI provides open-source GPT models, we can protect our data privacy by training and fine-tuning an in-house LLM model, which would require additional resources.  

## Deployment

To deploy this project run

```bash
pip install streamlit
```

Navigate to the WebApp folder and run the command below,

```bash
streamlit run Home.py
```

**Thank you and hope you like this demo :D**

