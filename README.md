# SwitchECommerce 🛍️

> **A Full-Featured E-Commerce Web Application Built with Django**

**SwitchECommerce** is a robust B2C web application designed to simulate a real-world online store for premium electronics. It covers the complete customer journey—from secure account creation and product browsing to dynamic cart management and order processing—providing a seamless experience for users and powerful management tools for administrators.

---

## 📖 Table of Contents
- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Database Architecture](#-database-architecture)
- [Installation & Setup](#-installation--setup)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)

---

## 🔭 Project Overview
The primary objective of SwitchECommerce is to provide a scalable platform where users can browse products (specifically focused on gadgets like iPhones and MacBooks), manage their shopping carts, and place orders securely.

* **Scope:** Full-stack implementation handling frontend UI, backend logic, and database transactions.
* **Target Audience:** Tech-savvy consumers looking for high-end electronics.

---

## 🌟 Key Features

### 🔐 User Management
* **Secure Authentication:** Standard Signup, Login, and Logout functionality using Django’s auth system.
* **Profile Management:** Users can update personal details (Name, Email) via a dedicated dashboard.
* **Advanced Security:** Custom **OTP-based Password Reset** system.
    * Generates a random 6-digit code.
    * Code validity is strictly limited to **10 minutes** for enhanced security.

### 🛒 Shopping Experience
* **Product Discovery:**
    * Filter products by **Category** (e.g., Mobiles, Laptops).
    * **Pagination** support (12 items per page) for optimized loading.
    * Detailed product views with high-resolution images.
* **Smart Cart:**
    * **Database-Backed Persistence:** Cart items are stored in the database, allowing users to log out and return later without losing their items.
    * Real-time subtotal and grand total calculations.

### 📦 Checkout & Ordering
* **Inventory Management:**
    * System automatically validates stock levels before confirming an order.
    * **Stock Reduction:** Successfully placed orders immediately subtract quantity from the global inventory to prevent overselling.
* **Order Snapshot:** Records exact item price and name at the time of purchase to preserve historical data accuracy.
* **Email Notifications:** Automated confirmation emails sent to users with order summaries.

### 📞 Customer Support
* **Contact System:** Integrated inquiry form that saves messages to the database and notifies admins via email.
* **Interactive FAQs:** A dynamic FAQ section where users can submit new questions if their issue isn't listed.

---

## 🛠 Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python & Django | Utilizes MVT architecture for core logic. |
| **Frontend** | HTML5, CSS3, JS | Responsive design with jQuery and Swiper.js. |
| **Database** | SQLite | Default relational DB managed via Django ORM. |
| **Utilities** | Django Core Mail | SMTP services for OTPs and Order alerts. |

---

## 🗄 Database Architecture
The system uses a relational schema defined in `models.py`:

* **Product:** Stores `title`, `price`, `description`, `image`, and `stock_quantity`.
* **Category:** Groups products (e.g., "Mobiles") with cover images.
* **Cart & CartItem:** Links specific products to a user's active session.
* **Order & OrderItem:** Captures shipping info and "freezes" transaction details (price/qty) for historical records.
* **PasswordResetOTP:** Temporary table storing 6-digit codes with timestamps for validation.

---

## 💻 Installation & Setup

Follow these steps to copy the repository and initialize the project on your local machine.

### Prerequisites
* **Python 3.x** installed
* **Git** installed

### 1. Clone the Repository
Open your terminal and run the following command to download the code:
```bash
git clone [https://github.com/bikrampy/SwitchECommerce](https://github.com/bikrampy/SwitchECommerce)
cd SwitchECommerce
```

### 2. Create a Virtual Environment
It is best practice to run Django projects in an isolated environment.
```bash
# Windows
python -m venv venv
venv\Scripts\activate
# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages. Based on the project structure, you need Django, Pillow (for images), and Widget Tweaks (for forms).

```bash
pip install django pillow django-widget-tweaks
```

### 4. Database Migrations
Navigate to the project folder (where manage.py is located) and initialize the database.

```bash
cd ecom
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)
Create an admin account to manage products and categories.

```bash
python manage.py createsuperuser
# Follow the prompts to set a username, email, and password.
```

### 6. Run the Server
Start the development server.

```Bash
python manage.py runserver
```

Open your browser and navigate to: http://127.0.0.1:8000/

---

## 🔮 Future Enhancements

- Payment Gateway: Integration with Stripe/PayPal for real-time payments.
- Order Tracking: Status updates (Shipped/Delivered) visible in the user profile.
- Product Reviews: Allowing verified buyers to rate and review items.

---

## 📄 License
This project is open-source and available under the MIT License.

---

Built with ❤️ by BeingBifrons

---