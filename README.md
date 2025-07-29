# Маха Фабрик — CRM для швейного цеха

Проект Django для управления заказами на пошив изделий.  
Позволяет вести базу клиентов, отслеживать этапы выполнения заказов, управлять профилем.

## Функциональность:
- Регистрация и авторизация
- Добавление и просмотр заказов
- Изменение статуса заказа
- Профиль клиента
- Панель администратора

## Стек:
- Python 3
- Django 5.2
- SQLite
- HTML/CSS (Bootstrap)
- Pillow, django-filter

## Запуск проекта

```bash
git clone https://github.com/alIm5ek0v/order-crm.git
cd order-crm
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
👤 Автор
Алимбеков Байбол Бактыбекович
E-mail: alim5ek0v.b@gmail.com
Тел: +996 995 555 211