import openai
import streamlit as st
from pytube import YouTube
import os
import sys
import time
import requests
from zipfile import ZipFile
from pyChatGPT import ChatGPT
from PIL import Image

st.markdown('# 📝 **Scribe-Buddy**')
bar = st.progress(0)


# Applying the Custom CSS to the Streamlit App 
page_bg_image = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://images.unsplash.com/photo-1525529336036-0b3faed361b7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=880&q=80");
background-size: cover;
}

[data-testid="stSidebar"]{
background-image: url("https://images.unsplash.com/photo-1518717202715-9fa9d099f58a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2129&q=80");
background-size: cover;
}
</style>
""" 
st.markdown(page_bg_image, unsafe_allow_html=True)
# Custom functions git 
# 1.Remove Redundant Files from the current directory
import os 
path1= './yt.srt'

path2= './yt.txt'
path3= './transcription'
isExist1 = os.path.exists(path1)
isExist2 = os.path.exists(path2)
isExist3 = os.path.exists(path3)
if isExist1:
    os.remove("./yt.srt")
    print("Yes1")
if isExist2:
    os.remove("./yt.txt")
    print("Yes2")
if isExist3:
    os.rmdir("./transcription")
    print('Yes3')
for File in os.listdir("."):
    if File.endswith(".mp4"):
        os.remove(File)
for File in os.listdir("."):
    if File.endswith(".zip"):
        os.remove(File)

# 2. Retrieving audio file from YouTube video
def get_yt(URL):
    video = YouTube(URL)
    yt = video.streams.get_audio_only()
    yt.download()

    #st.info('2. Audio file has been retrieved from YouTube video')
    bar.progress(10)

# 3. Upload YouTube audio file to AssemblyAI
def transcribe_yt():

    current_dir = os.getcwd()

    for file in os.listdir(current_dir):
        if file.endswith(".mp4"):
            mp4_file = os.path.join(current_dir, file)
            #print(mp4_file)
    filename = mp4_file
    bar.progress(20)

    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data
    headers = {'authorization': api_key}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename))
    audio_url = response.json()['upload_url']
    #st.info('3. YouTube audio file has been uploaded to AssemblyAI')
    bar.progress(30)

    # 4. Transcribe uploaded audio file
    endpoint = "https://api.assemblyai.com/v2/transcript"

    json = {
    "audio_url": audio_url
    }

    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }

    transcript_input_response = requests.post(endpoint, json=json, headers=headers)

    #st.info('4. Transcribing uploaded file')
    bar.progress(40)

    # 5. Extract transcript ID
    transcript_id = transcript_input_response.json()["id"]
    #st.info('5. Extract transcript ID')
    bar.progress(50)

    # 6. Retrieve transcription results
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {
        "authorization": api_key,
    }
    transcript_output_response = requests.get(endpoint, headers=headers)
    #st.info('6. Retrieve transcription results')
    bar.progress(60)

    # Check if transcription is complete
    from time import sleep

    while transcript_output_response.json()['status'] != 'completed':
        sleep(5)
        st.warning('Transcription is processing ...')
        transcript_output_response = requests.get(endpoint, headers=headers)
    
    bar.progress(100)

    # 7. Print transcribed text
    st.header('Output')
    st.success(transcript_output_response.json()["text"])
    text_to_summarize = "Summarize in maximum 25 words: " +  transcript_output_response.json()["text"]

    # 8. Save transcribed text to file

    # Save as TXT file
    yt_txt = open('yt.txt', 'w')
    yt_txt.write(transcript_output_response.json()["text"])
    yt_txt.close()

    # Save as SRT file
    srt_endpoint = endpoint + "/srt"
    srt_response = requests.get(srt_endpoint, headers=headers)
    with open("yt.srt", "w") as _file:
        _file.write(srt_response.text)
    
    zip_file = ZipFile('transcription.zip', 'w')
    zip_file.write('yt.txt')
    zip_file.write('yt.srt')
    zip_file.close()
    return text_to_summarize
#####

# The App

# 1. Read API from text file
#api_key = st.secrets['api_key']

# 1. Read API from User Input
st.sidebar.header('May I Ask You To')


with st.sidebar.form(key='my_form1'):
	api_key = st.text_input('Enter API Key for Assembly AI:')
	submit_button = st.form_submit_button(label='Go')

with st.sidebar.form(key='my_form2'):
	openai.api_key = st.text_input('Enter API Key for OpenAI:')
	submit_button = st.form_submit_button(label='Go')

with st.sidebar.form(key='my_form'):
	URL = st.text_input('Enter URL of YouTube video:')
	submit_button = st.form_submit_button(label='Go')

#st.info('1. API is read ...')
st.warning('Awaiting URL input in the sidebar.')

# Sidebar
# Run custom functions if URL is entered 
if submit_button:
    get_yt(URL)
    text_to_summarize = transcribe_yt()

    with open("transcription.zip", "rb") as zip_download:
        btn = st.download_button(
            label="Download ZIP",
            data=zip_download,
            file_name="transcription.zip",
            mime="application/zip"
        )

        # Printing the summary of the text
        #session_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..4ZpHuTqsNB6QqqAx.0kDIak8exZ8oihItU-jdpga2qjpOuggEuaBjCR_pb6ddu-ykhyrew___SbTziuY94tUxGHBOlzbaielqU17Kr_8SZ308iXO1ZOVAT7RWPED6iGI5zvkW6rl4SgEoPJLSXEq8AKRA2brc7jy5382qMNtMIVB1tY-v_AAcKNkbwJ3V9d1NVZxnm8XhNT1tHtfRBKVb9O_TTXNRqBBiur4TMuzs1ZDIhClt31opPFXQAJFZ2gG1aB_aFmM543GM6vjRlq_Xez4zp7OLMLie4vWgQhFsUTOCT8VEg391bXB4pfJ5g8UO2u1qvWX0m3f6s2DfaWZkn7scbIve6N65mNxayh3xHpIbNkONFBsHNTESETeHw8rzzpGlstw0oSfBTFLdrymoy0JNtIKlRVUtFbjjtC-a4nsApjgjXfEQ6mW5lJTqpXYhpbe8Dwg4JZEVxuDv28aFmWEIhFNnpYxLmUUVSqqxgt8atSOi1JysCbdWx3Z6Os6nH2ROcfqt273j4rOV3QNPy7liUyLE9Pf28_YIcoRzf5GzUZOW26nVJR6p7_ih9M9MJnoR9aG6Xp5kJCbZ5WvWoNKnTOi3mvG2MdV9ythS3sMCN07lL7RTBPUTJDJlLGRJ0BGJAO-6lO_KNV0Rm1oJXWCH-uhrDlVozUd8KbSg8En_Rw_jmKyyfE3CUKE-qb-4CiNkbfxD2tNJJMFpydHP5z6doN1iJWdA8jk5K2iz2nVKcKnAsAcjNrP39V_ZSbVQPYvAUcJK3BoDQ3U_CIbUh4dpB05-blKudztLhpbxRl0pVrKc2bWjl1bEUtArKZSZaZAobPUUtgZs2-n0Gv7GW5_IDKB8gc5sUB2WHaYaOxuSGRHoYbQKMEEu-uPHX8YT99HS-YGhBTBGMRGMvQmADpjim9DM8uq_S2BSriqsukN_5LriX2JwaGrRcK77oVUzItAW1reNLuCowrlco1264HGmRTi7Fx-gR8GS2ab25cnIJjXYqua5X5RYsND74uMmqefbCtknUiQ1bwYjS5nOxO2LtOjY2uoCXv72tCHCNWXvNWn_CdV5Fm4P8zhGdAKrzpxuHCZIs53lHHht9kMvuExFBQuMqOPgaQE-wcswPdZjjJEbdz5dUWZ-T4eKx_mef92cvP2vleQFzfMzYXM5h4nUF0X2j-hTc9ap3XR33wFTxD4Ij8IQmy0mBDeRVVJkf0Cu2ElSG2mM0DZyN4Qvb56KL4WHdv4_HOtTc8vO7mHH6roSCCSR0lNpj1R5ZwPfnKrU4PXi8tCS4K9pmBqw6yCzvfdMog6tr66f_269ra7hS6L60emDi3EzVXvSJ3kAVfqktS-bYFi0fTEcS2vbvM1EeYIUC4Goro7Nvt4bhH95G-zOEDXjFYOezmLMC-kJF_XSYktdP4zlM8zeH1tG7DkeoBAn37E5H184FZLWIlTeatgW_4VeGuLHq6AlOwr7vQjgkqG-M-b3tLIJZqdRi4VK-J0sWKKDK1R89BZ6Q-jwDv_oFYCIqR68KtASF7dYyg_48IsrHeOFSAMCkGlLrxilNn4Dt89IC5d91JIQfcgpNYRc-ZPi5Xohr5ChpvUAzc5TGcSgJXCKHQGImXAYdEFp1FESnQKMXjU1Qx-pTVCkpr62ZKa91rOM8GVmfYFjXhCoqFWW7aEqQPYLUJJ9fqgaWZUrnOs8d7sO6dcujb-5im5x6TGTApoYV0BXUbxbaU53eZ4WAttxieTOiQuVgrgRkPyBiK-irC9BJKm1SPqsj_EkSCwF4tyitHEN3BrtMUr8gl7lQFi3lO_PvRLAlyATtNHS9VwOFbn4yqR_GwmQN0gyyIApuL6QO6KnfphB48ccgXP8epVt4MGuM4eqjQOiI-jl1qNDdPIngaGisl_i5HbjTZi17eKrY39hvDWitcBkceKGLgPK2lurTA-DNGGTYBLSwhgHn2Axoc0vNqroDgHT1i03IEnrTz3PFeDemYhzgB-9M4L9dUAxCaT-je1u3uQYqIr1_4WBhFlD2Og0QvkpgN5NbYpUz5P5WECGKWw1OxKh6VnNB7UfJn6ETGeyu-QoBKyCJfj_Ap2IvNyPMC46cP7IefJmzZVe49HIrN4pr_g1hsNSxPrqQjsTy0XEJEtHBZGm8EgAF43zPa5VrkL6Gas8kFanTYD0CTNMYLwkrwWE1MQF_tdn6JzFogKdUh5N-A3WwYfuAu-_4I_pHyHOkeDEASCDXVO5eVUneMe3YdpLJFvDqVq67n2PtubNFbEIok1hzqZyz4oz4_TVO6gxXScQVT9fGrAs_GA4NM86xzMJygDao6dpcbtzEcHN_WwcKbwjpfrRuP0UCdTqsSfdBn1MfhFB2P8PRbVWy-CoBngvXTr59rcph-XyecpSDmSiMgRPUHkYRpnsuTyJ9UyCSyY58H8KEhXX7N6X9VtzUg.59G80nP2D_ZYmZlLuoGM7g'  # `__Secure-next-auth.session-token` cookie from https://chat.openai.com/chat
        #api = ChatGPT(session_token)  # auth with session token
        # api2 = ChatGPT(email='example@domain.com', password='password')  # auth with email and password
        # api3 = ChatGPT(session_token, conversation_id='some-random-uuid')  # specify a conversation id
        # api4 = ChatGPT(session_token, proxy='http://proxy.example.com:8080')  # specify proxy
        #resp = api.send_message(text_to_summarize)
        #st.write(resp['message'])
        response = openai.Completion.create(engine="text-davinci-003", prompt=text_to_summarize, max_tokens=100)
        st.write(response.choices[0].text)       # response received is a json object
