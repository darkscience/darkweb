from fabric.api import *
from fabric.contrib import project

env.local_static_root = '/tmp/static.darkscience.ws'
env.remote_static_root = '/srv/http/'

env.roledefs.update({
    'static': ['amnesia.darkscience.ws',],
})

@roles('static')
def deploy_static():
    local('python manage.py collectstatic')
    project.rsync_project(
        remote_dir = env.remote_static_root,
        local_dir = env.local_static_root,
        delete = True
    )
