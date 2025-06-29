CREATE OR REPLACE FUNCTION trg_create_cart_func()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO Carts (user_id) VALUES (NEW.user_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_create_cart
AFTER INSERT ON Users
FOR EACH ROW
EXECUTE FUNCTION trg_create_cart_func();



CREATE OR REPLACE FUNCTION trg_log_order_func()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.total_cost <> 0 THEN
        INSERT INTO Sales_Log (order_id, user_id, order_date, total_cost)
        VALUES (NEW.order_id, NEW.user_id, NEW.order_date, NEW.total_cost);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_log_order
AFTER UPDATE OF total_cost ON Orders
FOR EACH ROW
EXECUTE FUNCTION trg_log_order_func();


CREATE OR REPLACE FUNCTION trg_check_stock_func()
RETURNS TRIGGER AS $$
DECLARE
    available INTEGER := 0;
BEGIN
    SELECT COALESCE(quantity, 0) INTO available
    FROM Products
    WHERE product_id = NEW.product_id;

    IF available < NEW.quantity THEN
        RAISE EXCEPTION 'Insufficient stock for product ID: %', NEW.product_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_stock
BEFORE INSERT ON Order_Items
FOR EACH ROW
EXECUTE FUNCTION trg_check_stock_func();


CREATE OR REPLACE FUNCTION trg_update_total_cost_func()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Orders o
    SET total_cost = COALESCE((
        SELECT SUM(p.price * oi.quantity)
        FROM Order_Items oi
        JOIN Products p ON oi.product_id = p.product_id
        WHERE oi.order_id = o.order_id
    ), 0)
    WHERE o.order_id = NEW.order_id;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_total_cost
AFTER INSERT OR UPDATE ON Order_Items
FOR EACH ROW
EXECUTE FUNCTION trg_update_total_cost_func();


CREATE OR REPLACE FUNCTION trg_update_stock_func()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Products
    SET quantity = quantity - NEW.quantity
    WHERE product_id = NEW.product_id AND quantity >= NEW.quantity;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Stock update failed for product ID: %', NEW.product_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_stock
AFTER INSERT ON Order_Items
FOR EACH ROW
EXECUTE FUNCTION trg_update_stock_func();


CREATE OR REPLACE FUNCTION place_order(p_user_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    ordering_id INTEGER;
    total_order_cost NUMERIC := 0;
BEGIN
    -- Create order
    INSERT INTO Orders (user_id, order_date, total_cost)
    VALUES (p_user_id, CURRENT_TIMESTAMP, 0)
    RETURNING order_id INTO ordering_id;

    -- Move items from cart to order
    INSERT INTO Order_Items (order_id, product_id, quantity, price)
    SELECT ordering_id, ci.product_id, ci.quantity, COALESCE(p.price, 0)
    FROM Cart_Items ci
    JOIN Products p ON ci.product_id = p.product_id
    WHERE ci.cart_id = (SELECT cart_id FROM Carts WHERE user_id = p_user_id);

    -- Compute total
    SELECT COALESCE(SUM(price * quantity), 0)
    INTO total_order_cost
    FROM Order_Items
    WHERE order_id = ordering_id;

    -- Update cost
    UPDATE Orders SET total_cost = total_order_cost WHERE order_id = ordering_id;

    -- Clear cart
    DELETE FROM Cart_Items
    WHERE cart_id = (SELECT cart_id FROM Carts WHERE user_id = p_user_id);

    RETURN ordering_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION cancel_order(ordered_order_id INTEGER)
RETURNS VOID AS $$
BEGIN
    -- Restore stock
    UPDATE Products p
    SET quantity = p.quantity + oi.quantity
    FROM Order_Items oi
    WHERE oi.product_id = p.product_id 
      AND oi.order_id = ordered_order_id;

    -- Delete items and order
    DELETE FROM Order_Items WHERE order_id = ordered_order_id;
    DELETE FROM Orders WHERE order_id = ordered_order_id;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_user_order_count(p_user_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    v_order_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO v_order_count
    FROM Orders
    WHERE user_id = p_user_id;

    RETURN v_order_count;
END;
$$ LANGUAGE plpgsql;
