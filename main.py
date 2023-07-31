# # Supermarket Final Project - by Guy Bracha
class Super:
    def __init__(self):
        self.products = []
        self.customers = []
        self.orders = []
        self.cashiers = []
        self.shift_managers = []
        self.head_manager = None

    def add_product(self, product):
        self.products.append(product)
        print(f"Product '{product.name}' added successfully.")

    def __str__(self):
        return self.name

    def remove_product(self, product):
        if product in self.products:
            self.products.remove(product)
            print(f"Product '{product.name}' removed successfully.")
        else:
            print(f"Product '{product.name}' not found.")

    def add_customer(self, customer):
        self.customers.append(customer)
        print(f"Customer '{customer.name}' added successfully.")

    def add_order(self, order):
        self.orders.append(order)
        print(f"Order '{order.id}' added successfully.")

    def add_cashier(self, cashier):
        self.cashiers.append(cashier)
        print(f"Cashier '{cashier.name}' added successfully.")

    def add_shift_manager(self, shift_manager):
        self.shift_managers.append(shift_manager)
        print(f"Shift Manager '{shift_manager.name}' added successfully.")

    def set_head_manager(self, head_manager):
        self.head_manager = head_manager
        print(f"Head Manager '{head_manager.name}' set successfully.")

    def get_product_list(self):
        return self.products

    def get_customer_list(self):
        return self.customers

    def get_order_list(self):
        return self.orders

    def get_cashier_list(self):
        return self.cashiers

    def get_shift_manager_list(self):
        return self.shift_managers

    def get_head_manager(self):
        return self.head_manager

    def save_data_to_file(self, filename):
        with open(filename, 'w') as file:
            file.write("Products:\n")
            for product in self.products:
                file.write(str(product) + "\n")
            file.write("Customers:\n")
            for customer in self.customers:
                file.write(str(customer) + "\n")
            file.write("Orders:\n")
            for order in self.orders:
                file.write(str(order.id) + "\n")
            file.write("Cashiers:\n")
            for cashier in self.cashiers:
                file.write(str(cashier) + "\n")
            file.write("Shift Managers:\n")
            for shift_manager in self.shift_managers:
                file.write(str(shift_manager) + "\n")
            file.write("Head Manager:\n")
            file.write(str(self.head_manager) + "\n")
        print("Data saved to file successfully.")

    def load_data_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                products_data = [line.strip() for line in lines if line.startswith("Products:")]
                if products_data:
                    self.products = products_data[0].split(':')[1].split(',')
                customers_data = [line.strip() for line in lines if line.startswith("Customers:")]
                if customers_data:
                    self.customers = customers_data[0].split(':')[1].split(',')
                orders_data = [line.strip() for line in lines if line.startswith("Orders:")]
                if orders_data:
                    self.orders = orders_data[0].split(':')[1].split(',')
                cashiers_data = [line.strip() for line in lines if line.startswith("Cashiers:")]
                if cashiers_data:
                    self.cashiers = cashiers_data[0].split(':')[1].split(',')
                shift_managers_data = [line.strip() for line in lines if line.startswith("Shift Managers:")]
                if shift_managers_data:
                    self.shift_managers = shift_managers_data[0].split(':')[1].split(',')
                head_manager_data = [line.strip() for line in lines if line.startswith("Head Manager:")]
                if head_manager_data:
                    self.head_manager = head_manager_data[0].split(':')[1]
            print("Data loaded from file successfully.")
        except FileNotFoundError:
            print("File not found.")


class Person:
    def __init__(self, name, id_number):
        self.name = name
        self.id_number = id_number


class Orderer(Person):
    def __init__(self, name, id_number):
        super().__init__(name, id_number)

    def add_product_to_supermarket(self, supermarket, product):
        supermarket.add_product(product)
        print(f"Product '{product.name}' added to the supermarket shelves.")

    def order_menu(self, supermarket):
        while True:
            print("Orderer Menu:")
            print("1. Add product to supermarket")
            print("2. Return to main menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                product_name = input("Enter the product name: ")
                product = Product(product_name)
                self.add_product_to_supermarket(supermarket, product)
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please try again.")


class Customer(Person):
    def __init__(self, name, id_number):
        super().__init__(name, id_number)
        self.cart = []

    def __str__(self):
        return self.name

    def add_product_to_cart(self, product):
        self.cart.append(product)
        print(f"Product '{product.name}' added to cart.")

    def customer_menu(self, cashier, supermarket):
        while True:
            print("Customer Menu:")
            print("1. Add product to cart")
            print("2. Purchase products")
            print("3. Return to main menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                product_name = input("Enter the product name: ")
                product = Product(product_name)
                self.add_product_to_cart(product)
            elif choice == "2":
                self.purchase(cashier, supermarket)
            elif choice == "3":
                break
            else:
                print("Invalid choice. Please try again.")

    def purchase(self, cashier, supermarket):
        if self.cart:
            order = Order(self, self.cart.copy())
            cashier.process_purchase(order)
            self.cart.clear()
            self.export_purchases(supermarket, order)
        else:
            print("No items in the cart.")

    def export_purchases(self, supermarket, order):
        with open('supermarket.txt', 'a') as file:
            file.write(f"Customer: {self.name}\n")
            file.write(f"Order ID: {order.id}\n")
            file.write("Products:\n")
            for product in order.cart:
                file.write(f"- {product.name}\n")
            file.write("\n")
        print("Purchases exported successfully.")


class Order:
    order_id = 1

    def __init__(self, customer, cart):
        self.id = Order.order_id
        Order.order_id += 1
        self.customer = customer
        self.cart = cart


class Cashier(Person):
    def __init__(self, name, id_number):
        super().__init__(name, id_number)

    def __str__(self):
        return self.name

    def process_purchase(self, order):
        customer = order.customer
        self.complete_purchase(order)
        print(f"Purchase completed for customer '{customer.name}'.")

    def complete_purchase(self, order):
        # Perform necessary actions to complete the purchase
        pass

    def cashier_menu(self):
        while True:
            print("Cashier Menu:")
            print("1. Process purchase")
            print("2. Return to main menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                customer_name = input("Enter the customer name: ")
                customer = find_customer_by_name(customer_name)
                if customer:
                    self.process_purchase(customer)
                else:
                    print("Customer not found.")
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please try again.")


class ShiftManager(Person):
    def __init__(self, name, id_number):
        super().__init__(name, id_number)

    def add_employee(self, employee):
        if isinstance(employee, Cashier):
            supermarket.add_cashier(employee)
            print(f"Cashier '{employee.name}' added by Shift Manager '{self.name}'.")
        else:
            print("Only Cashiers can be added by Shift Managers.")

    def shift_manager_menu(self):
        while True:
            print("Shift Manager Menu:")
            print("1. Add cashier")
            print("2. Return to main menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                cashier_name = input("Enter the cashier name: ")
                cashier = find_cashier_by_name(cashier_name)
                if cashier:
                    self.add_employee(cashier)
                else:
                    print("Cashier not found.")
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please try again.")


class HeadManager(Person):
    def __init__(self, name, id_number):
        super().__init__(name, id_number)

    def __str__(self):
        return self.name

    def get_daily_report(self):
        orders = supermarket.get_order_list()
        for order in orders:
            print(f"Order ID: {order.id}")
            print(f"Customer: {order.customer.name}")
            print("Products:")
            for product in order.products:
                print(f"- {product.name}")
            print()

    def head_manager_menu(self):
        while True:
            print("Head Manager Menu:")
            print("1. Generate daily report")
            print("2. Return to main menu")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.get_daily_report()
            elif choice == "2":
                break
            else:
                print("Invalid choice. Please try again.")


class Product:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


# Helper function to find a customer by name
def find_customer_by_name(name):
    for customer in supermarket.get_customer_list():
        if customer.name == name:
            return customer
    return None


# Helper function to find a cashier by name
def find_cashier_by_name(name):
    for cashier in supermarket.get_cashier_list():
        if cashier.name == name:
            return cashier
    return None


def add_customer_to_supermarket(supermarket, name, id_number):
    customer = Customer(name, id_number)
    supermarket.add_customer(customer)
    print(f"Customer '{customer.name}' added to the supermarket.")


# main menu function
def main_menu(supermarket):
    while True:
        print("Main Menu:")
        print("1. Add Customer")
        print("2. Orderer Menu")
        print("3. Customer Menu")
        print("4. Cashier Menu")
        print("5. Shift Manager Menu")
        print("6. Head Manager Menu")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_customer_menu(supermarket)
        elif choice == "2":
            orderer.order_menu(supermarket)
        elif choice == "3":
            customer_name = input("Enter your name: ")
            customer = find_customer_by_name(customer_name)
            if customer:
                customer.customer_menu(cashier1, supermarket)
            else:
                print("Customer not found.")
        elif choice == "4":
            cashier1.cashier_menu()
        elif choice == "5":
            shift_manager_name = input("Enter shift manager name: ")
            shift_manager_id = input("Enter shift manager ID number: ")
            shift_manager = ShiftManager(shift_manager_name, shift_manager_id)
            shift_manager.shift_manager_menu()
        elif choice == "6":
            head_manager.head_manager_menu()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


def add_customer_menu(supermarket):
    print("Add Customer Menu:")
    name = input("Enter customer name: ")
    id_number = input("Enter customer ID number: ")
    add_customer_to_supermarket(supermarket, name, id_number)


# Create supermarket instance
supermarket = Super()

# Create initial orderer
orderer = Orderer("Orderer Name", "Orderer ID")

# Create initial cashier
cashier1 = Cashier("Cashier Name", "Cashier ID")

# Create initial head manager
head_manager = HeadManager("Head Manager Name", "Head Manager ID")
supermarket.set_head_manager(head_manager)

# Start the program with the main menu
main_menu(supermarket)
