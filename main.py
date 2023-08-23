import streamlit as st
import streamlit.components.v1 as components
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.document_loaders import TextLoader
from dotenv import load_dotenv
load_dotenv()

# os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY') - use this for local development with a .env file

ss = st.session_state

def on_api_key_change():
    api_key = ss.get('api_key') or os.getenv('OPENAI_API_KEY')
    os.environ['OPENAI_API_KEY'] = api_key

with st.sidebar:
    st.title('langchain-zim-generator')
    st.markdown('''
                ## About
    This LLM-powered app creates html code based on the ZIM template from https://zimjs.com/code.html
    - Source code: [github.com/ajerni/langchain-zim-generator](https://github.com/ajerni/langchain-zim-generator)
    
    ### The app needs a valid OpenAI Key to work. Get your own on [OpenAI](https://platform.openai.com/account/api-keys)
    ''')
    
    # st.text_input('OpenAI API key', type='password', key='api_key', on_change=on_api_key_change, label_visibility="collapsed")
    st.text_input('OpenAI API key', type='password', key='api_key', on_change=on_api_key_change)

def main():
    #query = "a blue circle and above it a label with the text 'it works'"
    #query = "3 circles within each other. Biggest red, middle green, smallest black"
    #query = "an input text field with a label 'enter your name' beside each other"
    st.header("ZIM code generator")
    st.write("Use ZIM terms like circle, rectangle, ... see [ZIM Docs](https://zimjs.com/docs.html)")
    st.markdown('''
                Examples:
                - a text label showing the text "Hello"
                - 3 circles within each other. Biggest red, middle green, smallest black
                - an input text field with a label "enter your name" beside each other
                ''')
    query = st.text_input('Enter what you want the AI to build:')

    if query:
        results = cenerateZIMcode(query)
        st.code(results, language='html')
        components.html(results, width=512, height=384)

def cenerateZIMcode(query):
    loader = TextLoader("zimdocs.txt")
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    vectorstore = FAISS.from_documents(docs, embeddings)

    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)

    similars = vectorstore.similarity_search(query=query, k=3)
    qa_chain = load_qa_chain(llm=llm, chain_type="stuff")
    response = qa_chain.run(input_documents=similars, question=query)

    ZIM_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8" />
    <title>ZIM - Code Creativity</title>

    <!-- zimjs.com - JavaScript Canvas Framework -->
    <script type=module>

    import zim from "https://zimjs.org/cdn/015/zim";

    // See Docs under Frame for FIT, FILL, FULL, and TAG
    new Frame(FIT, 1024, 768, light, dark, ready);
    function ready() {
        // given F (Frame), S (Stage), W (width), H (height)
        // put code here
            
    } // end ready

    </script>
    <meta name="viewport" content="width=device-width, user-scalable=no" />
    </head>
    <body></body>
    </html>
    """

    system_template="""You are a javascript expert using the zimjs framework.
    you always use this template to embed your reply: {zim_template}. You put your reply into the template after '// put code here'. You never need to create a Stage.
    You already have the following variables given: F (Frame), S (Stage), W (width), H (height). So instead of 'stage.' use 'S.' when you code the zim content.
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template="Create the follwoing in zim: {qa_result} and place it into your template (one line after the '// put code here'). Do not change the rest of your template. Reply with the whole index.html file."
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    response_chain = LLMChain(llm=llm, prompt=chat_prompt)
    res = response_chain.run(zim_template=ZIM_TEMPLATE, qa_result=response)
    print(res)
    return res

if __name__ == '__main__':
    main()