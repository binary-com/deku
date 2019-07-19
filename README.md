Deku [![CircleCI](https://circleci.com/gh/apoorv-binary/deku.svg?style=svg)](https://circleci.com/gh/4p00rv/deku)
====

Python service for seamless rolling updates of docker services.

----

## Usage

- Clone the repo
- Build the docker image: `docker built -t deku .`
- Start the service: `docker-compose up -d`

The service is available at *http://localhost:19231*

> Note: This service requires access to your docker socket. Refer to docker-compose.yml

Options
---

- _DOCKER_SOCKET_: Unix format uri to docker socket. eg:`unix://somefolder/docker.sock`. Needs to be passed as environment variable
- _AUTH_TOKEN_: This is used for authenticating the calls. This is passed as envrionment variable as well.


## Endpoints

/update
---

- Accepted method:  *POST*
- Parameters:
  - _secret_: Should be equal to AUTH_TOKEN for authenticating the requests. Throws `Invalid secret.` error
  - _name_: Name of service to update / get status of
  - _label_: Label associated with service to update / get status of
  - _image_: New image that service needs to be updated to. Without this parameter you will only get last update status.
