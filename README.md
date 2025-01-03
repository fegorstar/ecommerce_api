# E-commerce API Project Setup

This project is a Django REST Framework-based E-commerce API for managing categories, products, and discounts. Follow the steps below to set up and run the project.

---

## Prerequisites

Ensure you have the following installed on your system:

- Python (>=3.9)
- PostgreSQL
- Virtualenv
- Git
- PgAdmin4 (optional, for database management)

---

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_folder>
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the following sample variables:

```ini
# General Settings
ENV_SETTING=development
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

# CORS and CSRF Settings
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1

# PostgreSQL Database Variables
POSTGRES_DB=ecommerce-api
POSTGRES_USER=your-db-username
POSTGRES_PASSWORD=your-db-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# General Details
FRONTEND_URL=http://127.0.0.1:8000
```

### 5. Set Up the PostgreSQL Database

1. Log in to PostgreSQL:
   ```bash
   psql -U postgres
   ```

2. Create a database:
   ```sql
   CREATE DATABASE "ecommerce-api";
   ```

3. Alternatively, use PgAdmin4:
   - Open PgAdmin4 and log in with your PostgreSQL credentials.
   - Navigate to "Databases" > "Create" > "Database".
   - Enter the database name (`ecommerce-api`) and save.

4. Ensure the `.env` file is updated with the correct database details before proceeding.

### 6. Apply Migrations

```bash
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/docs/`.

---

## Using Django Admin for Category Creation

1. Go to the Django Admin Panel: `http://127.0.0.1:8000/admin/`
2. Log in with your superuser credentials.
3. Navigate to **Categories** and create new categories.
   - You can create parent-child relationships using the **Parent** field.

---

## Testing

Run tests using the following command:

```bash
python manage.py test
```

All tests are located in the `products/tests.py` file and cover key API functionalities, including:

- Listing categories
- Listing products with pagination
- Filtering products by category
- Creating products
- Retrieving product details
- Applying discounts

---

## API Documentation and Testing

The project supports API documentation and testing through the following tools:

- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- Postman Documentation: [Postman Link](https://documenter.getpostman.com/view/12478388/2sAYJ99J1q#d7a7413d-8fd3-4d07-8eb4-261883a8381d)

---
