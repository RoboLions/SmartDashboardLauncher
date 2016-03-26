import argparse
import os
import platform
import sys
import Tkinter as Tk
from subprocess import Popen
from networktables import NetworkTable

DEFAULT_SERVER = 'roboRIO-1261-FRC.local'
DEFAULT_TABLE = 'SmartDashboard'
COMMAND_LINE = ['java', '-jar', os.path.join(os.path.expanduser('~'), 'wpilib', 'tools', 'SmartDashboard.jar')]
COMMAND_NAME = 'SmartDashboard'
WINDOW_TITLE = 'Launcher'

LOOP_INTERVAL = 1

MESSAGES = {
    'INITIALIZE': u'Starting\u2026',
    'CONNECTING': u'Connecting to {0}\u2026',
    'WAITING':    u'Waiting for table "{1}"\u2026',
    'LAUNCHING':  u'Launching {2}\u2026'
}

def init():
    parser = argparse.ArgumentParser(
        description='A launcher that waits for a particular NetworkTable before launching SmartDashboard.',
    )
    parser.add_argument('server', nargs='?', default=DEFAULT_SERVER,
        help='The hostname or IP address of the NetworkTables server. Defaults to {0}.'.format(DEFAULT_SERVER)
    )
    parser.add_argument('table', nargs='?', default=DEFAULT_TABLE,
        help='The NetworkTables table to watch. Defaults to {0}.'.format(DEFAULT_TABLE)
    )
    args = parser.parse_args()

    server = args.server
    table = args.table

    NetworkTable.setIPAddress(server)
    NetworkTable.setClientMode()
    NetworkTable.initialize()

    root = Tk.Tk()
    app = App(root, server, table)
    root.mainloop()

class App:
    def __init__(self, parent, server, table):
        self.networktable = NetworkTable.getTable('')
	self.table = table

        self.messages = {k: v.format(server, table, COMMAND_NAME) for k, v in MESSAGES.iteritems()}

        self.root = parent
        self.root.title(WINDOW_TITLE)
        self.frame = Tk.Frame(self.root)
        self.frame.pack()
        self.progress = Tk.Label(self.frame, text=self.messages['INITIALIZE'])
        self.progress.pack()
        self.root.after(LOOP_INTERVAL, self.main)

    def main(self):
        if not self.networktable.isConnected():
            self.progress.configure(text=self.messages['CONNECTING'])
        elif not self.networktable.containsSubTable(self.table):
            self.progress.configure(text=self.messages['WAITING'])
        else:
            self.progress.configure(text=self.messages['LAUNCHING'])
            popen_kwargs = {}
            if platform.system() == 'Windows':
                # From http://msdn.microsoft.com/en-us/library/windows/desktop/ms684863%28v=vs.85%29.aspx
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                DETACHED_PROCESS = 0x00000008
                popen_kwargs.update(creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)
            else:
                popen_kwargs.update(preexec_fn=os.setsid)
            Popen(COMMAND_LINE, **popen_kwargs)
            self.frame.quit()
            return
        self.root.after(LOOP_INTERVAL, self.main)

if __name__ == '__main__':
    init()
