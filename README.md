# langchain-zim-generator

This python script uses langchain and OpenAI to create an index.html file containing ZIM code.
It takes the whole zimdocs.txt file (thanks to Dr. Abstract - https://zimjs.com/docs.html), splits it into smaller pieces that are embedded in a vectorsore. The query is placed in the same vectorstore and returns similar chunks from the documentation, from which a ZIM code is generated using some very clever 😉 prompt engineering.

## How to Use

1. Git Clone: `git clone https://github.com/ajerni/langchain-zim-generator.git`
2. Move to the new directory: `cd langchain-zim-generator`
3. Create Virtual Environment: `python -m venv env` or `python3 -m venv env` (on Windows: `python -m venv c:\path\to\env`)
4. Activate Virtual Environment: `source env/bin/activate` on Mac or `env\Scripts\activate` on Windows
5. Install Dependencies: `pip install -r requirements.txt`
6. Create a .env file containing your OpenAI Key: `echo "OPENAI_API_KEY=xyz" > .env` (replace xyz with your own OpenAI Key)
7. In main.py line 19 change the query string to whatever you want (use Zim terms circle, label, etc.) like: `3 circles within eachother. Biggest red, middle green, smallest black`
8. Run it: `python main.py` or `python3 main.py`
9. Copy and paste the output into your own `index.html` - open it as your usual ZIM file!
10. Fork my repo and start developing until we have the ultimate ZIM-Auto-Pilot 🚀

## Credits

- Dr. Abstract for his amazing ZIM: https://zimjs.com

## To-Dos:

- create a FastAPI endpoint to run it on Vercel, Google Cloud or so...
- Prommpts need further finetuning
- later on I can think of using langchain agents to include google search for pictures which can be added to the stage etc.
