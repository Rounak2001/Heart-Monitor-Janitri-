# Heart Monitor

This project is a RESTful API for a patient heart rate monitoring system, built with Django and Django REST Framework.

---

## Features

-   **Role-Based Authentication:** Secure JWT-based authentication for three user roles: HOD, Doctor, and Patient.
-   **Permission System:** Robust, role-based and object-level permissions.
    -   HODs can manage Doctors.
    -   Doctors can manage their own Patients and their health data.
    -   Patients can only view their own data.
-   **Patient Management:** Full CRUD API for managing patient profiles.
-   **Heart Rate Monitoring:** API endpoints to record and retrieve time-series heart rate data.
-   **Advanced Features:** API-wide pagination and powerful filtering capabilities on endpoints.
-   **Unit Tested:** Comprehensive test suite to ensure API reliability and security.

---

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <repository-name>
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Create a superuser (HOD):**
    ```bash
    python manage.py createsuperuser
    ```


6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

---

## API Endpoints

*(Here you should document your main endpoints. A table is a great way to do this.)*

| Endpoint                      | Method | Role Required | Description                                     |
| ----------------------------- | ------ | ------------- | ----------------------------------------------- |
| `/api/users/token/`           | `POST` | Public        | User login to get JWT access/refresh tokens.    |
| `/api/users/create-doctor/`   | `POST` | HOD           | Creates a new user with the 'Doctor' role.      |
| `/api/users/create-patient/`  | `POST` | Doctor        | Creates a new Patient and their login account.  |
| `/api/patients/`              | `GET`  | Doctor / HOD  | Lists patients with pagination and filtering. |
| `/api/patients/<id>/`         | `GET`  | Doctor / HOD  | Retrieves details of a specific patient.        |
| `/api/patients/<id>/heart-rates/` | `GET`  | Doctor / Patient | Lists heart rate data for a patient.     |
| `/api/patients/<id>/heart-rates/` | `POST` | Doctor        | Creates a new heart rate record for a patient.  |

---

## Running the Tests

To run the complete test suite, use the following command:

```bash
python manage.py test
```

---

## Design Decisions & Assumptions

-   **User Creation Flow:** The system uses a tiered registration process for security: HODs create Doctors, and Doctors create Patients. Patients do not have a public self-registration endpoint.
-   **Authentication:** JWT was chosen for its stateless nature, making it ideal for decoupled frontends (SPAs/mobile apps).
-   *(Add any other decisions you made here.)*