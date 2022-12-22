from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
# creating an empty dictionary to use in both functions below
current_card = {}
# creating an empty dictionary to use for the to_dict below
to_learn = {}

# trying to open words_to_learn csv, if it doesn't exist then read from the original data of french_words
try:
    # Using Pandas to read CSV
    data = pandas.read_csv("data/words_to_learn.csv")
# to_learn will create a dictionary for original data if words_to_learn csv doesn't exist
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
# if we find words_to_learn csv then we removed words we already know so do this below with the rest of the list
else:
    # creating a dictionary from the csv file...orient="records" creates [{'French': 'partie', 'English': 'part'} which
    # gives the key/value pairs of each french and english word
    to_learn = data.to_dict(orient="records")


def next_card():
    # calling global to use current_card, and flip_timer in both functions
    global current_card, flip_timer
    # saying if user clicks on a new button then current flip_timer will be invalidated...so 3 sec timer won't start
    # while user is just quickly clicking on the buttons
    window.after_cancel(flip_timer)
    # getting random choice from the value of the dictionary created from to_learn
    current_card = random.choice(to_learn)
    # taking value of current_card and making sure only the French value is shown
    random_french = current_card["French"]
    # calling the canvas to itemconfig and call original title(from canvas below) and changing the text to French when
    # button is pressed
    canvas.itemconfig(title, text="French", fill="black")
    # again getting the itemconfig to get original answer variable and adding the random french word as text when
    # button is pushed
    canvas.itemconfig(answer, text=random_french, fill="black")
    # changing the card back to the french side display after the 3 secs and the button is clicked for the next word
    canvas.itemconfig(canvas_front, image=card_front)
    # new flip_timer variable, so it waits again for 3 secs...basically if user is just scrolling through words when
    # user stops on card the 3 sec timer will continue
    flip_timer = window.after(3000, flip_card)


def flip_card():
    global current_card
    # configuring the other side of card with new image, title, and answer
    english_card = current_card["English"]
    canvas.itemconfig(canvas_front, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(answer, text=english_card, fill="white")


# defining a function for when the right_button is clicked, it will remove the current card from the to_learn csv

def is_known():
    to_learn.remove(current_card)
    # creating a new dataframe from the to_learn file and getting a new csv for the words that need to be learned
    words_to_learn = pandas.DataFrame(to_learn)
    # index false means the count won't show, just the records
    words_to_learn.to_csv("data/words_to_learn.csv", index=False)
    # then going to the next card
    next_card()


# UI Setup
window = Tk()
window.title("Flash Card Project")
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)
# window will flip to english card after 3 seconds
flip_timer = window.after(3000, flip_card)

# Canvas Setup
# changing the background color to the same background color as window and taking out the white borderline with
# highlightthickness
canvas = Canvas(width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
# the numbers 400 and 263 is half of the canvas width and height to get the image to fit in the canvas
canvas_front = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)
# creating text inside the canvas instead of creating label
title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
answer = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

# Buttons
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, width=100, highlightthickness=0, command=is_known)
right_button.grid(column=0, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, width=100, highlightthickness=0, command=next_card)
wrong_button.grid(column=1, row=1)

# calling function down here so when the program runs there will be a French word by default
next_card()

window.mainloop()
