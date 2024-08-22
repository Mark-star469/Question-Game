import customtkinter as ctk 
from PIL import Image
import json

# Загрузка темы
#ctk.set_default_color_theme("green.json")

root = ctk.CTk()
root.geometry("1000x700")
root.title("Кто хочет стать миллионером?")
root.iconbitmap("1.ico")
root.resizable(False, False)

# Загрузка изображения для фона
surat = Image.open("6.png")
surat = ctk.CTkImage(dark_image=surat, size=(1000, 700))
label_surat = ctk.CTkLabel(master=root, image=surat, text="")
label_surat.place(relheight=1, relwidth=1)

# Основной фрейм для вопросов и ответов
frame = ctk.CTkFrame(master=root, width=600, height=500)
frame.pack(side="left", padx=10)

# Загрузка второго изображения
surat2 = Image.open("2.png")
surat2 = ctk.CTkImage(dark_image=surat2, size=(600, 500))
label_surat2 = ctk.CTkLabel(master=frame, image=surat2, text="")
label_surat2.place(relheight=1, relwidth=1)

# Фрейм для наград
frame1 = ctk.CTkFrame(master=root, width=350, height=400)
frame1.pack(side="right", padx="10")

# Шрифты для текста
font = ctk.CTkFont(family="Timer", size=50, weight="bold")
font1 = ctk.CTkFont(family="Timer", size=15)
font12 = ctk.CTkFont(family="Timer", size=17)
font22 = ctk.CTkFont(family="Timer", size=30, weight="bold")

# Список наград
rewards = [10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 500000000, 1000000000]
rewards.reverse()  # Инвертируем список, чтобы показать награды в порядке убывания

# Создание меток для отображения наград и сохранение их в список
reward_labels = []
total_rewards = len(rewards)

for index, reward in enumerate(rewards):
    # Начинаем счет с 10 и движемся вниз
    label_number = total_rewards - index
    reward_label = ctk.CTkLabel(master=frame1, text=f"{label_number}. {reward:,} $", font=font22)
    reward_label.pack(pady=5)
    reward_labels.append(reward_label)

# Загрузка вопросов и ответов из JSON файла
with open('questions.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

questions = data["questions"]
correct_answers = data["correct_answers"]

current_question_index = 0
question_list = list(questions.keys())

# Глобальная переменная для управления таймером
timer_id = None

# Функция для обновления цвета меток наград
def update_reward_colors(current_index):
    total_rewards = len(reward_labels)
    
    # Инвертируем индекс, чтобы начинать с конца
    inverted_index = total_rewards - current_index - 1
    
    for i, label in enumerate(reward_labels):
        if i > inverted_index:
            label.configure(text_color="green")  # Зелёный цвет для отвеченных вопросов
        elif i == inverted_index:
            label.configure(text_color="red")    # Красный цвет для текущего вопроса
        else:
            label.configure(text_color="white")  # Белый цвет для ещё не достигнутых вопросов

# Функция для отображения вопроса и вариантов ответа
def display_question():
    global current_question_index
    
    # Обновление цветов наград
    update_reward_colors(current_question_index)
    
    question_text = question_list[current_question_index]
    l.configure(text=f"SORAG {current_question_index + 1}")
    l2.configure(text=question_text)
    btnA.configure(text=questions[question_text][0], command=lambda: check_answer(0))
    btnB.configure(text=questions[question_text][1], command=lambda: check_answer(1))
    btnC.configure(text=questions[question_text][2], command=lambda: check_answer(2))
    btnD.configure(text=questions[question_text][3], command=lambda: check_answer(3))
    
    # Запуск таймера
    start_timer()

def animate_button(button, color_sequence, interval):
    """Анимация кнопки с последовательностью цветов"""
    if color_sequence:
        # Получаем первый цвет из последовательности и применяем его
        color = color_sequence[0]
        button.configure(fg_color=color)
        
        # Удаляем первый цвет и снова вызываем функцию через интервал
        root.after(interval, animate_button, button, color_sequence[1:], interval)
    else:
        # Возвращаем кнопку к исходному цвету после анимации
        button.configure(fg_color="#3b8ed0")

def check_answer(selected_option):
    global current_question_index, timer_id
    correct_option = correct_answers[current_question_index]
    selected_answer = questions[question_list[current_question_index]][selected_option]
    
    # Отмена таймера при выборе ответа
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None
    
    selected_button = [btnA, btnB, btnC, btnD][selected_option]
    
    if selected_answer == correct_option:
        color_sequence = ["#ccffcc", "#99ff99", "#66ff66", "#33ff33", "#00ff00"]  # Переход от светло-зеленого к темно-зеленому
        animate_button(selected_button, color_sequence, 100)
        
        current_question_index += 1
        if current_question_index < len(questions):
            root.after(500, display_question)  # Задержка перед следующим вопросом
        else:
            show_winning_frame()  # Показ фрейма с надписью о выигрыше
            btnA.configure(state="disabled")
            btnB.configure(state="disabled")
            btnC.configure(state="disabled")
            btnD.configure(state="disabled")
            progress_bar.place_forget()  # Скрытие прогрессбара
    else:
        color_sequence = ["#ffcccb", "#ff9999", "#ff6666", "#ff3333", "#ff0000"]  # Переход от светло-красного к темно-красному
        animate_button(selected_button, color_sequence, 100)
        root.after(500, lambda: game_over("Вы выбрали неправильный ответ!"))

def show_winning_frame():
    """Функция для отображения мигающего фрейма с надписью о выигрыше"""
    winning_frame = ctk.CTkFrame(master=root, width=800, height=400)
    winning_frame.place(relx=0.5, rely=0.5, anchor="center")

    font_winning = ctk.CTkFont(family="Timer", size=50, weight="bold")
    winning_label = ctk.CTkLabel(master=winning_frame, text="ВЫ ВЫИГРАЛИ 1 МЛРД!!!", font=font_winning)
    winning_label.place(relx=0.5, rely=0.5, anchor="center")

    def blink():
        current_color = winning_frame.cget("fg_color")
        new_color = "#ffcc00" if current_color == "#ff0000" else "#ff0000"
        winning_frame.configure(fg_color=new_color)
        root.after(500, blink)

    blink()

def show_losing_frame():
    """Функция для отображения мигающего фрейма с надписью о проигрыше"""
    losing_frame = ctk.CTkFrame(master=root, width=800, height=400)
    losing_frame.place(relx=0.5, rely=0.5, anchor="center")

    font_losing = ctk.CTkFont(family="Timer", size=50, weight="bold")
    losing_label = ctk.CTkLabel(master=losing_frame, text="ВЫ ПРОИГРАЛИ 1 МЛРД!!!", font=font_losing)
    losing_label.place(relx=0.5, rely=0.5, anchor="center")

    def blink():
        current_color = losing_frame.cget("fg_color")
        new_color = "#ffcc00" if current_color == "#ff0000" else "#ff0000"
        losing_frame.configure(fg_color=new_color)
        root.after(500, blink)

    blink()

# Функция для обработки окончания игры при истечении времени
def game_over_timeout():
    game_over("Время вышло! Вы не успели ответить.")

# Функция для отображения сообщения об окончании игры
def game_over(message):
    global timer_id
    # Отмена таймера если он еще активен
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

    # Отключение кнопок
    btnA.configure(state="disabled")
    btnB.configure(state="disabled")
    btnC.configure(state="disabled")
    btnD.configure(state="disabled")
    
    # Удаление фреймов
    frame.pack_forget()
    frame1.pack_forget()
    
    font_game_over = ctk.CTkFont(family="Timer", size=40, weight="bold")
    # Отображение сообщения о проигрыше
    game_over_label = ctk.CTkLabel(master=root, text=message, font=font_game_over)
    game_over_label.place(relx=0.5, rely=0.5, anchor="center")
    
    # Показываем мигающий фрейм
    show_losing_frame()

# Функции для управления таймером и прогрессбаром
def start_timer():
    global timer_id
    progress_bar.set(1.0)  # Установка прогрессбара на полный
    timer_id = root.after(100, update_progress)

def update_progress():
    global timer_id
    current_value = progress_bar.get()
    decrement = 0.005  # Поскольку 0.005 * 200 = 1.0, это обеспечит 20 секундный таймер
    new_value = current_value - decrement
    if new_value <= 0:
        progress_bar.set(0)
        game_over_timeout()
    else:
        progress_bar.set(new_value)
        timer_id = root.after(100, update_progress)  # Обновление каждые 100 миллисекунд

# Метки и кнопки
l = ctk.CTkLabel(master=frame, text="ВОПРОС 1", font=font)
l.place(relx=0.3, rely=0.1)
l2 = ctk.CTkLabel(master=frame, font=font12, text="")
l2.place(relx=0.1, rely=0.4)
btnA = ctk.CTkButton(master=frame, width=250, height=50, font=font1, text="")
btnA.place(relx=0.05, rely=0.6)
btnB = ctk.CTkButton(master=frame, width=250, height=50, font=font1, text="")
btnB.place(relx=0.05, rely=0.75)
btnC = ctk.CTkButton(master=frame, width=250, height=50, font=font1, text="")
btnC.place(relx=0.5, rely=0.6)
btnD = ctk.CTkButton(master=frame, width=250, height=50, font=font1, text="")
btnD.place(relx=0.5, rely=0.75)

# Прогрессбар
progress_bar = ctk.CTkProgressBar(master=frame, orientation='horizontal', mode='determinate', width=500, height=20)
progress_bar.place(relx=0.5, rely=0.9, anchor='center')
progress_bar.set(1.0)  # Инициализация на полный

# Отображение первого вопроса
display_question()

root.mainloop()
