# supervisord doesn't have support for "dependencies", that is, we can't
# configure it to wait for another process to start. For airsonos, this is a
# minor problem because avahi needs dbus fully functioning, otherwise it'll
# have a false start.

import sys

from subprocess import call
from supervisor.childutils import listener

def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def main():
    while True:
        headers, body = listener.wait()
        body = dict([pair.split(":") for pair in body.split(" ")])

        if (
             headers["eventname"] == "PROCESS_STATE_RUNNING" and
             body["processname"] == "dbus"
           ):
            write_stderr("dbus is running, starting avahi\n")
            call(["supervisorctl", "start", "avahi"])
        listener.ok()

if __name__ == '__main__':
    main()
