# joke_engine
This was just me getting 2 desktop LLMs on Ollama to talk to each other. One is the coach, the other the generator, and their goal is generate jokes.  
The jokes are terrible... but it's a fun experiment


Ollama must be installed and running locally, and the specific models must also be installed locally.
Models are selected and controlled in config.py

Once Ollama is installed, the easiest way to install a model is from command line/terminal:
> ollama run <model_name>
for example:
> ollama run llama3.2:3b

I am running on a lower end i9 with 32GB, no graphics card on this machine, so it's not a big rig.
Generator runs for 10 iterations, and you can prime it with a joke of your own. 
I am now using this basic framework to generate and evaluate local LLM prompts, using one LLM to evaluate and fine-tune the results...
