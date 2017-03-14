from fabric.api import *
# Default release is 'current'
env.name = 'openparty'
env.release = 'current'
env.python_version = '2.7.2'


@task
def production():
    """Production server settings"""
    env.settings = 'production'
    env.user = 'openparty'
    env.path = '/home/%(user)s/sites/openparty-app' % env
    env.hosts = ['www.beijing-open-party.com']


@task
def setup():
    """
    Setup a fresh virtualenv and install everything we need so it's ready to deploy to
    """
    with activate_virtualenv():
        run('mkdir -p %(path)s; cd %(path)s; mkdir releases; mkdir shared;' % env)
        clone_repo()
        checkout_latest()
        install_requirements()


@task
def deploy():
    """Deploy the latest version of the site to the server and restart nginx"""
    with activate_virtualenv():
        checkout_latest()
        install_requirements()
        symlink_current_release()
        migrate()
        restart_server()


def clone_repo():
    """Do initial clone of the git repo"""
    run('cd %(path)s; git clone https://github.com/openparty/openparty.git repository' % env)


def checkout_latest():
    """Pull the latest code into the git repo and copy to a timestamped release directory"""
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')
    run("cd %(path)s/repository; git pull origin master" % env)
    run('cp -R %(path)s/repository %(path)s/releases/%(release)s; rm -rf %(path)s/releases/%(release)s/.git*' % env)


def install_requirements():
    """Install the required packages using pip"""
    """Pip need copy file into system folder, so we need a sudo"""
    run('cd %(path)s; pip install -r ./releases/%(release)s/requirements.txt' % env)


def symlink_current_release():
    """Symlink our current release, uploads and settings file"""
    with settings(warn_only=True):
        run('cd %(path)s; rm releases/previous; mv releases/current releases/previous;' % env)
    run('cd %(path)s; ln -s %(release)s releases/current' % env)
    """ production settings"""
    run('cd %(path)s/releases/current/; cp %(path)s/conf/local_settings.py local_settings.py' % env)
    run('cd %(path)s/releases/current/; cp %(path)s/conf/site-restart site-restart' % env)
    with settings(warn_only=True):
        run('cd %(path)s/releases/current/media; ln -s %(path)s/shared/post_images post_images' % env)
        run('cd %(path)s/releases/current/media; rm -rf upload; ln -s %(path)s/shared/upload upload' % env)
        run('cd %(path)s/releases/current/media; ln -s /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin .' %
            env)
        # run('rm %(path)s/shared/static' % env)
        # run('cd %(path)s/releases/current/static/; ln -s %(path)s/releases/%(release)s/static %(path)s/shared/static ' %env)


def migrate():
    """Run our migrations"""
    run('cd %(path)s/releases/current; python manage.py syncdb --noinput --migrate' % env)
    run('cd %(path)s/releases/current; python manage.py migrate --noinput core' % env)


def rollback():
    """
    Limited rollback capability. Simple loads the previously current
    version of the code. Rolling back again will swap between the two.
    """
    run('cd %(path)s; mv releases/current releases/_previous;' % env)
    run('cd %(path)s; mv releases/previous releases/current;' % env)
    run('cd %(path)s; mv releases/_previous releases/previous;' % env)
    restart_server()


@task
def restart_server():
    """Restart the web server"""
    with activate_virtualenv():
        run('cd %(path)s/releases/current; %(path)s/releases/current/site-restart' % env)
        sudo('/etc/init.d/nginx restart')


def activate_virtualenv():
    return prefix('PATH=/home/%(user)s/.pythonbrew/bin:$PATH source /home/%(user)s/.pythonbrew/etc/bashrc '\
        '&& pythonbrew use %(python_version)s && pythonbrew venv use %(name)s-%(settings)s' % env)


@task
def setup_pythonbrew():
    with prefix('PATH=/home/%(user)s/.pythonbrew/bin:$PATH source /home/%(user)s/.pythonbrew/etc/bashrc' % env):
        run('pythonbrew install %(python_version)s' % env)
        run('pythonbrew switch %(python_version)s' % env)
        run('pythonbrew symlink')
        run('pythonbrew venv init')


@task
def create_venv():
    with prefix('PATH=/home/%(user)s/.pythonbrew/bin:$PATH source /home/%(user)s/.pythonbrew/etc/bashrc && pythonbrew use %(python_version)s' % env):
        run('pythonbrew venv create %(name)s-%(settings)s' % env)
        run('pythonbrew venv use %(name)s-%(settings)s' % env)
