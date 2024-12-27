import math
from concurrent.futures import ThreadPoolExecutor
from functools import reduce

class Candy:
    def __init__(self, name, weight, sugar_content):
        self.name = name
        self.weight = weight
        self.sugar_content = sugar_content

    def __str__(self):
        return f"{self.name} (Вес: {self.weight} г, Содержание сахара: {self.sugar_content} г)"

class Chocolate(Candy):
    def __init__(self, name, weight, sugar_content, cocoa_content):
        super().__init__(name, weight, sugar_content)
        self.cocoa_content = cocoa_content

    def __str__(self):
        return f"{self.name} (Вес: {self.weight} г, Содержание сахара: {self.sugar_content} г, Содержание какао: {self.cocoa_content}%)"

class Cookie(Candy):
    def __init__(self, name, weight, sugar_content, flavor):
        super().__init__(name, weight, sugar_content)
        self.flavor = flavor

    def __str__(self):
        return f"{self.name} (Вес: {self.weight} г, Содержание сахара: {self.sugar_content} г, Вкус: {self.flavor})"

# Класс GiftBuilder для создания подарка
class GiftBuilder:
    def __init__(self):
        self.gift = []

    def add_candy(self, candy):
        self.gift.append(candy)

    def get_total_weight(self):
        return sum(candy.weight for candy in self.gift)

    def sort_by_sugar_content(self):
        self.gift.sort(key=lambda candy: candy.sugar_content)

    def find_candy_by_sugar_content(self, min_sugar, max_sugar):
        return [candy for candy in self.gift if min_sugar <= candy.sugar_content <= max_sugar]

# Основное выполнение программы
def main():
    gift_builder = GiftBuilder()

    # Создание объектов конфет
    chocolate_a = Chocolate("Шоколад А", 100, 50, 70)
    cookie_b = Cookie("Печенье Б", 50, 20, "ваниль")
    candy_c = Candy("Конфета В", 30, 25)

    # Добавление конфет в подарок
    gift_builder.add_candy(chocolate_a)
    gift_builder.add_candy(cookie_b)
    gift_builder.add_candy(candy_c)

    # Вывод общей информации о подарке
    print("Подарок содержит:")
    for candy in gift_builder.gift:
        print(candy)

    print(f"Общий вес подарка: {gift_builder.get_total_weight()} г")

    # Сортировка конфет по содержанию сахара
    gift_builder.sort_by_sugar_content()
    print("\nКонфеты после сортировки по содержанию сахара:")
    for candy in gift_builder.gift:
        print(candy)

    # Поиск конфет в диапазоне содержания сахара
    min_sugar = 20
    max_sugar = 50
    found_candies = gift_builder.find_candy_by_sugar_content(
        min_sugar, max_sugar)
    print(
        f"\nКонфеты с содержанием сахара в диапазоне от {min_sugar} до {max_sugar} г:")
    for candy in found_candies:
        print(candy)


if __name__ == "__main__":
    main()