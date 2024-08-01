

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
import django
django.setup()

from utils.control.ssh import SSHInterface
from apps.term.models import Session

def main():
    session = Session.objects.get(pk=25)
    auth = session.content_object.auth
    mgt_ip = session.content_object.mgt_ip
    ssh = SSHInterface(mgt_ip, auth)
    ssh.run(
        actions=['ls --color=auto', 'uname -a', 'sleep ', 'echo -e ddd', 'uname -a', 'htop'],
    )

if __name__ == "__main__":
    main()
