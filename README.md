# About

Code for AI-generated Podcast by Claude and GPT.

Create `.env` file in project and put your OpenAI and Anthropic keys as follows:

```
OPENAI_API_KEY=sk-xxxx
ANTHROPIC_API_KEY=sk-ant-xxxx
```
Then, do the following and run the notebook.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

- [01-openant-conversation.ipynb](01-openant-conversation.ipynb): code to generate the conversation scripts.
- [02-tts.ipynb](02-tts.ipynb): code to generate mp3 based on the conversation scripts.