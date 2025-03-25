# Website Analytics App

This application provides website analysis functionality and can be used for various user roles. It supports the following user types:

- **Unauthenticated Users**
- **Authenticated Users**
- **Semi-Authenticated Users**

## Getting Started

### Requirements

Before running the app, ensure you have the following installed:

- Python (version 3.12.3 or above)
- Required dependencies (can be installed using `pip`)

### Installation

1. Clone the repository to your local machine.
   
2. Install the necessary Python packages:

   ```bash
   pip install -r requirements.txt

3. Create a .env file in the root directory of the project, which contains all the necessary environment variables. An example .env file will look like:
       ENABLE_AUTH=False
       DATABASE_URL=your_database_url
       SECRET_KEY=your_secret_key


###Running the Application
To run the app locally, use the following command:
    ```bash
    python app.py


###Environment Variables
ENABLE_AUTH:
    Set to "True" to enable authentication for users. When enabled, the auth_bp blueprint will be activated for managing user login and registration.

DATABASE_URL:
    The URL for your database. This can be configured according to the database you're using (e.g., PostgreSQL, MySQL, SQLite).

SECRET_KEY:
    A secret key used for session management and encryption. Ensure that this is kept secret.


User Roles
1. Unauthenticated Users
Unauthenticated users can access the public areas of the website but cannot access the analytics data. They will be prompted to log in if they try to access restricted content.

2. Authenticated Users
Authenticated users can access additional features, including analytics data for websites they have access to.

3. Semi-Authenticated Users
Semi-authenticated users have limited access, typically with partial or restricted analytics data.

4. Superadmin
A Superadmin is the highest user role and has full access to all the analytics data.
Note: Analytics data is only available to Superadmin users.

Creating a Superadmin
Once the application is set up, you'll need to create a Superadmin. To do this, visit the /create-superadmin route and follow the instructions to set up your Superadmin account.

Notes
By default, a user model will be created when the application starts.

Make sure that ENABLE_AUTH is set to "True" in the .env file to enable authentication features.

The Superadmin is responsible for managing other user roles and accessing the full analytics data.

