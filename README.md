Fudbyte - The Food Social Network
=======================

Run migrations ``` ./manage.py migrate ```

Run celery worker ``` celery -A fudbyte worker -l info ```


Deploying
===============================

Initial Deploy
ansible-playbook -i production site.yml


After first setup and there are further changes
ansible-playbook -i production site.yml --tags="deploy"