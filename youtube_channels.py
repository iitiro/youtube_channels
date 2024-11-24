import os
import subprocess
import pandas as pd
import json

# Шлях до файлу з назвами каналів YouTube
channels_file = 'youtube.txt'

# Шлях до папки для збереження JSON файлів
directory = "./!youtube_downloader/"
os.makedirs(directory, exist_ok=True)

# Зчитування каналів з файлу youtube.txt
with open(channels_file, 'r') as file:
    channels = [line.strip() for line in file if line.strip()]

# Прохід по кожному каналу
for channel in channels:
    # Визначення імені файлу для збереження даних каналу
    json_filename = f"{channel}.json"
    json_filepath = os.path.join(directory, json_filename)
    
    # Команда для викачування даних с каналу YouTube із використанням yt-dlp
    command = ['yt-dlp', '-j', f"https://www.youtube.com/{channel}"]
    
    try:
        # Запуск команди і запис результатів у файл
        with open(json_filepath, 'w') as output_file:
            subprocess.run(command, stdout=output_file, check=True)
        print(f"Дані з каналу {channel} збережені у файл {json_filepath}")
    except subprocess.CalledProcessError as e:
        print(f"Помилка при завантаженні даних з каналу {channel}: {e}")

# Після завантаження даних виконується конвертація JSON у Excel

# Прохід по всім JSON файлам в директорії
for filename in os.listdir(directory):
    if filename.endswith(".json"):  # Перевірка, що файл має розширення .json
        filepath = os.path.join(directory, filename)

        # Читання вмісту JSON файлу
        with open(filepath, 'r') as file:
            content = file.read()

        # Спроба розділити вміст на окремі JSON об'єкти, якщо файл містить кілька JSON
        json_objects = content.strip().split('\n')

        data_frames = []
        for json_str in json_objects:
            try:
                # Завантаження JSON рядка як словника
                json_data = json.loads(json_str)
                # Перетворення словника у DataFrame
                df = pd.DataFrame([json_data])
                data_frames.append(df)
            except json.JSONDecodeError as e:
                print(f"Помилка парсингу JSON з файлу {filename}: {e}")

        # Об'єднання всіх DataFrame в один
        if data_frames:
            combined_df = pd.concat(data_frames, ignore_index=True)
            # Збереження DataFrame у Excel файл з тим самим іменем, що й вихідний JSON
            excel_path = os.path.join(directory, f"{os.path.splitext(filename)[0]}.xlsx")
            combined_df.to_excel(excel_path, index=False)
            print(f"Збережено {excel_path}")
        else:
            print(f"Немає даних для збереження з файлу {filename}")

# Повідомлення про завершення обробки
print("Обробка завершена.")