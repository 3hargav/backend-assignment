 **# Order Management Application**

**## Technologies Used**

- **Flask:** Python web framework for API development
- **Celery:** Distributed task queue for asynchronous tasks
- **MySQL:** Relational database for data storage
- **Docker Compose:** Tool for defining and running multi-container applications

**## Features**

- **Order creation and retrieval**
- **Automatic order status updates using Celery Beat**

**## Getting Started**

1. **Build the Docker image:**

   ```bash
   docker compose build --no-cache
   ```

2. **Start the application:**

   ```bash
   docker compose up
   ```
The app will be running at http://localhost:5000

**## REST APIs**

**### Create Order**

   - **Endpoint:** `POST /orders`
   - **Request body:**
     ```json
     {
        "pizzas": [{
            "base": "thin_crust",
            "cheese": "mozzarella",
            "toppings":["chicken", "paneer","kaju", "mushrooms"]
        }]
     }
     ```
   - **Response:**
     ```json
     {
       "order_id": 1,
       "total_price": 15.50,
       "status": "Placed"
     }
     ```

**### Get Order**

   - **Endpoint:** `GET /orders/<order_id>`
   - **Response:**
     ```json
     {
       "order_id": 1,
       "base": "regular_crust",
       "cheese": "mozzarella",
       "toppings": ["pepperoni", "mushrooms"],
       "total_price": 15.50,
       "status": "In Progress"  // Example updated status
     }
     ```

**### Create Database Tables**

   - **Endpoint:** `POST /create_tables`
   - **Response:** (Empty response on success)

**## Scheduling with Celery Beat**

- Celery Beat is configured to regularly update order statuses based on time criteria.

**## Additional Notes**
