# Lumba.ai's Preprocessing Microservice



Designed to be scalable via K8s cluster. Made with [flask](https://flask.palletsprojects.com/en/3.0.x/quickstart/) . 

#### ToDo:

- Fix file saving
- API documentation
- Kube/docker config
- debugging

### Dev Guide

1. Create the file directory
   ```
   mkdir directory/{{username}}/{{workspacename}}
   ```
2. Put csv files into the above folder
3. Run on local dev

    ```
    flask --app app run
    ```
4. Import Postman Collection, change the collection variables accordingly
5. (Optional) Docker build and run

    ```
   docker build -f Dockerfile -t lumba-preproc:latest .
   docker run -p 5001:5000 lumba-preproc
    ```
    
    Should be accessible http://127.0.0.1:5001
