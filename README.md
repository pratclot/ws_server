# Basic websocket server in python

To use it with docker-compose:

- export API_SERVER and LOCAL_PORT variables
```bash
export API_SERVER=server.com:8080
export LOCAL_PORT=20080
```
- build Docker image
```bash
docker-compose build
```
- run the service
```bash
docker-compose up -d
docker-compose logs -f
```
