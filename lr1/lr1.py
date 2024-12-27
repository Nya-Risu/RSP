class Customer:
    def __init__(self, id, Surname, Name, Middlename, Address, Credit_card_number, Bank_account_number):
        self.id = id
        self.Surname = Surname
        self.Name = Name
        self.Middlename = Middlename
        self.Address = Address
        self.Credit_card_number = Credit_card_number
        self.Bank_account_number = Bank_account_number

    def __str__(self):
        return f"ID: {self.id}, Фамилия: {self.Surname}, Имя: {self.Name}, Отчество: {self.Middlename}, Адрес: {self.Address}, Номер кредитной карточки: {self.Credit_card_number}, Номер банковского счета: {self.Bank_account_number}"


# Создаем массив объектов
customers = [
    Customer(1, "Иванов", "Иван", "Артёмович", "г.Москва, ул.Севастопольская, д. 1","2234", "9876"),
    Customer(2, "Петров", "Алексей", "Иванович","г.Петербург, ул.Невского, д.2", "9876", "1234"),
    Customer(3, "Сидоров", "Дмитрий", "Алексеевич", "г.Новосибирск, ул.Советская, д.3", "1011", "1122"),
    Customer(4, "Смирнов", "Богдан", "Сергеевич", "г.Екатеринбург, ул.Киевская, д.4", "1819", "2233"),
]

# a) — список покупателей в алфавитном порядке
customers.sort(key=lambda x: x.Surname)
print("Список покупателей в алфавитном порядке:")
for customer in customers:
    print(customer)

# b) список покупателей, у которых номер кредитной карточки находится в заданном интервале
lower_bound = 1000
upper_bound = 2000

print("Список покупателей с номером кредитной карточки в заданном интервале:")
for customer in customers:
    card_number = int(customer.Credit_card_number)
    if lower_bound <= card_number <= upper_bound:
        print(customer)