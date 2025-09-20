# Janitri Patient Heart Rate Monitoring API

This project is a comprehensive backend system for a patient heart rate monitoring application, developed as a backend developer assignment for Janitri. It features a secure, role-based RESTful API built with Django and Django REST Framework.

**Live Deployed API:** [`https://heartmonitor.pythonanywhere.com/`](https://heartmonitor.pythonanywhere.com/)

**Live API Documentation (Swagger UI):** [`https://heartmonitor.pythonanywhere.com/api/schema/swagger-ui/`](https://heartmonitor.pythonanywhere.com/api/schema/swagger-ui/)

---

## Features

-   **Secure JWT Authentication:** Stateless authentication using JSON Web Tokens with a token refresh mechanism. 
-   **Role-Based Access Control (RBAC):** Three distinct user roles (HOD, Doctor, Patient) with granular permissions.
-   **Data Segregation:** Robust permission system ensures that doctors can only access their own patients' data, and patients can only view their own records.
-   **Patient & Health Data Management:** Full CRUD (Create, Read, Update, Delete) functionality for patient profiles and endpoints to manage time-series heart rate data.
-   **Advanced API Features:** API-wide pagination (with 2 items per page) and powerful filtering capabilities on endpoints.
-   **Automated API Documentation:** Interactive API documentation generated automatically using `drf-spectacular` (Swagger/Redoc).
-   **Comprehensive Test Suite:** Unit and integration tests to ensure API reliability and security.
-   **Production Ready:** The application is configured for a production environment and deployed on PythonAnywhere.

---

## Setup and Installation (Local Environment)

### Prerequisites
- Python 3.10+
- Git

### Instructions
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Rounak2001/Heart-Monitor-Janitri-.git
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (HOD):**
    ```bash
    python manage.py createsuperuser
    ```
    *You will be prompted to create a username and password. This user will have HOD privileges.*

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000`.

---

## Testing with Postman & Example Workflow

This repository includes a Postman collection file: `Heart Monitoring.postman_collection.json`. To make testing as easy as possible, you can import this file directly into Postman. The collection includes saved examples for every endpoint.

### Setup
1.  In Postman, create a new **Environment**.
2.  Add a variable named `baseUrl` and set its value to the live deployment URL: `https://heartmonitor.pythonanywhere.com`.
3.  Select this environment in the top-right corner of Postman.

### Example Workflow
> **Security Note:** For security reasons, administrative credentials are not hardcoded in this repository. Please use the HOD account you created in the "Setup and Installation" step to perform the following actions.

1.  **Login as HOD:** Use the `POST /api/users/token/` request. In the body, provide the username (`"rounak"`) and password (`"12345"`) for your HOD account. Copy the `access` token from the response.
2.  **Create a Doctor:** Use the `POST /api/users/create-doctor/` request. In the `Authorization` tab, select "Bearer Token" and paste the HOD's access token. Provide details for a new doctor in the request body.
3.  **Login as Doctor:** Use the `POST /api/users/token/` request again, this time with the credentials of the doctor you just created. Copy the new `access` token.
4.  **Create a Patient:** Use the `POST /api/users/create-patient/` request. Use the **Doctor's** access token for authorization. Provide details for a new patient in the body.
5.  **Add Heart Rate Data:** Use the `POST /api/patients/{id}/heart-rates/` request. Use the **Doctor's** access token. Replace `{id}` with the ID of the patient you just created and provide a heart rate value in the body.
6.  **Test Pagination and Filtering:** Use the `GET /api/patients/` request. You will see the response is paginated with **2 items per page**. Try adding query parameters to filter the results, for example: `?full_name__icontains=John`.

The same workflow can be tested directly in the browser by selecting the **Production Server** from the dropdown menu in the [Swagger UI documentation](https://heartmonitor.pythonanywhere.com/api/schema/swagger-ui/).

---

## Running the Tests

To run the complete test suite and verify the functionality and security of all endpoints, use the following command:

```bash
python manage.py test
```

---

## Key Design Decisions & Assumptions

-   **User Creation Workflow:** A tiered registration process was implemented for security. HODs are created via the Django admin, HODs can create Doctors via a protected API endpoint, and Doctors can create Patients. There is no public self-registration for Doctors or HODs.
-   **Authentication:** JWT was chosen for its stateless nature, which is ideal for modern decoupled frontends.
-   **Database Model Design:** A key decision was to separate **Authentication** from **Profile Data**. The `User` model handles identity and credentials, while a `Patient` model (linked via a `OneToOneField`) stores application-specific profile information. This leverages Django's built-in auth system while providing a flexible and scalable structure.
-   **API Documentation Strategy:** The project uses `drf-spectacular` for auto-generated, interactive documentation (Swagger/Redoc) and includes a Postman collection for streamlined testing.