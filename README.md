# Chainlit - Vectara & Langchain

## Conversational Retrieval with Sources

This is an implementation of a Conversational Retrieval Chain with Sources (LangChain) that performs a semantic search of a Vectara database, all with a Chainlit frontend including chat settings and other fancy bits.

Blame this guy -> luke@lukesteuber.com

---

### Configure and Run

1. **Create a Vectara Index**

Visit [Vectara's Getting Started page](https://vectara.com/developers/getting-started/) to create a free index. Files can be uploaded and upserted via their web portal, so ingestion is not necessary in this file.

2. **Clone the repo and switch directories**

```
git clone https://github.com/lukeslp/chainlit-langchain-vectara.git
cd chainlit-langchain-vectara
```

3. **Create a virtual environment**

```
  python3 -m venv env
```

4. **Activate the virtual environment**

_On Windows, use:_

```
.\env\Scripts\activate
```

_On Unix, Linux, or MacOS, use:_

```
source env/bin/activate
```

5. **Install the requirements**

```
pip install -r requirements.txt
```

6. **Add API Keys**

Add API keys to .env.example and rename to .env

7. **Run the application**

```
chainlit run app.py
```

---

### Keep building!

This base project is easily modified to use other chains, llms, and vectorstores. Make it your own! For more information about the tools used in this project, please visit their respective documentation:

- [Chainlit Documentation](https://docs.chainlit.io/overview)
- [LangChain Documentation](https://langchain.io/docs)
- [Vectara Documentation](https://vectara.io/docs)

_Contributing_

I welcome contributions to this project. Please feel free to open an issue or submit a pull request. However, there's a larger project this feeds into that is worth discussing if you're considering contributing. Contact me by [email](mailto:luke@assisted.space), discord (lukelinguist), or visit [luke.augcom.tech](https://luke.augcom.tech).

_This project is licensed under the terms of the MIT license._
