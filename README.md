# Chat Application

Django based real-time chat web application for demonstrating power of Django Channels and Sagas.
Includes tests coverage with py.test and jest.

You can define the length of chat messages history using settings.py variable CHAT_QUEUE_LEN

### Django Channels React React Redux Saga WebSockets

### Installation

    git clone https://github.com/onary/tchannels.git
    source env/bin/activate
    cd tchannels
    pip install -r requirements.txt
    yarn
    ./manage.py migrate
    ./manage.py runserver

### Run tests

    ./manage.py test
    yarn test

### Build frontend

    yarn build
