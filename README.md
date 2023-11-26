# SupportAI
## _Support Made Simple_

SupportAI is an AI chatbot which uses a predefined knowledge base to answer questions
regarding the Exact Globe CMS.

- Contribute to knowledgebase
  > In order to contribute to the knowledgebase put your data in a `data` folder and make sure that if you have images, they are also in the folder so that they can be uploaded to the blob storage 
- Ask questions and recieve answers

## Features

- Upload HTML files to the knowledgebase of the application
- Ask questions regarding features and issues in relation to the Exact Globe CMS

## Tech

SupportAI uses a number of external resouces listed below:

- [streamlit] - turns data scripts into shareable web apps
- [LangChain] - a language model integration framework
- [SentenceTransformers] - easy methods to compute dense vector representations for sentences
- [OpenAI GPT] - API for accessing AI models developed by OpenAI.
- [Pinecone] - database that stores data as mathematical vectors
- [HuggingFace Pretrained LLM] - Pretrained multilingual llm that transforms sentences to vectors
- [Azure Storage Account] - unique namespace for your Azure Storage data that's accessible from anywhere in the world over HTTP or HTTPS.
- [Docker Engine] - helps developers build, share, and run applications anywhere — without tedious environment configuration or management
- [Docker-compose] -  tool for defining and running multi-container Docker applications

## Prerequisites
- Pincone project + api key
- OpenAI API key
- Azure Subscription + storage account

Create a `.env` file in the root of the project and include the following contents:
```sh
OPENAI-API-KEY={your-openai-key}
PINECONE-KEY={your-pinecone-key}
PINECONE-ENV={your-pinecone-env}
AZURE-STORAGE-CONNECTION-STRING={your-azure-storage-connection-string}
AZURE-BLOB-CONTAINER={your-blob-container-name}
```

## Installation

SupportAI requires 
- [Python] - v3.10.x to run.
- [Pip]

<details>
<summary>Manual Setup</summary>
Create a venv, install the dependencies and start the server.

```sh
python -m venv .\.venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
streamlit run .\main.py
```
</details>

#### Automatic Setup
Run the `setup_and_run.ps1` powershell script

Verify that the application is working by navigating to your server address in
your preferred browser.
```sh
Local URL: http://localhost:8502
Network URL: http://192.168.178.243:8502
```

#### Using the Official Docker container
SupportAI can be run using the docker-compose.yml file. All you need to do is provide an `.env` file in the `/app` folder with the 
abovemenitoned variables. After you do that simply run:

```sh
docker-compose up
```
> NOTE: In order for this method to work you need both Docker Engine and the Compose plugin installed and running on your machine

You should see an interface that looks like this:
![image](https://github.com/Axians-AI/AxiansSupportAI/assets/102069965/e35952bb-d2ab-47e1-a286-9a4fa106c99f)

## License

© Axians 2023 (TBD)

   [streamlit]: <https://streamlit.io/>
   [LangChain]: <https://www.langchain.com/>
   [SentenceTransformers]: <https://www.sbert.net/>
   [OpenAI GPT]: <https://openai.com/>
   [Pinecone]: <https://www.pinecone.io/>
   [HuggingFace Pretrained LLM]: <https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2>
   [Azure Storage Account]: <https://learn.microsoft.com/en-us/azure/storage/common/storage-account-overview>
   [Python]: <https://www.python.org/>
   [Pip]: <https://pip.pypa.io/en/stable/installation/>
   [Docker Engine]: <https://www.docker.com/>
   [Docker-compose]: <https://docs.docker.com/compose/>
