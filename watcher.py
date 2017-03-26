import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class ScriptModifiedHandler(PatternMatchingEventHandler):
    patterns = ['*.py']

    def __init__(self):
        super(ScriptModifiedHandler, self).__init__()
		# you can add some init code here

    def process(self, event):
        print(event.src_path, event.event_type)

    def on_modified(self, event):
        self.process(event)
		
	def on_moved(self, event):
		pass
		
	def on_deleted(self, event):
		pass
		
	def on_created(self, event):
		pass


if __name__ == '__main__':
    observer = Observer()
    path = '.'
    event_handler = ScriptModifiedHandler()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
   
