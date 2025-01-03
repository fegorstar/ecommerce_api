# E-commerce API Project Setup

This project is a Django REST Framework-based API for managing categories, products, and discounts.

---

## Prerequisites

Ensure the following are installed on your system:

- Python (>=3.9)
- PostgreSQL
- Virtualenv
- Git

---

## Project Setup

### 1. Clone the Repository

Download the project files from the provided source.

```bash
cd <project_folder>
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

Create a `.env` file in the project root and add the following variables:

```ini
# General Settings
ENV_SETTING=development
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost

# CORS and CSRF Settings
CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost,http://127.0.0.1

# PostgreSQL Database Variables
POSTGRES_DB=ecommerce-api
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# General Details
FRONTEND_URL=http://127.0.0.1:8000
```

### 5. Apply Migrations

Run the following command to apply database migrations:

```bash
python manage.py migrate
```

### 6. Create a Superuser

Create a superuser account to access the admin panel:

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

Start the server with:

```bash
python manage.py runserver
```

The server will be accessible at `http://127.0.0.1:8000/`.

---

## Using Django Admin for Category and Product Management

1. Navigate to the Django Admin Panel at `http://127.0.0.1:8000/admin/`.
2. Log in with your superuser credentials.
3. Create categories and products using the admin interface.
   - Set parent-child relationships for categories using the **Parent** field.

---

## Testing the API

### Using Swagger API Docs

Access the API documentation at:

- Swagger: `http://127.0.0.1:8000/api/docs/`

### Using Postman

A Postman collection is available at:

- [Postman Documentation](https://documenter.getpostman.com/view/12478388/2sAYJ99J1q#d7a7413d-8fd3-4d07-8eb4-261883a8381d)

You can import the Postman collection and test all available API endpoints.

---

## Running Tests

Run the unit tests using the following command:

```bash
python manage.py test
```

The test suite covers:

- Listing categories
- Listing products with pagination
- Filtering products by category
- Creating products
- Retrieving product details
- Applying discounts

---

