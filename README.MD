[commit-shield]: https://img.shields.io/github/last-commit/Kaspary/freelancers-technology-ecommerce?style=for-the-badge&logo=GitHub
[commit-url]: https://github.com/Kaspary/freelancers-technology-ecommerce/commits/main
[linkedin-shield]: https://img.shields.io/badge/-João%20Pedro%20Kaspary-6633cc?style=for-the-badge&logo=Linkedin&colorB=2366c2
[linkedin-url]: https://linkedin.com/in/joao-pedro-kaspary
[github-shield]: https://img.shields.io/github/followers/Kaspary?label=João%20Pedro%20Kaspary&style=for-the-badge&logo=GitHub
[github-url]: https://github.com/Kaspary

[![commit-shield]][commit-url]
[![linkedin-shield]][linkedin-url]
[![GitHub followers][github-shield]][github-url]


# Freelancers Technology Ecommerce

This project was developed with python 3.10, using Django Rest Freamework. To the developing envorinment was used Sqlite3.

## Scope definition
Professionals who work in a freelance job referral network and need to buy, sell, or exchange technology products (laptops, mouses, keyboards, etc.) that allow them to perform their work quickly, optimizing their costs with work structures.

- A RESTful API must be developed to meet the functional requirements of the presented visual project.
- In this API, there are a total of 7 entities, the 3 main entities are: user, negotiation, and offer.
- In addition to the 3 main entities, we have: messages, freight, payment, and invitation. The relationship would be:
    - User can generate multiple invitations;
    - An invitation is linked to a new user registration;
    - A user carries out multiple negotiations;
    - A user sends multiple offers in a negotiation;
    - A user sends and receives multiple messages linked to a negotiation;
    - A payment is associated with a negotiation and is made by a user;
- Each created endpoint, with its respective method, must receive parameters, if applicable, such as JSON object. These parameters are available in the endpoint description.
- Every endpoint will return a JSON.
- Authentication will be done using JWT (JSON Web Token).
All endpoint returns must have the correct HTTP Code for the return action.


## To-Do

- [ ]  Correct the behavior of picture updates, as currently they are duplicating the image instead of deleting or replacing it.
- [ ]  Implement a payment method and link the payment to the bid to validate the sale acceptance.
- [ ]  Add filters to the endpoints that return a list.
- [ ]  During delivery consultation, return a list of all available methods.
- [ ]  Improve the error messages.

## Runing the API

After completing the following steps, the documentation will be available at these addresses.
- [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/).
- [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/).

### **Local runing (without docker)**

To run the following steps, make sure you are in the folder `ecommerce_api`.

1. Create a Python 3.10 virtual environment.
    
    ```bash
    python -m venv venv && source venv/bin/activate
    ```
    
2. Install the requirements.
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. Run the “*migrations”,* to create the initial database schema.
    
    ```bash
    python manage.py makemigrations && \
    python manage.py migrate
    ```
    
4. Create a superuser to begin using the API and get access to the admin dashboard.
    
    ```bash
    python manage.py createsuperuser
    ```
    
5. Run the project.
    
    ```bash
    python manage.py runserver
    ```
    

### **Running with Docker**

Before proceeding with the following steps, ensure that you are in the root of the project and have *Docker* and *Docker Compose* installed in your environment.

Run the next command to build the container.
```bash
docker-compose up --build
```
This command will execute all steps, listed under **Execução local (sem o uso do docker).**.

The default user to admin dashboard is:
- **Username:** admin
- **Password:** admin

These configs, can be modified in the `docker-compose.yml` file, by changing the values for the *DJANGO_ADMIN_USER* and *DJANGO_ADMIN_PASSWORD* arguments.

## URLs for utilities.

Once the API is running, these links can be used.

**Admin Dashboard:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
**Swagger Documentation:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
**Redoc Documentation:** [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## Endpoints

The API uses path versioning and currently supports `v1` and `v2`. The version number must be included at the beginning of the path.
The final url must like this `http://127.0.0.1:8000/api/v1/authenticate/`.

### Authenticate
- POST: /{version}/authenticate/
- DELETE: /{version}/authenticate/
- POST: /{version}/authenticate/refresh/

### Deals
- GET: /{version}/deals/
- POST: /{version}/deals/
- GET: /{version}/deals/{id}/
- PUT: /{version}/deals/{id}/
- DELETE: /{version}/deals/{id}/

### Bids
- GET: /{version}/deals/{deal_id}/bids/
- POST: /{version}/deals/{deal_id}/bids/
- GET: /{version}/deals/{deal_id}/bids/{id}/
- PUT: /{version}/deals/{deal_id}/bids/{id}/
- DELETE: /{version}/deals/{deal_id}/bids/{id}/

### Messages
- GET: /{version}/deals/{deal_id}/messages/
- POST: /{version}/deals/{deal_id}/messages/
- GET: /{version}/deals/{deal_id}/messages/{id}/
- PUT: /{version}/deals/{deal_id}/messages/{id}/
- DELETE: /{version}/deals/{deal_id}/messages/{id}/

### Payments
- GET: /{version}/deals/{deal_id}/payments
- POST: /{version}/deals/{deal_id}/payments

### Deliveries
- GET: /{version}/deals/{deal_id}/deliveries

### Users
- GET: /{version}/users/
- POST: /{version}/users/
- GET: /{version}/users/invites/
- POST: /{version}/users/invites/
- GET: /{version}/users/invites/{id}/
- PUT: /{version}/users/invites/{id}/
- DELETE: /{version}/users/invites/{id}/
- GET: /{version}/users/{id}/
- PUT: /{version}/users/{id}/
