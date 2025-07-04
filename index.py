from datetime import date
from abc import ABC, abstractmethod

class Shippable(ABC):
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_weight(self):
        pass

class Products(ABC):
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    @abstractmethod
    def is_available(self, qty):
        pass

class RegularProducts(Products):
    def is_available(self, qty):
        return self.quantity >= qty

class ExpiredProducts(Products):
    def __init__(self, name, price, quantity, expiry_date):
        super().__init__(name, price, quantity)
        self.expiry_date = expiry_date

    def is_expired(self):
        return date.today() > self.expiry_date

    def is_available(self, qty):
        return self.quantity >= qty and not self.is_expired()

class ShippingProducts(Products, Shippable):
    def __init__(self, name, price, quantity, weight):
        super().__init__(name, price, quantity)
        self.weight = weight

    def get_weight(self):
        return self.weight

    def is_available(self, qty):
        return self.quantity >= qty

class ExpirableShippingProduct(ExpiredProducts, Shippable):
    def __init__(self, name, price, quantity, expiry_date, weight):
        ExpiredProducts.__init__(self, name, price, quantity, expiry_date)
        self.weight = weight

    def get_weight(self):
        return self.weight

class Customer:
    def __init__(self, balance):
        self.balance = balance

    def deduct(self, amount):
        self.balance -= amount

class Cart:
    def __init__(self):
        self.items = []

    def add(self, product, quantity):
        if isinstance(product, ExpiredProducts) and product.is_expired():
            raise ValueError(f"Product {product.get_name()} is expired")

        if product.is_available(quantity):
            self.items.append({'product': product, 'quantity': quantity})
        else:
            raise ValueError(f"Product {product.get_name()} is not available in the requested quantity")

class ShippingService:
    def ship_items(self, items):
        print("** Shipment notice **")
        total_weight = 0
        item_counts = {}

        for item in items:
            name = item.get_name()
            weight = item.get_weight()
            if name in item_counts:
                item_counts[name]['quantity'] += 1
                item_counts[name]['total_weight'] += weight
            else:
                item_counts[name] = {
                    'quantity': 1,
                    'total_weight': weight
                }

        for name, details in item_counts.items():
            print(f"{details['quantity']}x {name}    {int(details['total_weight'])}g")
            total_weight += details['total_weight']

        print(f"Total package weight {total_weight / 1000:.1f}kg\n")

def checkout(customer, cart):
    if not cart.items:
        raise ValueError("Cart is empty")

    subtotal = 0
    shippable_items = []

    for item in cart.items:
        product = item['product']
        quantity = item['quantity']

        subtotal += product.get_price() * quantity
        if isinstance(product, Shippable):
            shippable_items.extend([product] * quantity)

    shipping_fee = 30 if shippable_items else 0
    total = subtotal + shipping_fee

    if total > customer.balance:
        raise ValueError("Insufficient balance")

    customer.deduct(total)

    for item in cart.items:
        item['product'].quantity -= item['quantity']

    if shippable_items:
        shipping_service = ShippingService()
        shipping_service.ship_items(shippable_items)

    print("** Checkout receipt **")
    for item in cart.items:
        product = item['product']
        quantity = item['quantity']
        print(f"{quantity}x {product.get_name()}    {product.get_price() * quantity}")
    print("----------------------")
    print(f"Subtotal    {subtotal}")
    print(f"Shipping    {shipping_fee}")
    print(f"Amount    {total}\n")
    print(f"Customer balance after payment: {customer.balance}")


    
cheese = ExpirableShippingProduct("Cheese", 100, 10, date(2025, 8, 1), 200)
tv = ShippingProducts("TV", 500, 3, 5000)
biscuits = ExpirableShippingProduct("Biscuits", 150, 5, date(2025, 7, 30), 700)
scratchCard = RegularProducts("Scratch Card", 50, 100)

customer = Customer(1000)
cart = Cart()
cart.add(cheese, 2)
cart.add(biscuits, 1)
# cart.add(scratchCard, 1)
checkout(customer, cart)
