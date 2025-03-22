from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Инициализация браузера
browser = webdriver.Chrome()
browser.get("https://ru.wikipedia.org/")

# Функция для поиска статьи
def search_wikipedia(query):
    search_box = browser.find_element(By.ID, "searchInput")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Ожидание загрузки страницы

# Функция для отображения параграфов статьи
def show_paragraphs():
    paragraphs = browser.find_elements(By.CSS_SELECTOR, "div.mw-parser-output p")
    for i, paragraph in enumerate(paragraphs):
        print(f"\nПараграф {i + 1}:\n{paragraph.text}")
        if (i + 1) % 3 == 0:  # Показываем по 3 параграфа за раз
            choice = input("\nНажмите Enter для продолжения или 'q' для выхода: ")
            if choice.lower() == 'q':
                break

# Функция для отображения связанных страниц
def show_related_links():
    # Ожидание загрузки связанных ссылок
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.mw-parser-output p a[href*='/wiki/']"))
    )
    links = browser.find_elements(By.CSS_SELECTOR, "div.mw-parser-output p a[href*='/wiki/']")
    print("\nСвязанные страницы:")
    for i, link in enumerate(links[:5]):  # Показываем первые 5 ссылок
        print(f"{i + 1}: {link.text}")
    choice = input("\nВведите номер ссылки для перехода или 'q' для выхода: ")
    if choice.isdigit() and 1 <= int(choice) <= len(links[:5]):
        # Используем JavaScript для клика, если обычный клик не работает
        browser.execute_script("arguments[0].click();", links[int(choice) - 1])
        time.sleep(2)  # Ожидание загрузки страницы
        return True
    return False

# Основной цикл программы
def main():
    while True:
        query = input("\nВведите запрос для поиска на Википедии (или 'q' для выхода): ")
        if query.lower() == 'q':
            break

        search_wikipedia(query)

        while True:
            print("\nВыберите действие:")
            print("1: Листать параграфы текущей статьи")
            print("2: Перейти на одну из связанных страниц")
            print("3: Вернуться к поиску")
            choice = input("Введите номер действия: ")

            if choice == '1':
                show_paragraphs()
            elif choice == '2':
                if not show_related_links():
                    break
            elif choice == '3':
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

    # Закрытие браузера
    browser.quit()

if __name__ == "__main__":
    main()
