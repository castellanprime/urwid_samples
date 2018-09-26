# Pulled from a public gist https://gist.github.com/sphaero/8225315
# A ZeroMQ Event loop class for Urwid. This class inherits from the original 
# SelectEventLoop and replaces the filedescriptor polling with the ZeroMQ 
# methods.
# Author: Arnaud Loonstra <arnaud@sphaero.org>

import zmq
import time
import urwid

class ZmqEventLoop(urwid.SelectEventLoop):

    def __init__(self, ctx=zmq.Context(), *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._zctx = ctx
        self._zpoller = zmq.Poller()

    def watch_file(self, fd, callback):
        """
        Call callback() when fd has some data to read.  No parameters
        are passed to callback.
        Returns a handle that may be passed to remove_watch_file()
        fd -- file descriptor to watch for input
        callback -- function to call when input is available
        """
        self._watch_files[fd] = callback
        self._zpoller.register(fd, zmq.POLLIN)
        return fd
    
    def remove_watch_file(self, handle):
        """
        Remove an input file.
        Returns True if the input file exists, False otherwise
        """
        if handle in self._watch_files:
            self._zpoller.unregister(handle)
            del self._watch_files[handle]
            return True
        return False

    def run(self):
        """
        Start the event loop.  Exit the loop when any callback raises
        an exception.  If ExitMainLoop is raised, exit cleanly.
        """
        self._did_something = True
        while True:
            try:
                self._loop()
            except urwid.ExitMainLoop:
                break

    def _loop(self):
        """
        A single iteration of the event loop
        """
        if self._alarms or self._did_something:
            if self._alarms:
                tm = self._alarms[0][0]
                timeout = max(0, tm - time.time())
            if self._did_something and (not self._alarms or 
                    (self._alarms and timeout > 0)):
                timeout = 0
                tm = 'idle'
            items = dict(self._zpoller.poll(timeout))
        else:
            tm = None
            items = dict(self._zpoller.poll())

        if not items:
            if tm == 'idle':
                self._entering_idle()
                self._did_something = False
            elif tm is not None:
                # must have been a timeout
                tm, alarm_callback = self._alarms.pop(0)
                alarm_callback()
                self._did_something = True

        for fd, ev in items.items():
            if ev in (zmq.POLLIN, zmq.POLLOUT):
                self._watch_files[fd]()
                self._did_something = True
