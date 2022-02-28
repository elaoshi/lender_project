# Run project

docker-composer up -d

# Document UI with docker

http://localhost:8001/swagger/

# Local

http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/

# Test

docker exec -it demo_app_1 bash

pytest --cache-clear


