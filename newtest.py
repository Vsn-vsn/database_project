from tkinter import *
from tkinter import ttk
from supabase import create_client, Client

#Supabase credentials
#SUPABASE_URL = write the project url
#SUPABASE_KEY = #write the api key from supabase
#supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

import ttkbootstrap as ttk
from tkinter import *

root = Tk()
root.title("E-Commerce Dashboard")
root.geometry("800x800")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("darkly")  #built-in dark theme

# Scrollable Frame Setup
main_frame = Frame(root, bg="#333") #frame that holds other widgets, scroll bar and canvas
main_frame.pack(fill=BOTH, expand=True)

canvas = Canvas(main_frame, bg="#333", highlightthickness=0)
scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=canvas.yview)
scrollable_frame = Frame(canvas, bg="#333")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)       #listens to the event and decides what portion of the window must be scrollable so that it matches the contents 

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

def _on_mousewheel(event):      #function allows vertical scrolling using the mouse wheel.
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")     # converts the scroll to proper units and inverts it

canvas.bind_all("<MouseWheel>", _on_mousewheel)                              #standard mouse wheel event for Windows/macOS
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))   #linux
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))    #linux

#Header
header = Label(scrollable_frame, text="🛍️ E-Commerce Dashboard", font=("Segoe UI", 18, "bold"),
               bg="#2a2a2a", fg="#ffffff", pady=10)
header.pack(fill="x", padx=10, pady=(10, 5))

#Helper function that add section containers
def create_section(title):
    container = Frame(scrollable_frame, bg="#444", bd=1, relief="solid")
    container.pack(fill="x", padx=10, pady=6)
    frame = ttk.LabelFrame(container, text=title, padding=10)
    frame.pack(fill="x", padx=10, pady=5)
    return frame

#Section: User Authentication
auth_frame = create_section("🔐 User Authentication")
ttk.Label(auth_frame, text="Username").grid(row=0, column=0, sticky=W, padx=5, pady=5)
username_entry = ttk.Entry(auth_frame, width=25)
username_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(auth_frame, text="Password").grid(row=1, column=0, sticky=W, padx=5, pady=5)
password_entry = ttk.Entry(auth_frame, show="*", width=25)
password_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(auth_frame, text="Email").grid(row=2, column=0, sticky=W, padx=5, pady=5)
email_entry = ttk.Entry(auth_frame, width=25)
email_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons for registration and login
ttk.Button(auth_frame, text="Register", command=lambda: register_user()).grid(row=0, column=2, padx=10, pady=5)
ttk.Button(auth_frame, text="Login", command=lambda: login_user()).grid(row=1, column=2, padx=10, pady=5)
ttk.Button(auth_frame, text="Logout", command=lambda: logout_user()).grid(row=2, column=2, padx=10, pady=5)

# === Section: Product Catalog ===
catalog_frame = create_section("📦 Product Catalog")

search_group = Frame(catalog_frame, bg="#333")
search_group.grid(row=0, column=0, columnspan=4, pady=10, padx=5)

ttk.Button(search_group, text="Show Products", command=lambda: show_products()).pack(side=LEFT, padx=5)
ttk.Button(search_group, text="Show Categories", command=lambda: show_categories()).pack(side=LEFT, padx=5)

search_entry = ttk.Entry(search_group, width=25)
search_entry.pack(side=LEFT, padx=10)
ttk.Button(search_group, text="Search", command=lambda: search_items()).pack(side=LEFT, padx=5)

# === Section: Shopping Cart ===
cart_frame = create_section("🛒 Shopping Cart")

ttk.Label(cart_frame, text="Product ID").grid(row=0, column=0, sticky=W, padx=5, pady=5)
product_id_entry = ttk.Entry(cart_frame, width=10)
product_id_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(cart_frame, text="Quantity").grid(row=0, column=2, sticky=W, padx=5, pady=5)
quantity_entry = ttk.Entry(cart_frame, width=10)
quantity_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Button(cart_frame, text="Add to Cart", command=lambda: add_to_cart()).grid(row=0, column=4, padx=10, pady=5)
ttk.Button(cart_frame, text="View Cart", command=lambda: view_cart()).grid(row=0, column=5, padx=10, pady=5)
ttk.Button(cart_frame, text="Place Order", command=lambda: place_order()).grid(row=0, column=6, padx=10, pady=5)

# === Section: Interests ===
interest_frame = create_section("⭐ Interests")

ttk.Label(interest_frame, text="Product ID").grid(row=0, column=0, sticky=W, padx=5, pady=5)
product_id_interest_entry = product_id_entry  # Shared entry
ttk.Button(interest_frame, text="Add Product Interest", command=lambda: add_product_interest()).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(interest_frame, text="Category ID").grid(row=1, column=0, sticky=W, padx=5, pady=5)
category_id_entry = ttk.Entry(interest_frame, width=10)
category_id_entry.grid(row=1, column=1, padx=5, pady=5)
ttk.Button(interest_frame, text="Add Category Interest", command=lambda: add_category_interest()).grid(row=1, column=2, padx=5, pady=5)

#Add Products & Categories Section
add_frame = create_section("➕ Add Products & Categories")

ttk.Label(add_frame, text="Product Name").grid(row=0, column=0, sticky=W, padx=5, pady=5)
product_name_entry = ttk.Entry(add_frame, width=20)
product_name_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(add_frame, text="Description").grid(row=0, column=2, sticky=W, padx=5, pady=5)
product_desc_entry = ttk.Entry(add_frame, width=20)
product_desc_entry.grid(row=0, column=3, padx=5, pady=5)

ttk.Label(add_frame, text="Price").grid(row=1, column=0, sticky=W, padx=5, pady=5)
product_price_entry = ttk.Entry(add_frame, width=15)
product_price_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(add_frame, text="Quantity").grid(row=1, column=2, sticky=W, padx=5, pady=5)
product_quantity_entry = ttk.Entry(add_frame, width=15)
product_quantity_entry.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(add_frame, text="Category").grid(row=2, column=0, sticky=W, padx=5, pady=5)
category_dropdown = ttk.Combobox(add_frame, state="readonly", width=17)
category_dropdown.grid(row=2, column=1, padx=5, pady=5)

ttk.Button(add_frame, text="Add Product", command=lambda: add_product()).grid(row=2, column=2, padx=10, pady=5)

ttk.Label(add_frame, text="Category Name").grid(row=3, column=0, sticky=W, padx=5, pady=5)
category_name_entry = ttk.Entry(add_frame, width=20)
category_name_entry.grid(row=3, column=1, padx=5, pady=5)

ttk.Label(add_frame, text="Parent Category ID").grid(row=3, column=2, sticky=W, padx=5, pady=5)
parent_category_entry = ttk.Entry(add_frame, width=15)
parent_category_entry.grid(row=3, column=3, padx=5, pady=5)

ttk.Button(add_frame, text="Add Category", command=lambda: add_category()).grid(row=4, column=1, pady=5)

#Output Section
output_frame = create_section("📤 Output")
output_text = output_text = Text(output_frame, wrap=WORD, height=12, width=100, font=("Consolas", 10), bg="#2b2b2b", fg="#e0e0e0")
output_text.grid(row=0, column=0, padx=5, pady=5)

#Recent Orders Section
orders_frame = create_section("🧾 Recent Orders")
orders_listbox = Listbox(orders_frame, font=("Segoe UI", 10), height=6, bg="#2b2b2b", fg="#e0e0e0",width=101)
orders_listbox.grid(row=0, column=0, padx=5, pady=5,columnspan=2)

#Cancel Order Section
cancel_order_frame = create_section("❌ Cancel Order")
ttk.Label(cancel_order_frame, text="Select Order ID").grid(row=0, column=0, sticky=W, padx=5, pady=5)
cancel_order_id_entry = ttk.Entry(cancel_order_frame, width=25)
cancel_order_id_entry.grid(row=0, column=1, padx=5, pady=5)
ttk.Button(cancel_order_frame, text="Cancel Order", command=lambda: cancel_order()).grid(row=0, column=2, padx=10, pady=5)


def display_output(text):
    output_text.delete(1.0, END)
    output_text.insert(END, text)

# Functions
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    if not username or not password or not email:
        display_output("Please fill all fields to register.")
        return
    supabase.table("users").insert({
        "username": username,
        "password": password,
        "email": email
    }).execute()
    display_output("User registered!")

def login_user():
    global current_user_id
    email = email_entry.get()
    response = supabase.table("users").select("*").eq("email", email).execute()
    users = response.data
    if users:
        current_user_id = users[0]["user_id"]
        current_username = users[0]["username"]
        display_output(f"Logged in as : {current_username}")
        refresh_orders_view()
    else:
        display_output("User not found.")

def logout_user():
    global current_user_id
    current_user_id = None
    display_output("Logged out successfully.")
    orders_listbox.delete(0, END)

def show_products():
    response = supabase.table("products").select("product_id, name, price, quantity,description").execute()
    products = response.data
    display = "\n".join([f"{p['product_id']}: {p['name']} (₹{p['price']}, Description: {p['description']},Stock: {p['quantity']})" for p in products])
    display_output(display or "No products found.")

def show_categories():
    response = supabase.table("categories").select("category_id, name").execute()
    categories = response.data
    display = "\n".join([f"{c['category_id']}: {c['name']}" for c in categories])
    display_output(display or "No categories found.")

def search_items():
    query = search_entry.get().lower()
    prod_resp = supabase.table("products").select("product_id, name, price, category_id").execute().data
    cat_resp = supabase.table("categories").select("category_id, name").execute().data
    result = []

    # Here i am searching for matching products by its name
    for p in prod_resp:
        if query in p["name"].lower():
            result.append(f"[Product] {p['product_id']}: {p['name']} (₹{p['price']})")

    # Search for matching categories by name and show related products
    for c in cat_resp:
        if query in c["name"].lower():
            result.append(f"\n[Category] {c['category_id']}: {c['name']}")
            # I am Finding all products belonging to the current category
            related_products = [p for p in prod_resp if p["category_id"] == c["category_id"]]
            if related_products:
                for p in related_products:
                    result.append(f"    {p['product_id']}: {p['name']} (₹{p['price']})")
            else:
                result.append("    No products found for this category.")

    display_output("\n".join(result) or "No match found.")


def add_to_cart():
    if current_user_id is None:
        display_output("Please login first.")
        return
    try:
        pid = int(product_id_entry.get())
        qty = int(quantity_entry.get())
    except ValueError:
        display_output("Please enter valid Product ID and Quantity.")
        return
    cart_id = get_cart_id(current_user_id)
    supabase.table("cart_items").upsert({
        "cart_id": cart_id,
        "product_id": pid,
        "quantity": qty
    }).execute()
    display_output("Item added to cart.")

def place_order():
    if current_user_id is None:
        display_output("Please login first.")
        return
    try:
        supabase.rpc("place_order", {"p_user_id": current_user_id}).execute()   #remote procedure call(rpc) to call a postgre procedure through supabase client 
        display_output("✅ Order placed successfully.")
        refresh_orders_view()
    except Exception as e:
        try:
            err_json = e.args[0]
            if isinstance(err_json, dict) and 'message' in err_json:
                msg = err_json['message']
                display_output(f"❌ Order failed: {msg}")
            else:
                display_output("❌ Order failed. Please try again.")
        except:
            display_output("⚠️ Unexpected error occurred during order placement.")

def get_cart_id(user_id):
    response = supabase.table("carts").select("cart_id").eq("user_id", user_id).single().execute()
    return response.data["cart_id"]

def view_cart():
    if current_user_id is None:
        display_output("Please login first.")
        return
    cart_id = get_cart_id(current_user_id)
    items = supabase.table("cart_items").select("product_id, quantity").eq("cart_id", cart_id).execute().data
    if not items:
        display_output("Cart is empty.")
        return
    lines = [f"Product {i['product_id']}: {i['quantity']} pcs" for i in items]
    display_output("Cart Items:\n" + "\n".join(lines))

def refresh_orders_view():
    if current_user_id is None:
        return
    orders_listbox.delete(0, END)
    response = supabase.table("orders") \
        .select("order_id, order_date, total_cost") \
        .eq("user_id", current_user_id) \
        .order("order_date", desc=True) \
        .limit(5) \
        .execute()

    orders = response.data  # This is already a list

    if not orders:
        orders_listbox.insert(END, "No recent orders.")
        return

    for order in orders:
        orders_listbox.insert(END, f"Order #{order['order_id']} | Date: {order['order_date'][:10]} | ₹{order['total_cost']}")


def add_product_interest():
    if current_user_id is None:
        display_output("Please login first.")
        return
    pid_str = product_id_interest_entry.get()
    if not pid_str:
        display_output("Please enter a product ID.")
        return
    try:
        pid = int(pid_str)
    except ValueError:
        display_output("Invalid product ID. Must be a number.")
        return
    supabase.table("product_interests").insert({
        "user_id": current_user_id,
        "product_id": pid
    }).execute()
    display_output("Product added to your interests.")

def add_category_interest():
    if current_user_id is None:
        display_output("Please login first.")
        return
    try:
        cid = int(category_id_entry.get())
    except ValueError:
        display_output("Invalid category ID.")
        return
    supabase.table("category_interests").insert({
        "user_id": current_user_id,
        "category_id": cid
    }).execute()
    display_output("Category added to your interests.")

def add_product():
    if current_user_id is None:
        display_output("Please login first.")
        return

    try:
        name = product_name_entry.get()
        desc = product_desc_entry.get()
        price = float(product_price_entry.get())
        qty = int(product_quantity_entry.get())
        category_name = category_dropdown.get()
        if category_name not in category_name_to_id:
            display_output("Please select a valid category.")
            return
        cat_id = category_name_to_id[category_name]
        
        # Add product to the database
        supabase.table("products").insert({
            "name": name,
            "description": desc,
            "price": price,
            "quantity": qty,
            "category_id": cat_id
        }).execute()
        display_output(f"Product '{name}' added successfully.")
    except ValueError as e:
        display_output(f"Error: {e}")


def add_category():
    if current_user_id is None:
        display_output("Please login first.")
        return

    name = category_name_entry.get()
    parent_id_str = parent_category_entry.get()
    parent_id = int(parent_id_str) if parent_id_str.strip().isdigit() else None

    if not name:
        display_output("Category name is required.")
        return

    category_data = {"name": name}
    if parent_id is not None:
        category_data["parent_category_id"] = parent_id

    supabase.table("categories").insert(category_data).execute()

    display_output("✅ Category added successfully.")
    populate_category_dropdown()  # Refresh dropdown after adding a new category

category_name_to_id = {}

# Function to populate categories dropdown and category_name_to_id mapping
def populate_category_dropdown():
    # Fetch categories from Supabase
    response = supabase.table("categories").select("category_id, name").execute()
    categories = response.data
    
    if categories:
        # Create a mapping of category names to category IDs
        global category_name_to_id
        category_name_to_id = {category["name"]: category["category_id"] for category in categories}

        # Populate the dropdown with category names
        category_dropdown['values'] = list(category_name_to_id.keys())
        category_dropdown.current(0)  # Set default selection to the first category

# Call this function when the app starts to ensure categories are loaded
populate_category_dropdown()

def cancel_order():
    if current_user_id is None:
        display_output("Please login first.")
        return

    try:
        ordered_order_id = int(cancel_order_id_entry.get())
    except ValueError:
        display_output("Please enter a valid Order ID.")
        return

    # Call the cancel_order_func stored procedure (PostgreSQL function)
    response = supabase.rpc("cancel_order", {"ordered_order_id": ordered_order_id}).execute()
    print(response)

    if response.status_code == 200:
        display_output(f"Order #{ordered_order_id} has been canceled and stock has been restored.")
        refresh_orders_view()
    else:
        display_output("Failed to cancel the order. Please try again.")


root.mainloop()
