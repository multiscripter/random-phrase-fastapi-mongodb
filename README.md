# Random phrase


[![Build Status](https://travis-ci.com/multiscripter/random-phrase-fastapi-mongodb.svg?branch=master)](https://travis-ci.com/multiscripter/random-phrase-fastapi-mongodb)
[![codecov](https://codecov.io/gh/multiscripter/random-phrase-fastapi-mongodb/branch/master/graph/badge.svg?token=LUVPCW7XU7)](https://codecov.io/gh/multiscripter/random-phrase-fastapi-mongodb)

architecture: **REST**

framework: **FastAPI**

data storage: **MongoDB**

testing: **Pytest**

### Run from project root:

#### In Docker containers:
- docker-compose build
- docker-compose up -d


#### Or run server from project root:
```
uvicorn main:famd_app
```

**Run app:**
```
http://127.0.0.1:8000/
```

**OpenAPI:**
```
http://127.0.0.1:8000/docs
```

**dependencies**
- Python==3.8.7
- uvicorn==0.13.3
- aiofiles==0.5.0
- fastapi==0.61.1
- pydantic==1.6.1
- pymongo==3.11.0
- starlette==0.13.6
- jinja2==2.11.2
- requests==2.25.1
- pytest-mock==3.5.1
- pytest-cov==2.11.1