# Run project

docker-composer up -d

# Document UI with docker

http://localhost:8001/swagger/

# Local

http://127.0.0.1:8000/swagger/
http://127.0.0.1:8000/redoc/

# Test

docker exec -it demo_db_1 bash

pytest

# APIs
/lender
/page=1&active=0
/page=1&active=1

