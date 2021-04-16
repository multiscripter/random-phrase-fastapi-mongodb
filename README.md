# Random phrase

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