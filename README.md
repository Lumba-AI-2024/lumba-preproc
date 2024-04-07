# Lumba.ai's Preprocessing Microservice



Designed to be scalable via K8s cluster. Made with flask.

#### ToDo:

- Fix file saving
- API documentation
- Kube/docker config
- debugging

### Dev Guide

1. Local dev

    ```
    flask --app app run
    ```

2. Docker build and run

    ```
   docker build -f Dockerfile -t lumba-preproc:latest .
   docker run -p 5001:5000 lumba-preproc
    ```
    
    Should be accessible http://127.0.0.1:5001
