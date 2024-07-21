import threading
import time
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False

class Customer(threading.Thread):
    def __init__(self, customer_id, cafe):
        super().__init__()
        self.customer_id = customer_id
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)

class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = queue.Queue()

    def customer_arrival(self):
        for customer_id in range(1, 21):  # 20 customers
            print(f"Посетитель номер {customer_id} прибыл")
            self.serve_customer(Customer(customer_id, self))
            time.sleep(1)

    def serve_customer(self, customer):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f"Посетитель номер {customer.customer_id} сел за стол {table.number}.")
                customer.start()
                return

        print(f"Посетитель номер {customer.customer_id} ожидает свободный стол.")
        self.queue.put(customer)

# Создаем столики в кафе
tables = [Table(i) for i in range(1, 4)]
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()
customer_arrival_thread.join()

# Завершаем обслуживание
def finish_customer(customer):
    time.sleep(5)  # Время обслуживания
    for table in cafe.tables:
        if table.is_busy:
            table.is_busy = False
            print(f"Посетитель номер {customer.customer_id} покушал и ушёл.")
            if not cafe.queue.empty():
                next_customer = cafe.queue.get()
                cafe.serve_customer(next_customer)
                break