# python-rabbitmq-client

## Get Started

1. Using python virtualenv
```
~$ python3 -m venv venv
~$ source venv/bin/activate
```

2. Install packages
```
~$ pip3 install -r requirements.txt
```

3. Copy example config & Set-up config
```
~$ cp config.py.example config.py
# Set-up config for your RabbitMQ
~$ vim config.py
```

## Usage

### Publish
```
~$ python3 publish.py
```

### Consume
```
~$ python3 consume.py
```
