# scribe-buddy -app 
[Meet your scribe-buddy here](https://anshumantiware-scribe-buddy-app-8zp025.streamlit.app/)

# Description 

This web application is designed to create transcription for the Youtube videos. Once the transcription is finished, the application also provides a few sentences summary for the content of the video. This app is powered by the "Assembly AI" and the latest generative model - "ChatGPT". In order to run this application locally on the computer system, a user would need to provide their unique API keys for Assembly AI and ChatGPT3 using the process described below. The overll functionality of the app is shown in the tutorial video below. 

The project contains a file named 'requirements.txt'. This is the file with the list of all the libraries required to run the project. The file contains both the names as well as the exact versions of the libraries involved. 

The folder also contains the image of the logo of the transcriber app. 

The file "app.py" contains the actual code for this projects. This file explains the code to first convert the youtube video to an audio file. The transcription is then performed on this audio file using the Assembly AI API. The authorization to use Assembly AI API is performed using the API key of the user. Similarly, the ChatGPT (from Open AI) is used to summarize the transcription. It is recommended to use this summarization feature for videos where only one person is speaking (in other words a single speaker video). The ChatGPT model in it's current form was found to be getting stuck and unable to summarize in case of multi-speaker videos. 

The app reads the APIs of the user from the input fields provided in the sidebar of the application. 

For those people who might want to tinker with different prompts to ChatGPT (for example instead of summarization you might want to get a complete essay on the theme of the speech in the video, feel free to clone the scribe-buddy repository and modify the prompt accordingly.)
Here is the link to the repository.


```
https://github.com/AnshumanTiware/scribe-buddy
```
# Watch the tutorial video
[Watch the web app in action in the video here](https://youtu.be/Lt4nL410TmU) 

# 1. Obtain the AssemblyAI and OpenAI API keys

Get your free [AssemblyAI API key](https://www.assemblyai.com/?utm_source=youtube&utm_medium=social&utm_campaign=dataprofessor).

[This is how you get your OpenAI API key](https://elephas.app/blog/how-to-create-openai-api-keys-cl5c4f21d281431po7k8fgyol0)

The API keys for the Assembly AI and OpenAI need to be pasted in the relevant places in the secrets.toml file in the .streamlit folder of the application. 

# 2. Running scibe-buddy app as a Streamlit app
This application can be ran as a streamlit web application on your browser. Follow the steps below to run this application. 

### Create conda environment (Optional)
We create virtual environments to ensure that specific version of various libraries which we need for a particular project (in this case a web application called scribe-buddy app) do not interfere with/ uninstall the other versions of these libraries already installed in the system. These other versions of the libraries would be required for the other projects. We can create a virtual environment using conda. 

Conda is an open source package management system and environment management system that runs on Windows, macOS, and Linux. Conda quickly installs, runs and updates packages and their dependencies. Conda easily creates, saves, loads and switches between environments on your local computer. It was created for Python programs, but it can package and distribute software for any language.

First, create a new conda environment called *scribe_buddy*
```
conda create -n scibe_buddy python=3.7.9
```
Second, activate the *scibe_buddy* environment
```
conda activate scibe_buddy
```

###  Download GitHub repo

```
git clone https://github.com/dataprofessor/transcriber-app
```

###  Pip install libraries
```
pip install -r requirements.txt
```

###  Launch the app

```
streamlit run scribe_buddy.py
```

### Acknowledgement 

I would like to give special thanks to Chanin Nantasenamat for his streamlit application videos on Youtube to showcase different project ideas as well as his tutorials on using streamlit for hosting web applciations. 

### References

1) https://docs.conda.io/en/latest/
2) https://www.youtube.com/@DataProfessor
3) https://github.com/terry3041/pyChatGPT
4) https://github.com/dataprofessor/transcriber-app
5) https://www.youtube.com/watch?v=83-oicTOL70&t=362s
6) https://www.youtube.com/watch?v=pyWqw5yCNdo&t=5s


