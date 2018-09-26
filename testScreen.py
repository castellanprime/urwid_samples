import urwid
from testScreen4 import BoxButton
from UrwidZMQ import ZmqEventLoop
choices = ['Chapman', 'Clesse', 'Gilliam', 'Idle', 'Jones', 'Palin']

palette = [
	('reversed', 'standout', ''),
	('highlight', 'black', 'dark blue'),
	('unselected', 'default', 'default'),
	('selected', 'standout', 'default', 'bold')
]


def menu(title, choices):
	body = [urwid.Text(title), urwid.Divider()]
	for c in choices:
		button = BoxButton(c, on_press=item_chosen, user_data=c)
		#urwid.connect_signal(button, 'click', item_chosen, c)
		body.append(urwid.AttrMap(button, None, focus_map='reversed'))
	return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button,choice):
	response = urwid.Text([u'You chose ', choice, u'\n'])
	done = urwid.Button(u'Ok')
	urwid.connect_signal(done, 'click', exit_program)
	main.original_widget = urwid.Filler(urwid.Pile([response,
		urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
	raise urwid.ExitMainLoop()

main = urwid.Padding(menu(u'Pythons', choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
	align='center', width=('relative', 60),
	valign='middle', height=('relative', 60),
	min_width=20, min_height=9)


urwid.MainLoop(top, palette=palette, event_loop=ZmqEventLoop()).run()
