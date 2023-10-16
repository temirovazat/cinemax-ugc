## Cinemax UGC

[![python](https://img.shields.io/static/v1?label=python&message=3.8%20|%203.9%20|%203.10&color=informational)](https://github.com/temirovazat/cinemax-ugc/actions/workflows/main.yml)
[![dockerfile](https://img.shields.io/static/v1?label=dockerfile&message=published&color=2CB3E8)](https://hub.docker.com/r/temirovazat/ugc_api)
[![lint](https://img.shields.io/static/v1?label=lint&message=flake8%20|%20mypy&color=brightgreen)](https://github.com/temirovazat/cinemax-ugc/actions/workflows/main.yml)
[![code style](https://img.shields.io/static/v1?label=code%20style&message=WPS&color=orange)](https://wemake-python-styleguide.readthedocs.io/en/latest/)
[![platform](https://img.shields.io/static/v1?label=platform&message=linux%20|%20macos&color=inactive)](https://github.com/temirovazat/cinemax-ugc/actions/workflows/main.yml)

### **Description**

_The goal of this project is to implement a service for convenient storage of analytical information and UGC (User-Generated Content). UGC encompasses everything users add to your site, such as likes, bookmarks, and movie reviews. As a result, the storage not only needs to handle large data but also provide fast access to it (within 200 milliseconds). Therefore, as part of this project, research was conducted to meet these requirements, and MongoDB, a document-oriented NoSQL database, was chosen as the database solution. An asynchronous framework, FastAPI, is used to provide an API layer for the project. The project is run through an NGINX proxy server, which serves as the entry point for the web application._

### **Technologies**

```Python``` ```FastAPI``` ```MongoDB``` ```NGINX``` ```Gunicorn``` ```Docker```

### **How to Run the Project:**

Clone the repository and navigate to the `/infra` directory:
```
git clone https://github.com/temirovazat/cinemax-ugc.git
```
```
cd cinemax-ugc/infra/
```

Create a .env file and add project settings:
```
nano .env
```
```
# MongoDB
MONGO_HOST=mongo
MONGO_PORT=27017
```

Deploy and run the project in containers:
```
docker-compose up
```

The API documentation will be available at:
```
http://127.0.0.1/openapi
```