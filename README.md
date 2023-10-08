# Mailing Service

Mailing Service is a Django-based API for managing mailing campaigns and sending messages to clients based on specified rules.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)



## Getting Started

### Prerequisites

- Python 3.x
- Django and Django REST framework
- Postgresql
- Celery
- Redis
- This project has an external service that can accept requests to send messages to clients.
The OpenAPI specification is located at: https://probe.fbrq.cloud/docs
This API assumes authentication using JWT. 
- [External Service API Token](https://probe.fbrq.cloud/docs)

### Installation

#### Start project using docker-compose
1. The first thing to do is to clone the repository:
    ```bash
    git clone https://github.com/marik177/test-mail-sending.git
   ```
2. Using the Dockerfile and docker-compose.yaml run the project:
   ```bash
   docker-compose up --build
   ```
3. In new terminal window run command:
   ````bash
   docker-compose exec web sh
   ````
4. Run the migrations in the container, create a superuser, and populate the database with initial data:
   ````bash
   python manage.py migrate
   
   python manage.py createsuperuser
 
   python3 manage.py loaddata data_dump.json
   ````
5. To run tests, use the following command:
   ```bash
   docker-compose exec web pytest
   ```
   
#### Start the project without Docker:
1. The first thing to do is to clone the repository:
    ```bash
    git clone https://github.com/marik177/test-mail-sending.git
    
    cd messaging-service
    ```
2. Create a virtual environment to install dependencies in and activate it:
    ```bash
    python3 -m venv venv
   
    source venv/bin/activate
    ```   
3. Then install the dependencies:
    ```bash
   (env)$ pip install -r requirements.txt
    ```
    &emsp; Note the (env) in front of the prompt.

    &emsp; This indicates that this terminal session operates in a virtual environment set.


4. Once pip has finished downloading the dependencies make migrations:
    ```bash
    python3 manage.py migrate
    ```
5. Create superuser:
    ````bash
    python3 manage.py createsuperuser
    ````
   
6. Load testing data:
    ````bash
    python3 manage.py loaddata data_dump.json
    `````

7. And finally run the test server:
    ````bash
    (env)$ python3 manage.py runserver
   ````

8. Start Celery
   ```bash
   celery -A messages_sender worker -l INFO
   ```
9. Start Flower
   ```bash
   celery -A messages_sender flower
   ```
10. To run tests, use the following command:
   ```bash
   pytest
   ```

### Usage
Access the admin interface by navigating to http://localhost:8000/admin/ and log in using the superuser credentials created earlier.
Use the admin interface to manage clients, campaigns, and messages.

You could acceess project documentation http://localhost:8000/docs/.

You could monitor  and manage Celery using Flower http://localhost:5555

You can also interact with the API using the available endpoints (see [API Endpoints](#api-endpoints)).




### API Endpoints

#### Clients

- GET /api/clients/: List all clients.
- POST /api/clients/: Create a new client.
- GET /api/clients/{client_id}/: Retrieve a specific client.
- PUT /api/clients/{client_id}/: Update a client's information.
- DELETE /api/clients/{client_id}/: Delete a client.
- 
#### Campaigns

- GET /api/campaigns/: List all campaigns.
- POST /api/campaigns/: Create a new campaign.
- GET /api/campaigns/{campaign_id}/: Retrieve a specific campaign.
- PUT /api/campaigns/{campaign_id}/: Update a campaign's information.
- DELETE /api/campaigns/{campaign_id}/: Delete a campaign.
- GET /api/campaigns/full: List all campaigns with all sent messages.
- GET /api/campaigns/{campaign_id}/detail: Retrieve a specific campaign with all sent messages.

#### Messages

- GET /api/messages/: List all messages.
- GET /api/messages/{message_id}/: Retrieve a specific message.
- PUT /api/messages/{message_id}/: Update a message.
- POST /api/messages/: Create a new message.
- DELETE /api/messages/{message_id}/: Delete a message.

### Mailing rules
#### Filter properties of clients to whom mailing should  send out:
- Simultaneously mobile operator code and  tags


### An overview of the Django models used in the project

#### Tag

The `Tag` model represents a tag used for filtering clients. It has the following fields:

- `name`: SlugField with a maximum length of 200 characters, and it is unique.

#### MailSender

The `MailSender` model represents a mail sender configuration. It has the following fields:

- `sending_start`: DateTimeField representing the sending start time.
- `text`: TextField with a maximum length of 255 characters for the message text.
- `sending_stop`: DateTimeField representing the sending stop time.
- `filters`: Many-to-Many relationship with the `Tag` model for filtering clients. It is related through the `related_name='mail_sender'`.

#### Client

The `Client` model represents a client with phone number and tags. It has the following fields:

- `phone_number`: CharField representing the phone number in the format "7XXXXXXXXXX" (11 characters), and it is unique.
- `tags`: Many-to-Many relationship with the `Tag` model for assigning tags to clients. It is related through the `related_name='clients'`.
- `timezone`: CharField representing the client's time zone.

#### Properties

- `mobile_operator_code`: Returns the mobile operator code based on the client's phone number.

#### Message

The `Message` model represents a sent message. It has the following fields:

- `created`: DateTimeField representing the message creation timestamp.
- `send_status`: BooleanField indicating the send status of the message.
- `mail_sender`: ForeignKey relationship with the `MailSender` model, indicating the mail sending associated with the message.
- `client`: ForeignKey relationship with the `Client` model, indicating the client associated with the message.
