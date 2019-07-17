import flask
from services import Services
from os import environ
import docker

app = flask.Flask(__name__)
SOCKET_URL = 'unix://var/run/docker.sock'
if 'DOCKER_SOCKET' in environ: SOCKET_URL = environ['DOCKER_SOCKET'] or SOCKET_URL


@app.route('/update', methods=['POST'])
def update():
    label = flask.request.values.get('label')
    name = flask.request.values.get('name')
    image = flask.request.values.get('image')
    service_filter = None
    DOCKER_CLIENT= docker.DockerClient(base_url=SOCKET_URL)
    services_obj = Services(DOCKER_CLIENT)
    
    if label:
        service_filter = {'label': label}

    if name:
        service_filter = service_filter or {}
        service_filter['name'] = name

    if image and service_filter:
        args = { 'update_config': { 'image': image }, 'filters': service_filter }
        return services_obj.update(**args)
    else:
        return services_obj.get_status(filters=service_filter)

if __name__ == '__main__':
    app.run()
