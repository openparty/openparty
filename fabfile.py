from fabric import task


env = {
    "user": "openparty",
    "python_version": "3.9.9",
    "release": "current",
    "release_branch": "master",
    "environment": "production",
    "home_path": "/home/public_html/openparty-app",
    "releases": "releases",
}

op_hosts = ["openparty@beijing-open-party.com"]


def hostname(c):
    c.run("echo running at $(hostname)")


@task(hosts=op_hosts)
def setup(c):
    hostname(c)
    """
    Setup a fresh virtualenv and install everything we need so it's ready to deploy to
    """
    activate_pyenv(c)
    c.run("mkdir -p %(home_path)s; cd %(home_path)s; mkdir releases; mkdir shared;" % env)
    clone_repo(c)
    checkout_latest(c)
    install_requirements(c)


# pipenv run fab deploy
@task(hosts=op_hosts)
def deploy(c):
    """Deploy the latest version of the site to the server and restart nginx"""
    activate_pyenv(c)
    checkout_latest(c)
    install_requirements(c)
    symlink_current_release(c)
    migrate(c)
    restart_server(c)


def clone_repo(c):
    hostname(c)
    """Do initial clone of the git repo"""
    c.run("cd %(home_path)s; git clone https://github.com/openparty/openparty.git repository" % env)


@task(hosts=op_hosts)
def checkout_latest(c):
    print("checkout_latest")
    hostname(c)
    """Pull the latest code into the git repo and copy to a timestamped release directory"""

    with c.cd("%(home_path)s/repository" % env):
        c.run("git checkout %(release_branch)s" % env)
        c.run("git pull origin %(release_branch)s" % env)
        env["release"] = c.run("git rev-parse HEAD").stdout.strip()

    if c.run("ls %(home_path)s/releases/%(release)s" % env, warn=True):
        print("release folder already exists, skip the checkout-release step.")
    else:
        c.run("cp -R %(home_path)s/repository %(home_path)s/releases/%(release)s;" % env)
        c.run("rm -rf %(home_path)s/releases/%(release)s/.git*" % env)


def install_requirements(c):
    print("install_requirements")
    with c.cd("%(home_path)s/releases/%(release)s" % env):
        c.run("PIPENV_VENV_IN_PROJECT=enabled pipenv install" % env)


def symlink_current_release(c):
    print("symlink_current_release")
    """Symlink our current release, uploads and settings file"""
    # if c.run("ls %(home_path)s/releases/previous" % env, warn=True):
    #     c.run("rm -rf %(home_path)s/releases/previous" % env, warn=True)
    # if c.run("ls %(home_path)s/releases/current" % env, warn=True):
    #     c.run("mv %(home_path)s/releases/current %(home_path)s/releases/previous" % env, warn=True)
    print("ln -s %(home_path)s/releases/%(release)s %(home_path)s/releases/current" % env)
    c.run("ln -s %(home_path)s/releases/%(release)s %(home_path)s/releases/current" % env, warn=True)

    c.run("cp %(home_path)s/conf/local_settings.py %(home_path)s/releases/current/local_settings.py" % env, warn=True)
    c.run("cp %(home_path)s/conf/site-restart %(home_path)s/releases/current/site-restart" % env, warn=True)

    c.run("ln -s %(home_path)s/shared/post_images %(home_path)s/releases/current/media/post_images" % env, warn=True)
    c.run("rm -rf %(home_path)s/releases/current/media/upload" % env, warn=True)
    c.run("ln -s %(home_path)s/shared/upload %(home_path)s/releases/current/media/upload" % env, warn=True)
    # c.run(
    #     "cd %(home_path)s/releases/current/media; ln -s /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin ."
    #     % env
    # )
    # run('rm %(home_path)s/shared/static' % env)
    # run('cd %(home_path)s/releases/current/static/; ln -s %(home_path)s/releases/%(release)s/static %(home_path)s/shared/static ' %env)


def migrate(c):
    print("migrate")
    """Run our migrations"""
    # I need to fix the south -> django database change first
    # with c.cd("%(home_path)s/releases/%(release)s" % env):
    #     c.run("pipenv run python manage.py migrate --noinput" % env)


# def rollback(c):
#     print("rollback")
#     """
#     Limited rollback capability. Simple loads the previously current
#     version of the code. Rolling back again will swap between the two.
#     """
#     c.run("cd %(home_path)s; mv releases/current releases/_previous;" % env)
#     c.run("cd %(home_path)s; mv releases/previous releases/current;" % env)
#     c.run("cd %(home_path)s; mv releases/_previous releases/previous;" % env)
#     restart_server()


def kill_current_cgi_process(c):
    print("kill_current_cgi_process")
    c.run("kill -9 `ps aux|grep python|grep gunicorn|awk '{print $2}'`", warn=True)


def start_cgi_process(c):
    print("start_cgi_process")
    with c.cd("%(home_path)s/%(releases)s/current" % env):
        c.run("PIPENV_VENV_IN_PROJECT=enabled pipenv run gunicorn -c gunicorn_config.py" % env)


@task(hosts=op_hosts)
def restart_server(c):
    print("restart_server")
    """Restart the web server"""
    activate_pyenv(c)
    prepare_gunicorn(c)
    kill_current_cgi_process(c)
    start_cgi_process(c)
    c.sudo("service nginx restart")


def prepare_gunicorn(c):
    c.sudo("mkdir -p /var/{log,run}/gunicorn")
    c.sudo("chown openparty:openparty /var/{log,run}/gunicorn")


def activate_pyenv(c):
    c.run(
        "export PATH=%(home_path)s/.pyenv/shims:%(home_path)s/.pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
        % env
    )


@task(hosts=op_hosts)
def setup_python(c):
    print("setup_python")
    c.run("rm -rf %(home_path)s/.pyenv || true" % env)
    c.run("curl https://pyenv.run | bash")
    # this only affect interactive shell
    c.run("echo 'export PYENV_ROOT=\"$HOME/.pyenv\"' >> ~/.bashrc")
    c.run("echo 'export PATH=\"$PYENV_ROOT/bin:$PATH\"' >> ~/.bashrc")
    c.run("echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval \"$(pyenv init -)\"\nfi' >> ~/.bashrc")
    activate_pyenv(c)
    c.run("pyenv install %(python_version)s" % env)
    c.run("pyenv global %(python_version)s" % env)


@task(hosts=op_hosts)
def setup_venv(c):
    print("setup_venv")
    activate_pyenv(c)
    c.run("pip install --upgrade pip")
    c.run("pip install pipenv setuptools")
    with c.cd("%(home_path)s/%(releases)s/%(release)s" % env):
        c.run("PIPENV_VENV_IN_PROJECT=enabled pipenv --python %(python_version)s" % env)
        c.run("PIPENV_VENV_IN_PROJECT=enabled pipenv install")
