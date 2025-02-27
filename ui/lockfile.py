# coding=utf-8
# ##################################################### #
#                                                       #
# This is BashStyle-NG                                  #
#                                                       #
# Licensed under GNU GENERAL PUBLIC LICENSE v3          #
#                                                       #
# Copyright Christopher Roy Bratušek                    #
#                                                       #
# ##################################################### #

MODULES = ['os', 'os.path', 'string', 'sys', 'subprocess']
FAILED = []

for module in MODULES:
    try:
        globals()[module] = __import__(module)
    except ImportError:
        FAILED.append(module)

if FAILED:
    print(_("The following modules failed to import: %s")
          % (" ".join(FAILED)))
    sys.exit(1)

lockfile = os.path.expanduser("~/.bashstyle.lock")


class LockFile(object):
    def Check(self):
        if os.access(lockfile, os.F_OK):
            rlockfile = open(lockfile, "r")
            rlockfile.seek(0)
            oldpid = rlockfile.readline()
            if os.path.exists("/proc/%s" % oldpid):
                if sys.version_info[0] == 2:
                    xpid = commands.getoutput("pgrep -l bashstyle")
                    gpid = string.split(xpid)
                else:
                    xpid = subprocess.getoutput("pgrep -l bashstyle")
                    gpid = xpid.split()
                if gpid[1] == "bashstyle":
                    print(
                          _("Lockfile does exist and bashstyle-ng is \
already running.\
\
bashstyle-ng is running as process %s" % oldpid)
                    )
                    sys.exit(1)
                else:
                    print(
                          _("Lockfile does exist but the process with \
that pid is not\
\
bashstyle, removing lockfile of old process: %s" % oldpid)
                    )
                    os.remove(lockfile)
            else:
                print(
                      _("Lockfile does exist but the process with that \
pid is no\
\
longer running, removing lockfile of old process: %s" % oldpid)
                    )
                os.remove(lockfile)
        else:
            print(_("Lockfile does not exist"))

    def Write(self):
        if not os.access(lockfile, os.F_OK):
            wlockfile = open(lockfile, "w")
            wlockfile.write("%s" % os.getpid())
            wlockfile.close

    def Remove(self):
        if os.access(lockfile, os.F_OK):
            os.remove(lockfile)
