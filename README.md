## Tkinter E-Commerce Dashboard (with Supabase)

A feature-rich desktop application for managing an e-commerce platform using **Python Tkinter** for the GUI and **Supabase** as the backend database.
Supports user authentication, product catalog browsing, shopping cart, interest tracking, order placement, and order cancellation — all in a sleek, scrollable GUI.


## Features

### User Management
- Register, Login, Logout
- Email-based user identification
- Stores credentials 

### Shopping Cart
- Add products to cart with quantity
- View cart contents
- Place orders directly via Supabase RPC

### Product & Category Management
- Add new products with description, price, quantity
- Add categories (with optional parent-child structure)
- Browse products by category

### Search Functionality
- Search by product name or category
- View related items within categories

### Interest Tracking
- Add interests for specific products or categories

### Order Management
- View recent orders (last 5)
- Cancel existing orders (with inventory restoration)

### UI
- Built using `ttkbootstrap` for a dark modern look
- Scrollable interface using `Canvas` and `Scrollbar`


## Database Schema
Refer to `tables.sql` for full DDL statements.


## Supabase RPC Requirements (PL/pgSQL)
This project relies on PostgreSQL stored procedures written in PL/pgSQL, called via Supabase RPC.
These are deployed to the Supabase database and callable securely from the Python client.
Refer to `PlSql.sql` to see all the procedure and triggers used.

