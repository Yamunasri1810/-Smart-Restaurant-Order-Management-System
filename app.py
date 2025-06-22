from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'secret123'

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['hotel_orders']
users_col = db['users']
orders_col = db['orders']

menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 10, "image": "/templates/pizza.jpg"},
    {"id": 2, "name": "Spaghetti Carbonara", "price": 12, "image": "/templates/spaghetti.jpeg"},
    {"id": 3, "name": "Caesar Salad", "price": 8, "image": "/templates/salad.jpg"},
    {"id": 4, "name": "Tiramisu", "price": 6, "image": "/templates/tiramisu.jpg"},
    {"id": 5, "name": "Minestrone Soup", "price": 7, "image": "/templates/soup.jpg"},
]

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    phone = request.form['phone']
    user = users_col.find_one({"phone": phone})

    if user:
        session['user'] = {"name": user['name'], "role": user['role'], "phone": user['phone']}
        return redirect(url_for(f"{user['role']}_page"))
    else:
        return render_template('register.html', phone=phone)

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    phone = request.form['phone']

    users_col.insert_one({"name": name, "phone": phone, "role": "customer"})
    session['user'] = {"name": name, "phone": phone, "role": "customer"}
    return redirect(url_for("customer_dashboard"))

@app.route('/menu')
def customer_page():
    return render_template('menu.html', dishes=menu, datetime=datetime)

@app.route('/chef')
def chef_page():
    chef_orders = list(orders_col.find({"status": "pending"}).sort("timestamp", -1))
    
    # Convert timestamp to datetime if needed
    for order in chef_orders:
        if 'timestamp' in order and isinstance(order['timestamp'], str):
            try:
                order['timestamp'] = datetime.fromisoformat(order['timestamp'])
            except:
                order['timestamp'] = None

    return render_template("chef.html", orders=chef_orders, menu=menu)


@app.route('/owner')
def owner_page():
    one_week_ago = datetime.now() - timedelta(days=7)
    orders = list(orders_col.find({"timestamp": {"$gte": one_week_ago}}))

    dish_count = defaultdict(int)
    customer_freq = defaultdict(int)
    daily_customer_count = defaultdict(int)
    weekly_profit = defaultdict(float)
    total_profit = 0

    for order in orders:
        user_phone = order['user_phone']
        date = order.get("timestamp", datetime.now()).strftime("%A")
        customer_freq[user_phone] += 1
        daily_customer_count[date] += 1

        day = order.get("timestamp", datetime.now()).strftime("%Y-%m-%d")
        day_profit = 0

        for item in order['items']:
            dish = next((d for d in menu if d['id'] == item['id']), None)
            if dish:
                item_total = item['quantity'] * dish['price']
                dish_count[dish['name']] += item['quantity']
                day_profit += item_total
                total_profit += item_total

        weekly_profit[day] += day_profit

    sorted_dishes = sorted(dish_count.items(), key=lambda x: x[1], reverse=True)
    most_ordered = {"labels": [d[0] for d in sorted_dishes[:5]], "data": [d[1] for d in sorted_dishes[:5]]}
    least_ordered = {"labels": [d[0] for d in sorted_dishes[-5:]], "data": [d[1] for d in sorted_dishes[-5:]]}

    weekly_profits = {
        "labels": list(weekly_profit.keys()),
        "data": list(weekly_profit.values())
    }

    regular_customers = []
    for phone, count in customer_freq.items():
        if count >= 2:
            user = users_col.find_one({"phone": phone})
            if user:
                regular_customers.append(user['name'])

    return render_template(
        "owner.html",
        most_ordered=most_ordered,
        least_ordered=least_ordered,
        weekly_profits=weekly_profits,
        regular_customers=regular_customers,
        total_profit=total_profit
    )

@app.route('/submit_order', methods=['POST'])
def submit_order():
    try:
        data = request.get_json()
        if not data or 'items' not in data or 'table_number' not in data:
            return jsonify({"message": "Incomplete order data."}), 400

        order_items = data['items']
        table_number = data['table_number']

        # Store order in MongoDB
        orders_col.insert_one({
            "user_phone": session['user']['phone'],
            "user_name": session['user']['name'],
            "items": order_items,
            "table_number": int(table_number),
            "timestamp": datetime.now(),
            "status": "pending"
        })

        return jsonify({"message": "Order sent to the chef successfully!"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@app.route('/get_bill')
def get_bill():
    try:
        last_order = orders_col.find_one({"user_phone": session['user']['phone']}, sort=[('_id', -1)])
        if not last_order:
            return jsonify({"success": False, "message": "No order found."})

        bill_details = []
        total = 0
        for item in last_order['items']:
            dish = next((d for d in menu if d['id'] == item['id']), None)
            if dish:
                item_total = item['quantity'] * dish['price']
                total += item_total
                bill_details.append({
                    "name": dish['name'],
                    "quantity": item['quantity'],
                    "total_price": item_total
                })

        return jsonify({"success": True, "orders": bill_details, "total": total})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
