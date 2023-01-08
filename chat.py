from tensorflow import keras
from tkinter import *
from tkinter import filedialog
import re
import cv2 as cv
import numpy as np
import requests

# Code for UI from GeeksForGeeks https://www.geeksforgeeks.org/gui-chat-application-using-tkinter-in-python/

json_model = open("model.json", "r")
model = keras.models.model_from_json(json_model.read())
json_model.close()
model.load_weights("model.h5")
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

window = Tk()
window.title("Chatbot")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

INTRODUCTION = "Bot -> This is an AI model for identifying dogs or cats.\n"
INTRODUCTION_2 = "Bot -> Start by typing 'Help'."
# Send function
def send():
    send = "You -> " + e.get()
    txt.insert(END, "\n" + send)

    response()

    e.delete(0, END)

def response():
    user = e.get().lower()

    if re.search("hello", user):
        txt.insert(END, "\n" + "Bot -> Hello!")

    elif re.search("hi+", user):
        txt.insert(END, "\n" + "Bot -> Hi!")

    elif re.search("identify", user):
        try:
            image = open_file()
            prediction = model.predict(image)
            prediction = np.argmax(prediction)

            prediction_text = "dog" if prediction == 0 else "cat"
            txt.insert(END, "\n" + "Bot -> I think that " + prediction_text + " is depicted here.")
            txt.insert(END, "\n" + "Bot -> Here is a random fact about that animal.")

            fact = dog_api_fact() if prediction_text == "dog" else cat_api_fact()
            txt.insert(END, "\n" + "Bot -> " + fact)

        except Exception:
            txt.insert(END, "\n" + "Bot -> Something seemed to go wrong. Try again.")

    elif re.search("dog fact", user):
        txt.insert(END, "\n" + "Bot -> " + dog_api_fact())

    elif re.search("cat fact", user):
        txt.insert(END, "\n" + "Bot -> " + cat_api_fact())

    elif re.search("help", user):
        txt.insert(END, "\n" + "Bot -> I can do following things:")
        txt.insert(END, "\n" + "Bot -> identify - identify whether there is a cat or a dog in the photo.")
        txt.insert(END, "\n" + "Bot -> dog fact - random dog fact")
        txt.insert(END, "\n" + "Bot -> cat fact - random cat fact")
    else:
        txt.insert(END, "\n" + "Bot -> Sorry! I didn't understand that")


def open_file():
    path = filedialog.askopenfilename(title="Choose a picture", filetypes=(("image  files", "*.jpg"), ("all files","*.*")))
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    resized = cv.resize(img, (50, 50))
    arr = np.array(resized)
    arr = arr.reshape((50, 50, 1))
    arr = np.expand_dims(arr, axis=0)
    return arr

def dog_api_fact():
    url = "http://dog-api.kinduff.com/api/facts"
    response = requests.get(url=url)
    if response.status_code != 200:
        return None
    return response.json()["facts"][0]

def cat_api_fact():
    url = "https://cat-fact.herokuapp.com/facts/random"
    response = requests.get(url=url)
    if response.status_code != 200:
        return None
    return response.json()["text"]

def affirmation_check(text):
    affirmation_buzzwords = ("yes", "yep", "sure", "affirmative", "gladly", "of course", "indeed", "+", "jah")
    for word in affirmation_buzzwords:
        if re.search(word, text):
            return True
    return False

def refutation_check(text):
    affirmation_buzzwords = ("no", "nah", "not really", "nope", "hell no", "never", "ei", "-", "don't think so", "do not think so")
    for word in affirmation_buzzwords:
        if re.search(word, text):
            return True
    return False


txt = Text(window, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
txt.grid(row=1, column=0, columnspan=2)
txt.insert(END, INTRODUCTION)
txt.insert(END, INTRODUCTION_2)
scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)


e = Entry(window, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
e.grid(row=2, column=0)

send = Button(window, text="Send", font=FONT_BOLD, bg=BG_GRAY,
              command=send).grid(row=2, column=1)

window.mainloop()