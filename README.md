

# PawHaus - PetStore

**PawHaus** is an online pet store where users can browse, add pets to the cart, and make secure payments through **Razorpay**. It's a fully-functional Django application that provides a seamless shopping experience for pet lovers.

## Features

- **User Registration & Authentication**: Users can register, log in, and manage their accounts.
- **Browse Pets**: Users can browse through available pets in different categories.
- **Add to Cart**: Users can add pets to the cart and proceed to checkout.
- **Secure Payment via Razorpay**: Integrated Razorpay for secure payments.
- **Admin Panel**: Admins can manage pet listings, users, and orders.

## Table of Contents
- [Installation Guide](#installation-guide)
- [Folder Structure](#folder-structure)
- [Technologies Used](#technologies-used)
- [Running the Application](#running-the-application)
- [Database Configuration](#database-configuration)

## Installation Guide

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/Adhityask/PawHaus.git
cd PawHaus
````

### 2. Create a Virtual Environment

Create a virtual environment to manage dependencies:

```bash
python -m venv venv
```

Activate the virtual environment:

* **For Windows**:

  ```bash
  venv\Scripts\activate
  ```
* **For macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 3. Install Dependencies

Install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configure Database (MySQL)

The project uses MySQL. Ensure you have MySQL installed and running. You can create a new database by following these steps:

1. Log into MySQL:

   ```bash
   mysql -u root -p
   ```

2. Create a new database:

   ```sql
   CREATE DATABASE pawhaus;
   ```

3. Update your `petstore/settings.py` to configure the database connection:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'pawhaus',  # Your database name here
           'USER': 'root',     # Your MySQL username
           'PASSWORD': 'your_password',  # Your MySQL password
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### 5. Run Migrations

Run Django migrations to set up the database schema:

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

To access the Django admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the superuser credentials.

### 7. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Your application should now be running at `http://127.0.0.1:8000/`.

## Folder Structure

```plaintext
.vscode/               # VS Code configuration files (optional)
petstore/              # Main Django project folder
  petapp/              # Application folder with models, views, etc.
  manage.py            # Django project management script
  petstore/settings.py # Settings for the Django project
  petstore/urls.py     # URL routing for the Django project
  petstore/wsgi.py     # WSGI entry point for deployment
static/                # Static files like CSS, JS, Images
templates/             # HTML templates for rendering pages
.gitignore             # Git ignore file
requirements.txt       # Python dependencies for the project
```

### Key Files:

* `petstore/settings.py`: Django settings, including database and third-party integrations.
* `petstore/urls.py`: URL routing for the project.
* `petstore/templates/`: Contains HTML templates used by the application.
* `petstore/static/`: Contains CSS, JS, and image files for the frontend.
* `requirements.txt`: Lists the required Python packages for the project.

## Technologies Used

* **Django**: Backend framework for developing web applications.
* **MySQL**: Database management system for storing pet and order data.
* **Razorpay**: Integrated payment gateway for secure transactions.
* **Bootstrap**: Frontend framework for a responsive design.
* **Python 3.x**: The main programming language for backend development.

## Running the Application

After completing the installation steps and configuring your environment, you can run the application locally.

1. Start the Django development server:

   ```bash
   python manage.py runserver
   ```

2. Access the application by navigating to `http://127.0.0.1:8000/` in your browser.

## Database Configuration

The project uses MySQL. Please ensure that:

* You have MySQL installed on your system.
* The MySQL server is running.
* You have updated the `DATABASES` configuration in `petstore/settings.py` to match your local database credentials.



## Contact

For any issues or suggestions, feel free to reach out to [Adhityask](https://github.com/Adhityask).

---

**PawHaus** is a simple yet powerful pet store application, and we hope it helps pet lovers manage their pet shopping experience effectively. Contributions and feedback are always appreciated!



