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

os.environ['OPENAI_API_KEY'] = os.environ.get('OPENAI_API_KEY')

query = "a blue circle in the top left of the screen"
#query = "3 circles within eachother. Biggest red, middle green, smallest black"
#query = "an input text field with a label 'enter your name' beside each other"

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
you always use this template to embed your reply: {zim_template}. You put your reply into the template after '// put code here'.
Your have the following variables given: F (Frame), S (Stage), W (width), H (height). So instead of 'stage.' use 'S.' when you code the zim content.
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

human_template="Create the follwoing in zim: {qa_result} and place it into your template (one line after the '// put code here'). Do not change the rest of your template. Reply with the whole index.html file."
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

response_chain = LLMChain(llm=llm, prompt=chat_prompt)
res = response_chain.run(zim_template=ZIM_TEMPLATE, qa_result=response)
print(res)