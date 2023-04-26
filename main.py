import openai
from gtts import gTTS
from colored import fg, attr
import datetime
import re
import os
import playsound



key = "YOUR API KEY"    

openai.api_key = key

def remove_emoji(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)



def speak(text):
    tts = gTTS(text= remove_emoji(text), lang='ja') 

    filename = "ENFI_voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


color = fg('green')
reset = attr('reset')




greetings = {
    "morning": "Good Morning",
    "afternoon": "Good Afternoon",
    "evening": "Good Evening"
}

def greet():
    # Get current hour
    hour = int(datetime.datetime.now().hour)
    # Determine appropriate greeting based on time of day
    if hour >= 0 and hour < 12:
        greeting = greetings["morning"]
    elif hour >= 12 and hour < 18:
        greeting = greetings["afternoon"]
    else:
        greeting = greetings["evening"]
    # Greet user
    message = greeting + " , how may I help you 😃"
    print(message)
    message = message.replace("😃", "")  
    speak(message)

def chat(message_log):
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=message_log,   
                max_tokens=3000,        
                stop=None,           
                temperature=0.9, 
                top_p=1,
        )

        return response.choices[0].message.content



def main():
    personality = f"You are a helpful assistant  , Your name is AQUA and you answer questions in sarcasm and also reply with emojis "
    time = datetime.datetime.now().strftime("%I:%M %p")
    message_log = [
        {"role": "system", "content": personality },
        {"role": "system", "content": f"Current/now time is {time}" }
    ]

    while True:
        ask = input("Ask any thing...")
    
        message_log.append({"role": "user", "content": ask})

        response = chat(message_log)
        message_log.append({"role": "system", "content": response})

        print(f"{color}ENFI : {response} {reset}\n")
        speak(response)

        if ask.lower() == "exit":
            break
        

if __name__ == "__main__":
    greet()
    main()

