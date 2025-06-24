# Hotel Menu Management and Visualization Suite

A full-stack web application and Visualization Suit for managing restaurant orders, built with Flask, MongoDB, and HTML/CSS/JS. The system supports customer ordering, chef dashboards, and an owner dashboard with sales analytics and export options.

![Screenshot (265)](https://github.com/user-attachments/assets/41dc3a84-7061-4a1d-867b-4589a488b808)

# 📌 Features

🍽️ Customers
View a visually appealing digital menu with images.

![Screenshot (260)](https://github.com/user-attachments/assets/d5755f25-3b45-49ab-a5b6-347abfbb2161)

![Screenshot (261)](https://github.com/user-attachments/assets/5493dc34-c79a-4665-ba19-c9d15e743001)

View a generated bill and receive a thank-you message.

![Screenshot (262)](https://github.com/user-attachments/assets/d7c2b930-39ab-428f-8111-0c785dec6d25)

![Screenshot (263)](https://github.com/user-attachments/assets/370b981c-3cee-46b2-b976-fdec6925097f)

👨‍🍳 Chef
Real-time view of incoming orders.

![Screenshot (264)](https://github.com/user-attachments/assets/35b327b6-fa90-48aa-9b93-d1ea984bc5a8)

Checkbox interface to manage dish preparation.

Page auto-refreshes for new orders.

📈 Owner
Dashboard showing:

![Screenshot (266)](https://github.com/user-attachments/assets/130e66a2-6aa1-4eb6-a97b-0d35f25f51ad)

![Screenshot (267)](https://github.com/user-attachments/assets/59dbee83-5495-4c0f-b453-c88c4d8eb7fa)

Most and least ordered dishes.

Weekly/monthly/yearly sales trends.

Top 5 regular customers.

Total profit calculation.

Export sales data as CSV or PDF.

🛠️ Tech Stack

Technology	                  Purpose

Flask	                    Backend framework

MongoDB	                  Database for user and order data

HTML, CSS, JS	            Frontend

:

# 🔄 Application Workflow
The application handles 3 user roles — Customer, Chef, and Owner — each with a specific flow:

👤 1. Customer Workflow
Login/Register using phone number.

Redirected to the Menu Page.

Select Table and Choose Dishes with quantities.

Click "Send Order" to submit.

Chef receives the order in real-time.

Click "Get Bill" when ready to pay:

Bill is displayed with total.

Orders are marked as completed.

Chef's screen is auto-refreshed to remove completed orders.

A thank-you page is shown before logout.

🍳 2. Chef Workflow
Log in as Chef using phone number.

Redirected to Chef Dashboard.

View all pending orders in real-time.

Each order shows:

Customer Name

Table Number

Dish names and quantities

Orders disappear from the screen when the customer completes payment.

🧑‍💼 3. Owner Workflow
Log in as Owner using phone number.

Redirected to Owner Dashboard with analytics:

Most ordered dish

Least ordered dish

Weekly/Monthly/Yearly profit trend

Top 5 frequent customers

Filter dashboard using time period: week, month, or year.

Option to export data as CSV or PDF.


