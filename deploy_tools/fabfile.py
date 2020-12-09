import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run
from fabric.context_managers import shell_env

REPO_URL = 'https://github.com/jonabadie/superlists.git'


def _get_latest_source():
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'git reset --hard {current_commit}')


def _update_virtualenv():
    if not exists('venv/bin/pip'):
        run(f'python3.7 -m venv venv')
    run(f'./venv/bin/pip install -r requirements.txt')


def _secret_key():
    return ''.join(random.SystemRandom().choices(
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))


def _create_or_update_dotenv():
    append('.env', 'DEBUG=False')
    append('.env', f'SITE_NAME={env.host}')
    env_content = run('cat .env')
    if 'SECRET_KEY' not in env_content:
        new_secret = _secret_key()
        append('.env', f'SECRET_KEY={new_secret}')


def _update_static_file():
    with shell_env(SECRET_KEY=_secret_key()):
        run('./venv/bin/python manage.py collectstatic --noinput')


def _update_database():
    with shell_env(SECRET_KEY=_secret_key()):
        run('./venv/bin/python manage.py migrate --noinput')


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_file()
        _update_database()