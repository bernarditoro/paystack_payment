# paystack_payment

This is an applet that integrates the Paystack payment gateway into any Django project.

## Prerequisites
- Django

## Usage
Run command to apply pending migrations
```bash
python manage.py migrate
```
Also make sure you have an account with [Paystack](https://paystack.com) and copy your API keys into _settings.py_ in your django project.

```python
PAYSTACK_SECRET_KEY = ""
PAYSTACK_PUBLIC_KEY = ""
```
