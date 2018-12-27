import urwid
import sys, logging
from testScreen3 import ActionButton
from boxbutton import BoxButton

logger = logging.getLogger('')
logger.setLevel(logging.INFO)

fh = logging.FileHandler('run.log', 'w', 'utf-8')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(' - %(name)s - %(levelname)-8s: %(message)s')

fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

class LineBoxTest(urwid.WidgetWrap):
	def __init__(self):
		self.games = [dict(game_name='FireBolt', players=['Earl', 'Phineas', 'Tucker']),
			dict(game_name='FireBolt2', players=['Carlson', 'Ben', 'Kevlin'])
		]
		self._logger = logging.getLogger(__name__)
		self.players_pane = self.generate_pane_widget('players')
		self.game_pane = self.generate_pane_widget('game')
		# self._parent = parent
		self.status_box = urwid.Text(u'')
		middle_col = self.generate_middle_col()
		self.widgets = urwid.Pile([
			urwid.Columns([
				('weight', 3, self.game_pane),
				('weight', 2,  middle_col),
				('weight', 3, self.players_pane)
			]),
			urwid.Padding(
				urwid.Columns([
					('pack', self.status_box),
					('pack', BoxButton(u'Join', on_press=self.join_game))
				])
				, align='right'
			)
		])
		super().__init__(self.widgets)

	def generate_middle_col(self, *args, **kwargs):
		return urwid.Filler(
			urwid.Pile([
				BoxButton('+', on_press=self.add_player_to_game),
				BoxButton('-', on_press=self.remove_player_from_game)
			])
		)
            
	def join_game(self, *args, **kwargs):
		w = [widget.get_text() for widget in list(self.players_pane._original_widget._get_body())]
		if 'Mike' in w:
			self._logger.info('Found Mike')
		else:
			self.set_status_text(u'Need to add yourself in the game')
            
	def set_status_text(self, text, *args, **kwargs):
		self.status_box.set_text(text)
    
	def add_player_to_game(self, *args, **kwargs):
		self.players_pane._original_widget._get_body().append(urwid.Text('Mike'))
		if len(self.status_box.get_text()) != 0:
			self.set_status_text('')
		self._invalidate()
        
	def remove_player_from_game(self, *args, **kwargs):
		self.players_pane._original_widget._get_body().pop()
		self._invalidate()

	def generate_pane_widget(self, pane_type, *args, **kwargs):
		if pane_type == 'game':
			body = [urwid.Text(game.get('game_name')) for game in self.games]
			widget = urwid.SimpleFocusListWalker(body)
			widget.set_focus_changed_callback(lambda f: self.change_list_items(f))
			return urwid.LineBox(urwid.ListBox(widget))
		elif pane_type == 'players':
			body = [urwid.Text(player) for player in self.games[0].get('players')]
			return urwid.LineBox(urwid.ListBox(urwid.SimpleFocusListWalker(body)))

	def change_list_items(self, num, *args, **kwargs):
		body = [urwid.Text(player) for player in self.games[num].get('players')]
		self.players_pane._original_widget._set_body(urwid.SimpleFocusListWalker(body))
		self._invalidate()

if __name__ == '__main__':
	header = urwid.Text(u'Discard')
	footer = urwid.Text(u'Created By Dave')
	# the only way to raise an Exception in lambda is through exec
	onclick = lambda x: exec('raise urwid.ExitMainLoop()')
	games = [dict(game_name='FireBolt', players=['Earl', 'Phineas', 'Tucker']),
		dict(game_name='FireBolt2', players=['Carlson', 'Ben', 'Kevlin'])
	]
	r_body = [ActionButton(game.get('game_name')) for game in games]
	# r_body = [game.get('game_name') for game in games]
	widget = urwid.SimpleFocusListWalker(r_body)
	t_body = urwid.LineBox(urwid.BoxAdapter(urwid.ListBox(widget), len(r_body)))
	# body = urwid.Pile([
	#	('pack', urwid.Columns([('weight', 2, t_body), ('weight', 2, t_body)])),
	#	('pack', urwid.Padding(BoxButton('OK', on_press=onclick), align='right'))
	#])
	body = urwid.Columns([('pack', t_body), ('pack', t_body)])
	
	palette = [
		('unselected', 'default', 'default'),
		('menu', '', 'dark blue', 'bold'),
		('reversed', 'standout', '')
	]
	app = urwid.MainLoop(urwid.Frame(header=header, body=body, footer=footer), palette=palette)
	app.run()
