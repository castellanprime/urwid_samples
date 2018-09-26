import urwid

class ActionButton(urwid.Button):
	def __init__(self, caption, callback=None):
		super(ActionButton, self).__init__("")
		urwid.connect_signal(self, 'click', callback)
		self._w = urwid.AttrMap(urwid.SelectableIcon(caption, 2), None, focus_map='reversed')		

class App(object):
	def __init__(self):
		self.bodies = { 'landingPage' : self.landing_page }
		self.set_current_page('landingPage')
		self.frame = self.get_frame()
		self.palette = [
			('titlebar', 'dark red', ''),
			('footer', 'dark green', ''),
			('reversed', 'standout', '')
		]	
		self.loop = urwid.MainLoop(self.frame, palette=self.palette)	

	def set_current_page(self, page):
		self.page = page

	def landing_page(self):
		body = []
		body.append(urwid.Divider())
		button = ActionButton('> Enter the Game Lobby')
		body.append(button)
		body.append(urwid.Divider())
		button = ActionButton('> Exit Game', self.exit_program)
		body.append(button)
		return urwid.LineBox(urwid.Columns(
			urwid.ListBox(urwid.SimpleFocusListWalker(body)), valign='middle'))
	
	def get_frame(self):
		header_text = urwid.Text(u'Discard')
		header = urwid.AttrMap(header_text, 'titlebar')
		footer_text = urwid.Text(u'Created by Dave', align='right')
		footer = urwid.AttrMap(footer_text, 'footer')
		body = self.bodies[self.page]()
		return urwid.Frame(header=header, body=body, footer=footer) 
	
	def run(self):
		self.loop.run()

	def exit_program(self):
		raise urwid.ExitMainLoop()
	
if __name__ == '__main__':
	app = App()
	app.run()
