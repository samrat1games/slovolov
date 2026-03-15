import random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

def first():
    print('''
Программа обучения английскому языку!
Программа пишет вам слово, а вы его произносите на английском языке!
===========================================
    Правила:
    1. Выбери уровень сложности (1, 2, 3, 4).
    2. Я пишу слово на русском — ты произносишь на английском.
    3. У тебя есть 3 жизни.
    4. За каждое угаданное слово +10 баллов.
==========================================
''')

words_easy = {
    "привет": "hello",
    "да": "yes",
    "нет": "no",
    "хорошо": "ok",
    "день": "day",
    "ночь": "night",
    "мама": "mother",
    "кот": "cat",
    "друг": "friend",
    "яблоко": "apple"
}

words_normal = {
    "город": "city",
    "жизнь": "life",
    "думать": "think",
    "красивый": "beautiful",
    "быстро": "fast",
    "книга": "book",
    "завтрак": "breakfast",
    "помогать": "help",
    "машина": "car",
    "семья": "family"
}

words_hard = {
    "возможность": "opportunity",
    "общество": "society",
    "решение": "decision",
    "влияние": "influence",
    "состояние": "condition",
    "развитие": "development",
    "опыт": "experience",
    "предложение": "offer",
    "цель": "goal",
    "свобода": "freedom"
}

words_extreme = {
    "сознание": "consciousness",
    "пренебрежение": "disregard",
    "ответственность": "responsibility",
    "воображение": "imagination",
    "законодательство": "legislation",
    "предрассудок": "prejudice",
    "вдохновение": "inspiration",
    "противоречие": "contradiction",
    "существование": "existence",
    "независимость": "independence"
}

def start_game():
    level = input('''
        Выбери режим! 
        1 - Easy
        2 - Normal
        3 - Hard
        4 - Extreme
        Введи число: ''')
    
    if level == "1":
        vibrat_slovo = words_easy
    elif level == "2":
        vibrat_slovo = words_normal
    elif level == "3":
        vibrat_slovo = words_hard
    elif level == "4":
        vibrat_slovo = words_extreme
    else:
        print("Неверный ввод, введите заново!")
        return start_game()

    game_list = list(vibrat_slovo.items())
    random.shuffle(game_list)
    
    score = 0
    lives = 3
    recognizer = sr.Recognizer()
    translator = Translator()
    
    # Настройка микрофона один раз перед началом
    with sr.Microphone() as source:
        print("\nНастройка микрофона под уровень шума... Помолчите секунду.")
        recognizer.adjust_for_ambient_noise(source, duration=1)

    for ru_word, en_word in game_list:
        if lives <= 0:
            print(f"\n==========================================")
            print(f"ИГРА ОКОНЧЕНА! ВАШ ИТОГОВЫЙ СЧЕТ: {score}")
            print(f"==========================================")
            break
            
        print(f"\nСлово: {ru_word.upper()}")
        print(f"Баллы: {score} | Жизни: {lives}")
        
        with sr.Microphone() as source:
            print("Слушаю вас...")
            try:
                # Используем listen вместо фиксированной записи для точности
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                print("Распознаю...")
                
                text = recognizer.recognize_google(audio, language="en-US").lower()
                print(f"Вы сказали: {text}")

                # 1. Сначала проверяем точное совпадение на английском
                if text == en_word.lower():
                    print("ОТЛИЧНО! Правильно!")
                    score += 10
                else:
                    # 2. Запасная проверка через перевод
                    translated = translator.translate(text, dest='ru')
                    word_ru = translated.text.lower()
                    
                    if word_ru == ru_word.lower():
                        print("ПРАВИЛЬНО (распознано через смысл)!")
                        score += 10
                    else:
                        print(f"ОШИБКА. Вы сказали '{text}', а нужно было '{en_word}'")
                        lives -= 1
                    
            except sr.WaitTimeoutError:
                print("ВРЕМЯ ВЫШЛО. Вы ничего не сказали.")
                lives -= 1
            except sr.UnknownValueError:
                print("НЕ УДАЛОСЬ ПОНЯТЬ. Попробуйте произнести четче.")
                lives -= 1
            except sr.RequestError as e:
                print(f"ОШИБКА СЕРВИСА: {e}")
                break

if __name__ == "__main__":
    first()
    start_game()