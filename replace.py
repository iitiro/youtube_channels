import os
import pandas as pd

# Функція для заміни @@ на @ у всіх значеннях DataFrame
def replace_double_at_in_df(df):
    # Здійснюємо заміну `@@` на `@` для всіх значень у DataFrame
    df = df.applymap(lambda x: x.replace('@@', '@') if isinstance(x, str) else x)
    return df

# Функція для обробки всіх .xlsx файлів у заданій папці
def process_xlsx_files_in_folder(folder_path):
    # Перевіряємо, чи існує папка
    if not os.path.exists(folder_path):
        print(f"Папка {folder_path} не існує.")
        return
    
    # Проходимо по всім файлам у папці
    for filename in os.listdir(folder_path):
        # Обробляємо тільки файли з розширенням .xlsx
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            print(f"Обробка файлу: {file_path}")
            
            try:
                # Зчитуємо дані з Excel файлу у DataFrame
                df = pd.read_excel(file_path)
                
                # Здійснюємо заміну @@ на @
                df = replace_double_at_in_df(df)
                
                # Зберігаємо змінений DataFrame у той самий файл
                df.to_excel(file_path, index=False)
                print(f"Заміна виконана і файл збережено: {file_path}")
            except Exception as e:
                print(f"Помилка при обробці файлу {file_path}: {e}")

# Вказуємо шлях до папки з .xlsx файлами
folder_path = "!search_youtube"

# Запускаємо обробку
process_xlsx_files_in_folder(folder_path)