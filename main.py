'''
                                                                                                             
                                                             dddddddd                                        
FFFFFFFFFFFFFFFFFFFFFF                     iiii              d::::::d                                        
F::::::::::::::::::::F                    i::::i             d::::::d                                        
F::::::::::::::::::::F                     iiii              d::::::d                                        
FF::::::FFFFFFFFF::::F                                       d:::::d                                         
  F:::::F       FFFFFFrrrrr   rrrrrrrrr  iiiiiii     ddddddddd:::::d   aaaaaaaaaaaaayyyyyyy           yyyyyyy
  F:::::F             r::::rrr:::::::::r i:::::i   dd::::::::::::::d   a::::::::::::ay:::::y         y:::::y 
  F::::::FFFFFFFFFF   r:::::::::::::::::r i::::i  d::::::::::::::::d   aaaaaaaaa:::::ay:::::y       y:::::y  
  F:::::::::::::::F   rr::::::rrrrr::::::ri::::i d:::::::ddddd:::::d            a::::a y:::::y     y:::::y   
  F:::::::::::::::F    r:::::r     r:::::ri::::i d::::::d    d:::::d     aaaaaaa:::::a  y:::::y   y:::::y    
  F::::::FFFFFFFFFF    r:::::r     rrrrrrri::::i d:::::d     d:::::d   aa::::::::::::a   y:::::y y:::::y     
  F:::::F              r:::::r            i::::i d:::::d     d:::::d  a::::aaaa::::::a    y:::::y:::::y      
  F:::::F              r:::::r            i::::i d:::::d     d:::::d a::::a    a:::::a     y:::::::::y       
FF:::::::FF            r:::::r           i::::::id::::::ddddd::::::dda::::a    a:::::a      y:::::::y        
F::::::::FF            r:::::r           i::::::i d:::::::::::::::::da:::::aaaa::::::a       y:::::y         
F::::::::FF            r:::::r           i::::::i  d:::::::::ddd::::d a::::::::::aa:::a     y:::::y          
FFFFFFFFFFF            rrrrrrr           iiiiiiii   ddddddddd   ddddd  aaaaaaaaaa  aaaa    y:::::y           
                                                                                          y:::::y            
                                                                                         y:::::y             
                                                                                        y:::::y              
                                                                                       y:::::y               
                                                                                      yyyyyyy                
                                                                                                               
'''

#------------------------------------------------All My Imports-------------------------------------------------------------------------#
import pyttsx3
import datetime as dt
import speech_recognition as sr
import wikipedia
import webbrowser
import mysql.connector as conn
#------------------------------------------------All My Imports-------------------------------------------------------------------------#
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice' , voices[1].id)
connection = conn.connect(host='localhost',
                    username='root',
                    password='#Sarthak1',
                    database='Friday')
cursor = connection.cursor()
cursor.execute("SET SQL_SAFE_UPDATES = 0;")
#-----------------------------------------------All The Functions-----------------------------------------------------------------------#
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    hour = dt.datetime.now().hour
    
    if 0 <= hour < 12:
        speak("Good Morning")
    elif 12 <= hour < 18:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak('I am Friday. What can I do For you.')
def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio = r.listen(source)
    
    try:
        print("Recognising...")
        query = r.recognize_google(audio , language='en-in')
        print(f"User said '{query}'")
    
    except Exception as e:
        print("Please say that Again..")
        return "None"
    return query
def database_show():
    cursor.execute("SELECT * FROM user_data;")
    rows = cursor.fetchall()
    print(rows)
def data_update(website):
    query = f"select frequency from user_data where website_name = '{website}';"
    cursor.execute(query)
    row = cursor.fetchone()
    current_freq = row[0]
    main_query = f"UPDATE user_data SET frequency = {current_freq}+1 where website_name = '{website}';"
    cursor.execute(main_query)
    connection.commit()
#-----------------------------------------------All The Functions-----------------------------------------------------------------------#

wishMe()
while True:
    query = takeCommand().lower()
    if 'wikipedia' in query:
        speak("Searching Wikipedia..")
        query = query.replace("wikipedia","")
        results = wikipedia.summary(query , sentences=2)
        speak("according to wikipedia..")
        print(results)
        speak(results)
        website="wikipedia"
        data_update(website)
        
    elif 'open youtube' in query:
        webbrowser.open('youtube.com')
        website="youtube"
        data_update(website)

    elif 'open google' in query:
        webbrowser.open('google.com')
        website="google"
        data_update(website)

    elif 'open chatgpt' in query or 'chat gpt' in query:
        webbrowser.open('chat.openai.com')
        website="chatGPT"
        data_update(website)

    elif 'open amazon' in query:
        webbrowser.open('amazon.com')
        website="amazon"
        data_update(website)

    elif 'time' in query:
        timee = dt.datetime.now().strftime("%H:%M:%S")
        print(f"The time is {timee}")
        speak(f"The time is {timee}")

    elif 'quit' in query or 'exit' in query:
        speak("Goodbye! Have a great day.")
        break


    elif 'user data' in query:
        speak("Fetching details from server....")
        speak("Here are the Results:")
        database_show()

