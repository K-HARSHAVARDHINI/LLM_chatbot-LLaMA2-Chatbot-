import sqlite3
import os
import re

# === DATABASE SETUP ===
db_filename = "order_management.db"

def init_db():
    if os.path.exists(db_filename):
        os.remove(db_filename)
        print("✅ Old database deleted!")

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS product_info (
        product_id TEXT PRIMARY KEY,
        name TEXT,
        features TEXT,
        price REAL
    );

    CREATE TABLE IF NOT EXISTS order_status (
        order_id TEXT PRIMARY KEY,
        customer_name TEXT,
        status TEXT
    );

    CREATE TABLE IF NOT EXISTS support_contacts (
        department TEXT PRIMARY KEY,
        phone TEXT,
        email TEXT
    );

    CREATE TABLE IF NOT EXISTS faq (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        keywords TEXT,
        answer TEXT
    );
    """)
    print("✅ Tables created!")

    cursor.executemany("INSERT INTO product_info VALUES (?, ?, ?, ?)", [
        ('PROD001', 'Galaxy S23', '6.1-inch, 8GB RAM, 128GB Storage', 79999),
        ('PROD002', 'iPhone 14', '6.1-inch, A15 Bionic, 128GB Storage', 89999),
        ('PROD003', 'MacBook Pro', 'M2 Chip, 16GB RAM, 512GB SSD', 199999),
        ('PROD004', 'Dell XPS 13', '13.3-inch, Intel i7, 16GB RAM, 512GB SSD', 124999),
        ('PROD005', 'OnePlus 11', 'Snapdragon 8 Gen 2, 16GB RAM, 256GB Storage', 59999),
        ('PROD006', 'iPad Air', '10.9-inch, M1 Chip, 64GB Storage', 61999),
        ('PROD007', 'Pixel 8', 'Tensor G3, 8GB RAM, 128GB Storage', 69999),
        ('PROD008', 'ASUS ROG Phone 7', 'Gaming, 16GB RAM, 512GB Storage', 85999),
        ('PROD009', 'Lenovo Yoga 9i', '14-inch, Intel i7, 16GB RAM', 109999),
        ('PROD010', 'HP Spectre x360', '13.5-inch, OLED, 16GB RAM, 1TB SSD', 139999)
    ])

    cursor.executemany("INSERT INTO order_status VALUES (?, ?, ?)", [
        ('ORD1234', 'John Doe', 'Shipped'),
        ('ORD5678', 'Arjun Kapoor', 'In Transit'),
        ('ORD4321', 'Sneha Reddy', 'Delivered'),
        ('ORD8765', 'Raj Patel', 'Cancelled'),
        ('ORD9999', 'Aisha Khan', 'Processing'),
        ('ORD2024', 'Vikram Menon', 'Delivered'),
        ('ORD2025', 'Neha Sharma', 'Shipped'),
        ('ORD2026', 'Vikas Gupta', 'In Transit'),
        ('ORD2027', 'Priya Das', 'Pending'),
        ('ORD2028', 'Anil Kumar', 'Returned')
    ])

    cursor.executemany("INSERT INTO support_contacts VALUES (?, ?, ?)", [
        ('Sales', '123-456-7890', 'sales@example.com'),
        ('Tech Support', '987-654-3210', 'support@example.com'),
        ('Billing', '111-222-3333', 'billing@example.com'),
        ('Returns', '444-555-6666', 'returns@example.com'),
        ('Warranty', '777-888-9999', 'warranty@example.com'),
        ('Accounts', '999-111-2222', 'accounts@example.com')
    ])

    cursor.executemany("INSERT INTO faq (question, keywords, answer) VALUES (?, ?, ?)", [
        ('How to track my order?', 'track,order,shipping', 'Track your order under "My Orders" in your profile.'),
        ('How to contact support?', 'contact,support', 'Email support@example.com or call 987-654-3210.'),
        ('What is the return policy?', 'return,refund', 'Return items within 10 days of delivery.'),
        ('How long is the warranty?', 'warranty,duration', '1-year warranty unless mentioned otherwise.'),
        ('Do you offer EMI?', 'emi,installments,payment', 'Yes, EMI options are available at checkout.'),
        ('Where is my invoice?', 'invoice,bill', 'Invoices are available in the order details section.'),
        ('Can I cancel my order?', 'cancel,cancellation', 'Orders can be canceled before they are shipped.'),
        ('How to change delivery address?', 'change,address,delivery', 'Edit the address in your profile before dispatch.'),
        ('How to reset my password?', 'reset,password,forgot', 'Use the "Forgot Password" link on login page.'),
        ('Can I get a GST invoice?', 'gst,invoice,bill', 'Yes, enable GST billing in your account settings.')
    ])

    conn.commit()
    conn.close()
    print("✅ Sample data inserted!\n")

# === BOT LOGIC FUNCTIONS ===

def fetch_order_status(user_query):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        match = re.search(r"\bORD\d+\b", user_query.upper())
        if not match:
            return "⚠️ No valid order ID found!"
        order_id = match.group()
        cursor.execute("SELECT * FROM order_status WHERE order_id = ?", (order_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return f"📦 Order {row[0]} for {row[1]} is currently: {row[2]}"
        else:
            return "⚠️ No matching order found!"
    except Exception as e:
        return f"❌ Error: {e}"

def fetch_product_price(user_query):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM product_info")
        for name, price in cursor.fetchall():
            if name.lower() in user_query.lower():
                conn.close()
                return f"💰 The price of {name} is ₹{price}"
        conn.close()
        return "⚠️ No data found."
    except Exception as e:
        return f"❌ Error: {e}"

def fetch_support_contact(user_query):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        departments = ["Sales", "Tech Support", "Billing", "Returns", "Warranty", "Accounts"]
        for dept in departments:
            if dept.lower() in user_query.lower():
                cursor.execute("SELECT phone, email FROM support_contacts WHERE department = ?", (dept,))
                result = cursor.fetchone()
                if result:
                    phone, email = result
                    conn.close()
                    return f"📞 {dept} Team\nPhone: {phone}\nEmail: {email}"
        conn.close()
        return "❓ No matching support department found."
    except sqlite3.Error as e:
        return f"❌ SQL execution failed: {e}"

def fetch_faq_answer(user_query):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT question, answer FROM faq")
        for question, answer in cursor.fetchall():
            if any(word in user_query.lower() for word in question.lower().split()):
                conn.close()
                return f"❓ {question}\n💡 {answer}"
        conn.close()
        return "❓ Sorry, I couldn't find a related FAQ."
    except Exception as e:
        return f"❌ FAQ error: {e}"

def fetch_orders_by_customer(user_query):
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        name_match = re.search(r"(for|by)\s+([a-zA-Z]+)", user_query)
        if name_match:
            customer_name = name_match.group(2)
            cursor.execute("SELECT order_id, status FROM order_status WHERE customer_name LIKE ?", (f"%{customer_name}%",))
            orders = cursor.fetchall()
            conn.close()
            if orders:
                return "\n".join([f"📦 Order {oid} - {status}" for oid, status in orders])
            else:
                return "⚠️ No orders found for that customer."
        else:
            return "⚠️ No customer name detected."
    except Exception as e:
        return f"❌ Order history error: {e}"

def simulate_sql_error():
    try:
        conn = sqlite3.connect(db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT category FROM support_contacts")  # Invalid column
        return cursor.fetchall()
    except Exception as e:
        return f"❌ Internal error occurred."

# === MAIN CHAT LOOP ===

def run_bot():
    print("🦙 LLaMA2 Chatbot\nAsk me anything related to orders, pricing, tech support, and more!\n")
    while True:
        user_query = input("💬 Your Message\n\nYou: ")
        query_lower = user_query.lower()

        if "exit" in query_lower:
            print("👋 Exiting. Goodbye!")
            break
        elif "price" in query_lower:
            print("Bot:", fetch_product_price(user_query))
        elif "order" in query_lower and "ord" in user_query.upper():
            print("Bot:", fetch_order_status(user_query))
        elif "orders for" in query_lower or "orders by" in query_lower:
            print("Bot:", fetch_orders_by_customer(user_query))
        elif "tech support" in query_lower and "contact" in query_lower:
            print("Bot:", fetch_support_contact(user_query))
        elif any(dept in query_lower for dept in ["sales", "returns", "billing", "warranty", "accounts"]):
            print("Bot:", fetch_support_contact(user_query))
        elif "how" in query_lower or "help" in query_lower or "faq" in query_lower:
            print("Bot:", fetch_faq_answer(user_query))
        else:
            print("Bot: I'm not sure how to help with that. Try asking about order status, pricing, support, or FAQs.")

# === RUN ===
if __name__ == "__main__":
    init_db()
    run_bot()
