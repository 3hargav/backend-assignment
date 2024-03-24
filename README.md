### Steps to reproduce locally 

**Technologies Used**

- **Flask:** Python web framework for API development
- **Celery:** Distributed task queue for asynchronous tasks
- **MySQL:** Relational database for data storage
- **Docker Compose:** Tool for defining and running multi-container applications

**Features**

- **Data from the Youtube API is being fetched asynchronously using celery**

**Getting Started**
1. Clone the repository

2. **Build the Docker image:**

   ```bash
   docker compose build --no-cache
   ```

3. **Start the application:**

   ```bash
   docker compose up
   ```
The app will be running at http://localhost:5000

**REST APIs**

1. **Get videos in paginated response sorted in descending order of published datetime**

   - **Endpoint:** `GET /videos`
   - **cURL:**
     ```curl
     curl --location 'http://127.0.0.1:5000/videos?page=1&perPage=10'
     ```

2. **Search videos by either title or description**

   - **Endpoint:** `GET /search_videos`
   - **cURL:**
     ```curl
     curl --location 'http://127.0.0.1:5000/search_videos?query=football'
     ```
     
3. **Provide the API_KEY if current quota exceeded**

   - **Endpoint:** `POST /api_key`
   - **cURL:**
     ```curl
     curl --location 'http://127.0.0.1:5000/api_key' --header 'Content-Type: application/json'
     --data '{"key": "AIzaSyB5vV-PK60bd_OaIsIo2iIzUhP82diY4Uc"}'
     ```
4. **View the stored videos with filters and sorting options (admin)**

   - **Endpoint:** `GET /admin/videos`
   - **cURL:**
     ```curl
     curl --location 'http://127.0.0.1:5000/admin/videos'
     
   - **Query Params(Pass any of the filters as you like)** 
     ```text
     title=play
     description=messi
     sort_by=id (default=published_at)
     sort_order=asc (default=desc)

**Scheduling with Celery Beat**

- Celery Beat is configured for every **20 seconds** to call the Youtube data API and update the videos data in database.

**When starting the Docker containers for the first time, you may experience some delay in the web-app container connecting to the MySQL container. This delay occurs because the MySQL container needs to execute some pre-scripts during initialization.
To ensure a smooth startup process, please be patient and allow some time for the containers to initialize properly. Once the initialization process is complete, the web application should be accessible without any further delays.**