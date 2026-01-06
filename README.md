# order-and-inventory-management-system

📦 Order and Inventory Management System

A role-based web application built using Flask and MySQL that allows users to place orders and administrators to manage products, inventory, and orders efficiently through a centralized dashboard.


📁 Project Structure

   order-and-inventory-management-system/
│
├── app.py                  # Main Flask application (routes & logic)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── static/
│   ├── css/
│   │   └── style.css       # Common styling for all pages
│   └── images/             # UI images/icons (if any)
│
├── templates/
│   ├── login.html          # Login page
│   ├── register.html       # User registration page
│   ├── dashboard.html      # Admin dashboard
│   ├── products.html       # User product listing
│   ├── orders.html         # User orders page
│   ├── admin_products.html # Admin product management
│   └── admin_orders.html   # Admin order management
│
├── venv/                   # Virtual environment (ignored in Git)


⚙️ Tech Stack

Frontend: HTML, CSS, Bootstrap
Backend: Python (Flask)
Database: MySQL
Version Control: Git & GitHub
Tools: VS Code, Command Prompt



✨ Key Features (Admin vs User)

👤 User Features

User registration & login
View available products
Place orders
View order history and status
Clean navigation bar & responsive UI

🛠️ Admin Features

Secure admin login
Admin dashboard with:
Total revenue
Total orders
Delivered orders
Cancelled orders
Product management:
Add products
Delete products
Track stock levels
Order management:
View all user orders
Update order status (PLACED / DELIVERED / CANCELLED)
Delete orders
Admin-only control (users cannot access admin routes)







