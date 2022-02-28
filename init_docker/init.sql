
CREATE DATABASE IF NOT EXISTS `test_django_app`;

CREATE DATABASE IF NOT EXISTS `django_app`;


GRANT ALL PRIVILEGES ON `test_django_app`.* TO 'example'@'%';
GRANT ALL PRIVILEGES ON `django_app`.* TO 'example'@'%';

GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';