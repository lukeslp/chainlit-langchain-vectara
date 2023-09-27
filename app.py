# app.py

import os
import logging
from datetime import datetime
from typing import List

import chainlit as cl
from dotenv import load_dotenv

from langchain.chat_models.openai import ChatOpenAI
from langchain.vectorstores import Vectara
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.combine_documents.base import BaseCombineDocumentsChain
from langchain.chains.qa_with_sources.retrieval import RetrievalQAWithSourcesChain
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
from langchain.docstore.document import Document

from chainlit.input_widget import Select, Switch, Slider

load_dotenv()

# Input your API keys in .env
vectara_instance = Vectara(
    vectara_customer_id=os.environ.get("VECTARA_CUSTOMER_ID"),
    vectara_corpus_id=os.environ.get("VECTARA_CORPUS_ID"),
    vectara_api_key=os.environ.get("VECTARA_API_KEY"),
)


@cl.on_chat_start
async def start():
    # Define chat settings
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI - Model",
                values=["gpt-3.5-turbo", "gpt-3.5-turbo-16k",
                        "gpt-4", "gpt-4-32k"],
                initial_index=1,
            ),
            Switch(id="Streaming", label="OpenAI - Stream Tokens", initial=True),
            Slider(
                id="Temperature",
                label="OpenAI - Temperature",
                initial=0,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()
    # Call the setup_agent function with the chat settings
    await setup_agent(settings)


@cl.on_settings_update
async def setup_agent(settings):
    # Initialize chat message history and conversation buffer memory
    message_history = ChatMessageHistory()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        output_key="answer",
        chat_memory=message_history,
        return_messages=True,
    )

    # Initialize conversational retrieval chain
    llm = ChatOpenAI(model_name=settings["Model"],
                     temperature=settings["Temperature"], streaming=settings["Streaming"])
    chain = ConversationalRetrievalChain.from_llm(
        llm,
        chain_type="stuff",
        retriever=vectara_instance.as_retriever(),
        memory=memory,
        return_source_documents=True,
    )
    # Set chain in user session
    cl.user_session.set("chain", chain)


@cl.on_message
async def main(message):
    # Get chain from user session
    chain = cl.user_session.get("chain")
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=False,
    )
    cb.answer_reached = True

    # Call chain with message and callback
    res = await chain.acall(message, callbacks=[cb])
    answer = res["answer"]
    source_documents = res["source_documents"]
    text_elements = []
    source_names = []

    # If source documents exist, process them
    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"Source {source_idx + 1}"
            text_elements.append(
                cl.Text(content=source_doc.page_content, name=source_name)
            )
        source_names = [text_el.name for text_el in text_elements]

    # Append sources to answer
    if source_names:
        answer += f"\nSources: {', '.join(source_names)}"
    else:
        answer += "\nNo sources found"

    # Update final stream if it has been streamed, else send message
    if cb.has_streamed_final_answer:
        cb.final_stream.content = answer
        cb.final_stream.elements = text_elements
        await cb.final_stream.update()
    else:
        await cl.Message(content=answer, elements=text_elements).send()

    log_directory = os.getenv('LOG_DIRECTORY')
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(
        log_directory, f"log_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt")

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"User input: {message}\n")
        f.write(f"Response: {answer}\n")
