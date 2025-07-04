# Fawry Rise Journey - Full Stack Internship Challenge

## 💡 Challenge Description

This project is a solution to Fawry's Full Stack Development Internship Challenge.  
It implements a simple e-commerce system using **Object-Oriented Programming (OOP)** principles in Python.

### ✨ Features Implemented

- Define products with:
  - `name`, `price`, `quantity`
- Support for:
  - **Expirable Products** (e.g., Cheese, Biscuits)
  - **Shippable Products** (e.g., Cheese, TV)
  - **Regular Products** (e.g., Mobile Scratch Cards)
- Add items to cart with specific quantity (not more than available stock)
- Prevent adding expired products
- Checkout process that:
  - Calculates subtotal
  - Adds shipping fee (if applicable)
  - Verifies customer balance
  - Deducts from balance and updates stock
  - Sends shippable items to `ShippingService`

---

## 🧱 Class Design Overview

- `Products (Abstract)`  
  Base class for all products

- `RegularProducts`, `ExpiredProducts`, `ShippingProducts`, `ExpirableShippingProduct`  
  Specialized types for different product behaviors

- `Shippable (Interface)`  
  Any class that implements `get_name()` and `get_weight()` is shippable

- `Customer`  
  Holds customer balance and handles payments

- `Cart`  
  Holds added products and validates availability & expiry

- `ShippingService`  
  Accepts shippable items and prints shipment notice

- `checkout()`  
  Validates cart, processes order, prints invoice

---

## ▶️ How to Run

1. Make sure you have Python 3 installed.
2. Save the code in a file named `index.py`
3. Run from terminal:

```bash
python index.py
