from contextlib import contextmanager
from fabric.api import env, local, run, cd, prefix


def vagrant():
    """Install env.config."""

    env.user = 'vagrant'
    env.hosts = ['127.0.0.1:2222']

    # find running VM (assuming only one is running)
    result = local('vagrant global-status | grep running', capture=True)
    machineId = result.split()[1]

    # use vagrant ssh key
    result = local(
        'vagrant ssh-config {} | grep IdentityFile'.format(machineId),
        capture=True
    )
    env.key_filename = result.split()[1]

    env.app_dir = '/vagrant/final_project'
    env.activate3_5 = 'source .env/bin/activate'
    env.activate2_7 = 'source .env2/bin/activate'


def install_apt_get():
    """Installing |sudo apt-get|."""

    run('sudo apt-get update')
    run('sudo apt-get install software-properties-common '
        'python-software-properties python3-tk python3-dev')

    run('sudo add-apt-repository ppa:fkrull/deadsnakes')
    run('sudo apt-get update')
    run('sudo apt-get install python3.5')
    run('cd /usr/bin')
    run('sudo rm python3')
    run('sudo ln -s python3.5 python3')

    run('sudo pip install virtualenv')
    run('sudo apt-get install git python-pip python-virtualenv '
        'libssl-dev redis-server build-essential python3.5-dev '
        'libffi-dev gcc lxml nginx supervisor sqlite3')


def clone_the_project():
    """Clone the project from
    https://github.com/NaStyA128/final_project.git."""

    with cd('/vagrant'):
        run('git clone https://github.com/NaStyA128/final_project.git')


def create_env():
    """Create virtualenv (.env - python3.5, .env2 - python2.7)."""

    with cd('/vagrant'):
        with cd('final_project'):
            run('virtualenv -p /usr/bin/python3 .env')
            run('virtualenv -p /usr/bin/python .env2')


def install_requirements():
    """Installing requirements at the virtualenv."""

    with cd('/vagrant'):
        with cd('final_project'):
            with start_virtualenv3_5():
                run('pip install -r requirements.txt')

                run('sudo service nginx start')
                run('sudo cp /vagrant/final_project/django_project/django_project_nginx.conf /etc/nginx/sites-avialable/django_project_nginx.conf')
                run('sudo ln -s /etc/nginx/sites-available/django_project_nginx.conf /etc/nginx/sites-enabled/')
            with start_virtualenv2_7():
                run('pip install -r requirements2.txt')


@contextmanager
def start_virtualenv3_5():
    """Start virtualenv (python3.5)."""

    with cd(env.app_dir):
        with prefix(env.activate3_5):
            yield


@contextmanager
def start_virtualenv2_7():
    """Start virtualenv (python2.7)."""

    with cd(env.app_dir):
        with prefix(env.activate2_7):
            yield


def start_install():
    """Start function."""

    install_apt_get()
    clone_the_project()
    create_env()
    install_requirements()


# def restart_install():
#     clone_the_project()
#     install_requirements()


def virtualenv3_5():
    with start_virtualenv3_5():
        run('sudo service nginx start')
        run('uwsgi --ini django_project/django_project_uwsgi.ini -d uwsgi_logs.txt')
        run('supervisord -c supervisord.conf')


def virtualenv2_7():
    with start_virtualenv2_7():
        pass


def deploy():
    # run('vagrant reload --provision')
    # vagrant()
    # start_install()
    virtualenv3_5()
