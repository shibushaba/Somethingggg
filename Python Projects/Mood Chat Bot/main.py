print("Mood Bot: Iam Your Mood Switching Bot")
print("Mood Bot: I can switch to three moods: Happy,Sad,Angry")
print("Mood Bot: To exit type 'exit'")


normal_mood = "confusion"

response = {
    "happy":{
        "start": "Iam happy",
        "hi" : "whats up maahnn lets chill outt!!",
    },
    "sad" :{
        "start": "Iam sad",
        "hi" : "iam sad maahn i donna want to talk",
    },
    "angry" :{
        "start": "Iam angry",
        "hi" : "whats your prblm dude lets fght",
    },
    "confusion" :{
        "start": "Iam confused",
    }
}



while True:
    mood = input("Mood Bot : Enter your Mood : (happy/sad/angry) or 'exit' to quit:").lower().strip()
    if mood == "exit":
        print("Mood Bot : seeeyaaa laterr Idiot")
        break
    if mood in response:
        print("Mood Bot : Iam switching to", mood)
        print("Mood Bot :", response[mood]["start"])
        break
    else:
        print("Mood Bot : What kind of mood is zhaaattt Brruhh????")
        print("Mood  Bot :", response["confusion"]["start"])
        
while True: 
     you = input("You :").lower().strip()
     if you == "exit":
        print("Mood Bot : seeeyaaa laterr Idiot")
        break
     if you in response [mood]:
        print("Mood Bot :", response[mood][you])
     else:
         print("Mood Bot :", response["confusion"]["start"])