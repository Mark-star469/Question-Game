import customtkinter as ctk
from PIL import Image
import json
import pygame

# Initialize the pygame mixer
pygame.mixer.init()

# Load music and sound effects
pygame.mixer.music.load("fon.mp3")  # Replace with your music file path
correct_sound = pygame.mixer.Sound("dogry.mp3")  # Replace with your correct sound file path
incorrect_sound = pygame.mixer.Sound("yalnys.mp3")  # Replace with your incorrect sound file path
winner_sound = pygame.mixer.Sound("winner.mp3")  # Replace with your winner music file path

# Play background music
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Function to load questions from JSON
def load_questions_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['questions']

# Load questions from file
questions = load_questions_from_json('questions.json')
current_question_index = 0
progress_value = 0  # Starting value of progress
progress_increment = 100 / len(questions)  # Increment per correct answer
countdown_active = False

def display_question(index):
    global countdown_active
    countdown_active = True
    question_data = questions[index]
    l1.configure(text=question_data['question'], justify="center")
    btn1.configure(text=question_data['options'][0], command=lambda: check_answer(question_data['options'][0], question_data['answer']))
    btn2.configure(text=question_data['options'][1], command=lambda: check_answer(question_data['options'][1], question_data['answer']))
    btn3.configure(text=question_data['options'][2], command=lambda: check_answer(question_data['options'][2], question_data['answer']))
    btn4.configure(text=question_data['options'][3], command=lambda: check_answer(question_data['options'][3], question_data['answer']))

    # Start the countdown timer
    countdown_progress_bar.set(1.0)  # Reset the progress bar
    root.after(0, countdown)

def countdown():
    global countdown_active
    current_value = countdown_progress_bar.get()
    decrement_value = 1 / (20 * 50)  # 20 seconds, 50 updates per second

    if current_value > 0 and countdown_active:
        countdown_progress_bar.set(current_value - decrement_value)  # Decrease progress bar
        root.after(20, countdown)  # Update every 20ms (50 updates per second)
    elif current_value <= 0:
        countdown_active = False
        incorrect_sound.play()
        pygame.mixer.music.fadeout(3000)  # Fade out music over 3 seconds
        display_game_over()

def check_answer(selected_option, correct_answer):
    global countdown_active
    countdown_active = False
    if selected_option == correct_answer:
        correct_sound.play()
        update_progress_bar()
    else:
        incorrect_sound.play()
        pygame.mixer.music.fadeout(3000)  # Fade out music over 3 seconds
        display_game_over()

def update_progress_bar():
    global progress_value, current_question_index

    # Increase progress value
    progress_value += progress_increment

    font33 = ctk.CTkFont(family="Timer", size=30, weight="bold")

    # Create and display frame with ProgressBar
    progress_frame = ctk.CTkFrame(master=root, width=800, height=500)
    progress_frame.place(relx=0.1, rely=0.15)

    progress_label = ctk.CTkLabel(master=progress_frame, text=f"SIZIŇ BALYŇYZ: {progress_value:.2f}% MAX = 100%", font=font33)
    progress_label.place(relx=0.17, rely=0.3)

    progress_bar = ctk.CTkProgressBar(master=progress_frame, width=600, height=40, progress_color="orange")
    progress_bar.place(relx=0.1, rely=0.6)
    progress_bar.set((progress_value - progress_increment) / 100)

    # Wait 100 ms before starting animation
    root.after(100, lambda: animate_progress_bar(progress_bar, progress_frame, progress_value / 100))

def animate_progress_bar(progress_bar, progress_frame, end_value):
    start_value = progress_bar.get()
    step = (end_value - start_value) / 100  # 100 animation steps

    def animate():
        nonlocal start_value
        if start_value < end_value:
            start_value += step
            progress_bar.set(start_value)
            root.after(10, animate)  # Update frequency 10ms
        else:
            root.after(500, progress_frame.destroy)  # Remove frame after animation
            next_question()

    animate()

def next_question():
    global current_question_index
    current_question_index += 1
    if current_question_index < len(questions):
        display_question(current_question_index)
    else:
        pygame.mixer.music.fadeout(3000)  # Fade out background music
        display_winner()

def play_winner_sound():
    winner_sound.play()

def display_game_over():
    game_over_frame = ctk.CTkFrame(master=root, width=800, height=500)
    game_over_frame.place(relx=0.1, rely=0.15)

    surat = Image.open("R.png")
    surat = ctk.CTkImage(dark_image=surat, size=(500, 400))
    label_surat = ctk.CTkLabel(master=game_over_frame, image=surat, text="")
    label_surat.place(relheight=1, relwidth=1)

    game_over_label = ctk.CTkLabel(master=game_over_frame, text="SIZ UTULDUNYZ!", font=font)
    game_over_label.place(relx=0.3, rely=0.9)

def display_winner():
    winner_frame = ctk.CTkFrame(master=root, width=800, height=500)
    winner_frame.place(relx=0.1, rely=0.15)

    surat = Image.open("winner_emoji.jpg")
    surat = ctk.CTkImage(dark_image=surat, size=(300, 300))
    label_surat = ctk.CTkLabel(master=winner_frame, image=surat, text="")
    label_surat.place(relheight=1, relwidth=1)

    winner_label = ctk.CTkLabel(master=winner_frame, text="SIZ ZEHINLI OKUWCY!", font=font)
    winner_label.place(relx=0.27, rely=0.9)

    # Play winner sound immediately after displaying the winner frame
    play_winner_sound()

ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.geometry("1000x700")
root.title("Dana bilim")
root.iconbitmap("7.ico")
root.resizable(False, False)

surat = Image.open("bg.jpg")
surat = ctk.CTkImage(dark_image=surat, size=(1000, 700))
label_surat = ctk.CTkLabel(master=root, image=surat, text="")
label_surat.place(relheight=1, relwidth=1)

frame = ctk.CTkFrame(master=root, width=800, height=500)
frame.place(relx=0.1, rely=0.15)

font = ctk.CTkFont(family="Timer", size=40, weight="bold")
font2 = ctk.CTkFont(family="Timer", size=23, weight="bold")

l = ctk.CTkLabel(master=frame, text="SORAGLAR", font=font)
l.place(relx=0.35, rely=0.1)

l1 = ctk.CTkLabel(master=frame, text="", font=font2)
l1.place(relx=0.5, rely=0.4, anchor="center")  # Centered alignment

btn1 = ctk.CTkButton(master=frame, height=60, width=200)
btn1.place(relx=0.13, rely=0.6)
btn2 = ctk.CTkButton(master=frame, height=60, width=200)
btn2.place(relx=0.13, rely=0.8)
btn3 = ctk.CTkButton(master=frame, height=60, width=200)
btn3.place(relx=0.6, rely=0.6)
btn4 = ctk.CTkButton(master=frame, height=60, width=200)
btn4.place(relx=0.6, rely=0.8)

# Add a countdown progress bar to the main frame
countdown_progress_bar = ctk.CTkProgressBar(master=frame, width=600, fg_color="red", progress_color="green")
countdown_progress_bar.place(relx=0.1, rely=0.2)

# Display the first question
display_question(current_question_index)

root.mainloop()
