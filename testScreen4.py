import urwid

class BoxButton(urwid.WidgetWrap):
	_border_char = u'-'
	padding_sizes = { 'sm' : 2 , 'lg' : 6 }
	btn_types = { 'menu': 'menu', 'action':'action' }
	def __init__(self, label, on_press=None, user_data=None, size='sm', btn_type='action'):
		border = self._border_char * (len(label) + self.padding_sizes[size] * 2)
		cursor_position = len(border) + self.padding_sizes[size]
		self.padding = self.padding_sizes[size] * ' '

		_inner_widgets = []
		self.top = u'\u250C' + border + u'\u2510\n'
		_inner_widgets.append(urwid.Text(self.top[:-1]))
		self.padding_line = u'|' + self.padding + len(label) * ' ' + self.padding + u'|'
		self.middle = u'|' + self.padding + label + self.padding + u'|'
		for  cnt in range((self.padding_sizes[size] // 2)):
			_inner_widgets.append(urwid.Text(self.padding_line))
		_inner_widgets.append(
			urwid.AttrMap(urwid.SelectableIcon(self.middle, 3),
				'unselected', focus_map=self.btn_types[btn_type]))
		for  cnt in range((self.padding_sizes[size] // 2)):
			_inner_widgets.append(urwid.Text(self.padding_line))
		self.bottom = u'\u2514' + border + u'\u2518\n'
		_inner_widgets.append(urwid.Text(self.bottom[:-1]))

		self.widget = urwid.Pile(_inner_widgets)

		self.widget = urwid.Columns([(len(self.padding_line), self.widget)])
		
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
		urwid.Columns([BoxButton('OK', on_press=onclick, size='lg', btn_type='menu'), 
		BoxButton('Exit', on_press=onclick)])
	))
	palette = [
		('unselected', 'default', 'default'),
		('menu', '', 'dark blue', 'bold'),
		('action', 'standout', '')
	]
	app = urwid.MainLoop(urwid.Frame(header=header, body=body, footer=footer), palette=palette)
	app.run()
