-- USERS TABLE
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL, -- Store hashed passwords
    email VARCHAR(100) UNIQUE NOT NULL
);

-- CATEGORIES TABLE
CREATE TABLE Categories (
    category_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    parent_category_id INTEGER,
    CONSTRAINT fk_parent_category FOREIGN KEY (parent_category_id) 
        REFERENCES Categories(category_id) ON DELETE SET NULL
);

-- PRODUCTS TABLE
CREATE TABLE Products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,  -- Using TEXT instead of CLOB
    price NUMERIC(10,2) NOT NULL,
    quantity INTEGER DEFAULT 0 CHECK (quantity >= 0), 
    category_id INTEGER,
    CONSTRAINT fk_product_category FOREIGN KEY (category_id) 
        REFERENCES Categories(category_id) ON DELETE CASCADE
);

-- CARTS TABLE
CREATE TABLE Carts (
    cart_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    CONSTRAINT fk_cart_user FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
);

-- CART_ITEMS TABLE
CREATE TABLE Cart_Items (
    cart_id INTEGER,
    product_id INTEGER,
    quantity INTEGER DEFAULT 1,
    PRIMARY KEY (cart_id, product_id),
    CONSTRAINT fk_cart FOREIGN KEY (cart_id) 
        REFERENCES Carts(cart_id) ON DELETE CASCADE,
    CONSTRAINT fk_cart_product FOREIGN KEY (product_id) 
        REFERENCES Products(product_id) ON DELETE CASCADE
);

-- ORDERS TABLE
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_cost NUMERIC(10,2),
    CONSTRAINT fk_order_user FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
);

-- ORDER_ITEMS TABLE
CREATE TABLE Order_Items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER DEFAULT 1,
    price NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    CONSTRAINT fk_order FOREIGN KEY (order_id) 
        REFERENCES Orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_order_product FOREIGN KEY (product_id) 
        REFERENCES Products(product_id) ON DELETE CASCADE
);

-- PRODUCT_INTERESTS TABLE
CREATE TABLE Product_Interests (
    interest_id SERIAL PRIMARY KEY,
    product_id INTEGER,
    user_id INTEGER,
    CONSTRAINT fk_interest_product FOREIGN KEY (product_id) 
        REFERENCES Products(product_id) ON DELETE CASCADE,
    CONSTRAINT fk_interest_user FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
);

-- CATEGORY_INTERESTS TABLE
CREATE TABLE Category_Interests (
    interest_id SERIAL PRIMARY KEY,
    category_id INTEGER,
    user_id INTEGER,
    CONSTRAINT fk_category_interest FOREIGN KEY (category_id) 
        REFERENCES Categories(category_id) ON DELETE CASCADE,
    CONSTRAINT fk_user_category_interest FOREIGN KEY (user_id) 
        REFERENCES Users(user_id) ON DELETE CASCADE
);

-- SALES_LOG TABLE
CREATE TABLE Sales_Log (
    log_id SERIAL PRIMARY KEY,
    order_id INTEGER,
    user_id INTEGER,
    order_date TIMESTAMP,
    total_cost NUMERIC(10,2),
    CONSTRAINT fk_log_order FOREIGN KEY (order_id) 
        REFERENCES Orders(order_id) ON DELETE CASCADE
);
