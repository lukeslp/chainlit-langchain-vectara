# Chainlit - Vectara & Langchain

## Conversational Retrieval with Sources

This is an implementation of a Conversational Retrieval Chain with Sources (LangChain) that performs a semantic search of a Vectara database, all with a Chainlit frontend and callbacks and other fancy bits.

*Getting Started*

Follow these steps to get going:

`git clone 

*Create a Vectara Index*

Visit Vectara to create a free index. Files can be uploaded and upserted via their web portal, so ingestion is not necessary.

*Create a virtual environment*

`python3 -m venv env`

*Activate the virtual environment*

On Windows, use:

`.\env\Scripts\activate`

On Unix, Linux, or MacOS, use:
`source env/bin/activate`

Install the requirements

`pip install -r requirements.txt`

Run the application

`chainlit run app.py`

## Keep building!

This base project is easily modified to use other chains, llms, and vectorstores. Make it your own! For more information about the tools used in this project, please visit their respective documentation:

- Chainlit Documentation
- LangChain Documentation
- Vectara Documentation

*Contributing*

I welcome contributions to this project. Please feel free to open an issue or submit a pull request. However, there's a larger project this feeds into that is worth discussing if you're considering contributing.

This project is licensed under the terms of the MIT license.
