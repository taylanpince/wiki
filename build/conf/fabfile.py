from __future__ import with_statement

from fabric.api import *
from fabric.contrib.console import confirm


env.remote_dir = "/home/taylan/sites/wiki"
env.hosts = [
    "67.23.4.212",
]


def pack(hash="HEAD"):
    # Create a temporary local directory, export the given commit using git archive
    local("mkdir ../../tmp", capture=False)
    local("cd ../../ && git archive --format=tar --prefix=deploy/ %s build/conf build/lib build/src build/wiki | gzip > tmp/archive.tar.gz" % hash, capture=False)
    
    # Untar the archive to minify js files
    # local("cd ../tmp; tar -xzf archive.tar.gz; rm -f archive.tar.gz", capture=False)
    # local("python /usr/local/lib/yuicompressor/bin/jsminify.py --dir=../tmp/deploy/build/taylanpince/media/js", capture=False)
    
    # Tarball the release again
    # local("cd ../tmp; tar -cf archive.tar deploy; gzip archive.tar")


def deploy():
    # Upload the archive to the server
    put("../../tmp/archive.tar.gz", "%(remote_dir)s/archive.tar.gz" % env)
    
    with cd(env.remote_dir):
        # Extract the files from the archive, remove the file
        run("tar -xzf archive.tar.gz")
        run("rm -f archive.tar.gz")
        
        # Move directories out of the build folder and get rid of it
        run("mv deploy/build/* deploy/")
        run("rm -rf deploy/build")
        
        # Create a symlink for the Django settings file
        with cd("deploy/wiki"):
            run("ln -s ../conf/settings.py settings_local.py")
        
        # Move the uploaded files directory from the active version to the new version, create a symlink
        # run("mv app/files deploy/files")
        
        # with cd("deploy/taylanpince/media"):
        #     run("ln -s ../../files")
        
        # Remove the active version of the app and move the new one in its place
        run("rm -rf app")
        run("mv deploy app")
    
    # Sync the database
    run("cd %(remote_dir)s/app/wiki; export PYTHONPATH=../lib; ./manage.py syncdb" % env)
    
    # Restart Apache
    sudo("/etc/init.d/apache2 restart")
    
    # Remove the temporary local directory
    local("rm -rf ../../tmp", capture=False)
