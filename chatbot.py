import sqlite3

# Function to fetch order details from the SQLite database
def get_order_details(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Fetch order details based on order_id
    cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
    order = cursor.fetchone()

    conn.close()

    if order:
        # Assuming we add extra columns for payment status, return status, etc.
        order_details = {
            'order_id': order[0],
            'product': order[1],
            'order_date': order[2],
            'status': order[3],
            'payment_status': order[4] if len(order) > 4 else "Not Available",  # Placeholder for payment status
            'delivery_status': order[5] if len(order) > 5 else "Not Delivered",  # Placeholder for delivery status
            'refund_status': order[6] if len(order) > 6 else "No Refund",  # Placeholder for refund status
            'damaged_item': order[7] if len(order) > 7 else "No Damage",  # Placeholder for damaged item status
        }
        return order_details
    else:
        return None

# Function to format the response based on the order details
def format_order_response(order_details):
    return (
        f"Order ID: {order_details['order_id']} - Product: {order_details['product']} "
        f"- Order Date: {order_details['order_date']} - Status: {order_details['status']} "
        f"- Payment Status: {order_details['payment_status']} - Delivery Status: {order_details['delivery_status']} "
        f"- Refund Status: {order_details['refund_status']} - Damaged Item: {order_details['damaged_item']}"
    )

# Function to get a chatbot response based on user input
def get_chatbot_response(user_message):
    user_message = user_message.lower()

    # Look for order-related queries
    if 'order' in user_message:
        # Extract order ID from the message (e.g., "order 1")
        words = user_message.split()
        if len(words) > 1 and words[-1].isdigit():
            order_id = int(words[-1])
            order_details = get_order_details(order_id)
            if order_details:
                return format_order_response(order_details)
            else:
                return "Sorry, I couldn't find the order. Please check the order ID."

    # Handle payment status query
    elif 'payment' in user_message:
        words = user_message.split()
        if len(words) > 1 and words[-1].isdigit():
            order_id = int(words[-1])
            order_details = get_order_details(order_id)
            if order_details:
                return f"The payment status for Order ID {order_id} is {order_details['payment_status']}."
            else:
                return "Sorry, I couldn't find the order. Please check the order ID."

    # Handle delivery status query
    elif 'delivered' in user_message or 'delivery' in user_message:
        words = user_message.split()
        if len(words) > 1 and words[-1].isdigit():
            order_id = int(words[-1])
            order_details = get_order_details(order_id)
            if order_details:
                return f"The delivery status for Order ID {order_id} is {order_details['delivery_status']}."
            else:
                return "Sorry, I couldn't find the order. Please check the order ID."

    # Handle refund queries
    elif 'refund' in user_message:
        words = user_message.split()
        if len(words) > 1 and words[-1].isdigit():
            order_id = int(words[-1])
            order_details = get_order_details(order_id)
            if order_details:
                return f"The refund status for Order ID {order_id} is {order_details['refund_status']}."
            else:
                return "Sorry, I couldn't find the order. Please check the order ID."

    # Handle damaged item queries
    elif 'damaged' in user_message or 'damage' in user_message:
        words = user_message.split()
        if len(words) > 1 and words[-1].isdigit():
            order_id = int(words[-1])
            order_details = get_order_details(order_id)
            if order_details:
                return f"Order ID {order_id} has the following status regarding damaged items: {order_details['damaged_item']}."
            else:
                return "Sorry, I couldn't find the order. Please check the order ID."

    # Handle product-related queries
    elif 'product' in user_message or 'item' in user_message:
        return "You can view our products on the Flipkart website. What product are you looking for?"

    elif 'hello' in user_message or 'hi' in user_message:
        return "Hello! How can I assist you today?"

    elif 'bye' in user_message or 'goodbye' in user_message:
        return "Goodbye! Have a great day!"

    elif 'thank you' in user_message:
        return "You're welcome! Let me know if you need any further assistance."

    else:
        return "I'm sorry, I didn't understand that. Could you please rephrase?"
