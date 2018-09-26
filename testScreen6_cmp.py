import urwid

class BoxButton(urwid.WidgetWrap):
	_border_char = u'-'
	def __init__(self, label, on_press=None, user_data=None):
		padding_size = 2
		border = self._border_char * (len(label) + padding_size * 2)
		cursor_position = len(border) + padding_size
		
		self.top = u'\u250C' + border + u'\u2510\n'
		self.middle = u'│  ' + label + u'  │\n'
		self.bottom = u'\u2514' + border + u'\u2518'

		self.widget = urwid.Pile([
			urwid.Text(self.top[:-1]),
			urwid.AttrMap(urwid.SelectableIcon(self.middle[:-1], 3), 
				'unselected', focus_map='selected'),
			urwid.Text(self.bottom)
		])

		self.widget = urwid.Columns([(len(self.bottom), self.widget)])
		
		#self.widget = urwid.AttrMap(self.widget, '', 'selected')
		self._hidden_btn = urwid.Button('hidden %s' % label, on_press, user_data)

		super(BoxButton, self).__init__(self.widget)

	def selectable(self):
		return True

	def keypress(self, *args, **kw):
		return self._hidden_btn.keypress(*args, **kw)

	def mouse_event(self, *args, **kw):
		return self._hidden_btn.mouse_event(*args, **kw)

if __name__ == '__main__':
	header = urwid.Text(u'Discard')
	footer = urwid.Text(u'Created By Dave')
	# the only way to raise an Exception in lambda is through exec
	onclick = lambda x: exec('raise urwid.ExitMainLoop()')
	body = urwid.LineBox(urwid.Filler(
		urwid.Columns([BoxButton('OK', on_press=onclick), 
		BoxButton('Exit', on_press=onclick)])
	))
	palette = [
		('unselected', 'default', 'default'),
		('menu', '', 'dark blue', 'bold'),
		('action', 'standout', '')
	]
	app = urwid.MainLoop(urwid.Frame(header=header, body=body, footer=footer), palette=palette)
	app.run()
