import urwid
import datetime
from boxbutton import BoxButton

LANDING_PAGE = 'LANDING_PAGE'
MAIN_MENU = 'MAIN_MENU'
NEW_GAME_PAGE = 'NEW_GAME_PAGE'
PLAYER_LOBBY = 'PLAYER_LOBBY'
PLAYER_GAME_PAGE = 'PLAYER_GAME_PAGE'

class FormControl(urwid.WidgetWrap):
	_border_char = u'-'
	def __init__(self, label, isPassword=False):
		_inner_widgets = []
		self.label = urwid.Text(label)
		self.edit, self.checkbox = None, None
		self.border = self._border_char * 15
		if isPassword:
			self.checkbox = urwid.CheckBox(label=u'Hide Characters', state=False)
			urwid.connect_signal(self.checkbox, 'change', self.unhide_chars)
			self.edit = urwid.Edit(mask=u'*')
		else:
			self.edit = urwid.Edit()
		_inner_widgets.append(self.label)
		_inner_widgets.append(urwid.Divider())
		_inner_widgets.append(self.edit)
		_inner_widgets.append(self.border)
		if isPassword:
			_inner_widgets.append(self.checkbox)
		self.widget = urwid.Pile(_inner_widgets)
		self.widget = urwid.Columns([(len(self.border), self.widget)])
		super().__init__(self.widget)

	def selectable(self):
		return True

	def unhide_chars(self):
		if self.checkbox.get_state() == False:
			self.edit.set_mask(None)
		else:
			self.edit.set_mask(u'*')
	
	def keypress(self, size, key):
		return key

	def mouse_event(self, *args):
		return True
		
class FormControlEdit(urwid.WidgetWrap):
	def __init__(self, label, label_width=15, input_width=30, next_callback=None
		, isPassword=False):
		self.label, self.next_callback = label, next_callback
		self._edit = None
		if isPassword:
			self._edit= urwid.Edit(mask=u'*')
		else:
			self._edit = urwid.Edit(mask=None)
		self.edit = urwid.Padding(self._edit, left=1, right=1)
		label = urwid.LineBox(
			urwid.Text(label),
			tlcorner = ' ',
			tline = ' ',
			lline = ' ',
			trcorner = ' ',
			blcorner = ' ',
			rline = ' ',
			brcorner = ' ',
			bline = ' ')
		lbox = urwid.AttrMap(
			urwid.LineBox(
			self.edit,
			tlcorner = ' ',
			tline = ' ',
			lline = ' ',
			trcorner = ' ',
			blcorner = ' ',
			rline = ' ',
			brcorner = ' '),
			'input',
			'input focus'
		)
		cols = None
		if isPassword:
			self.checkbox = urwid.CheckBox(u'Hide Chars', state=True)
			urwid.connect_signal(self.checkbox, 'postchange', self.unhide_chars, self._edit)
			cols = urwid.Pile([
				urwid.Columns([(label_width, label)]),
				urwid.Columns([(input_width, lbox)]),
				self.checkbox
			]) 
		else:
			cols = urwid.Pile([
				urwid.Columns([(label_width, label)]),
				urwid.Columns([(input_width, lbox)])
			])
		super().__init__(cols)

	def get_text(self):
		return self.edit.original_widget.get_text()[0]
	
	def unhide_chars(self, size, key, widget):
		text = widget.get_edit_text()
		if self.checkbox.get_state() == False:
				widget.set_mask(mask=None)
				widget.set_edit_text(text)
		else:
				widget.set_edit_text(text)
				widget.set_mask(mask=u'*')

	def get_label(self):
		return self.label

	def keypress(self, size, key):
		if key is 'enter' and self.next_callback:
			self.next_callback()
		else:
			return super().keypress(size, key)

class LandingPage(urwid.WidgetWrap):
	def __init__(self, parent):
		self.usernameBox = FormControlEdit('Username')
		self.passwordBox = FormControlEdit('Password', isPassword=True)
		self.user_data = [self.usernameBox, self.passwordBox]
		self.anonymousBtn = BoxButton('Anonymous User', on_press=self.create_anon_user,
			btn_type='action', user_data=self.user_data)
		self.loginBtn = BoxButton('Login', on_press=self.login, btn_type='action',
			user_data=self.user_data)
		self.registerBtn = BoxButton('Register', on_press=self.register, btn_type='action',
			user_data=self.user_data)
		self.exitBtn = BoxButton('Exit', on_press=self.exit_app, btn_type='action')
		self.user_data_widgets = urwid.Pile(self.user_data)
		self.form_buttons = urwid.Columns([
			self.anonymousBtn, self.loginBtn, self.registerBtn, self.exitBtn
		])
		self.error_text = urwid.Text('')
		self.form_widgets = urwid.Pile([
			urwid.Padding(urwid.BigText('Sign In', urwid.Thin3x3Font()), width='clip'),
			self.user_data_widgets,
			urwid.Divider(),
			urwid.Divider(),
			self.form_buttons,
			self.error_text
		])
		self.form_widgets = urwid.Filler(urwid.Padding(self.form_widgets, left=4, right=4))
		self._parent = parent
		super().__init__(self.form_widgets)

		# User creds
		self.username, self.password = None, None

	def get_username_text(self):
		return self.usernameBox.get_text()

	def create_anon_user(self, *args, **kwargs):
		self._parent.go_to_pane(MAIN_MENU)

	def login(self, *args, **kwargs):
		pass

	def register(self, *args, **kwargs):
		pass

	def exit_app(self, *args, **kwargs):
		self._parent.exit_app(*args, **kwargs)

class MainMenuPage(urwid.WidgetWrap):
	def __init__(self, parent):
		self.new_game_btn = BoxButton('New Game', on_press=self.create_new_game,
			size='lg')
		self.join_game_btn = BoxButton('Join Game', on_press=self.join_game,
			size='lg')
		self.save_game_btn = BoxButton('Save Game', on_press=self.save_game,
			size='lg')
		self.load_game_btn = BoxButton('Load Game', on_press=self.load_game,
			size='lg')
		self.show_help_btn = BoxButton('Show Help', on_press=self.show_help,
			size='lg')
		self.exit_game_btn = BoxButton('Exit Game', on_press=self.exit_game,
			size='lg') 
		self.btn_list = urwid.Filler(
			urwid.GridFlow(
				[
					self.new_game_btn, self.join_game_btn, self.save_game_btn,
					self.load_game_btn, self.show_help_btn,  self.exit_game_btn
				],
				cell_width=30,
				h_sep=10,
				v_sep=2,
				align='center'
			),				
			valign='middle'
		)
		self._parent = parent
		super().__init__(self.btn_list)

	def create_new_game(self, *args, **kwargs):
		self._parent.go_to_pane(NEW_GAME_PAGE)

	def join_game(self):
		self._parent.go_to_pane(PLAYER_LOBBY)

	def save_game(self):
		pass

	def load_game(self):
		pass

	def show_help(self):
		pass

	def exit_game(self, *args, **kwargs):
		self._parent.exit_app(*args, **kwargs)

class NewGamePage(urwid.WidgetWrap):
	def __init__(self, parent):
		self.game_name_box = FormControlEdit('Name of game')
		self.number_of_players_box = FormControlEdit('Number of players')
		self.create_btn = BoxButton('Create', on_press=self.create_game)
		self._parent = parent
		self.widgets = urwid.Filler(
			urwid.Padding(
				urwid.Pile([
					self.game_name_box, self.number_of_players_box, self.create_btn
				])
				,
				left=8,
				right=8
			)
		)
		super().__init__(self.widgets)

	def get_game_name(self, *args, **kwargs):
		return self.game_name_box.get_text()

	def get_number_of_players(self, *args, **kwargs):
		return self.number_of_players_box.get_text()

	def create_game(self, *args, **kwargs):
		self._parent.go_to_pane(PLAYER_LOBBY)

# This is where the error is
class PlayerLobby(urwid.WidgetWrap):
	def __init__(self, parent):
		self.games = [dict(game_name='FireBolt', players=['Earl', 'Phineas', 'Tucker']),
			dict(game_name='FireBolt2', players=['Carlson', 'Ben', 'Kevlin'])
		]
		self.players_pane = self.generate_pane_widget('players')
		self.game_pane = self.generate_pane_widget('game')
		self._parent = parent
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
			self._parent.go_to_pane(PLAYER_GAME_PAGE)
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

class PlayerGamePage(urwid.WidgetWrap):
	pass

class Window(urwid.Frame):

	def __init__(self):
		self.usernameText = urwid.Text(u'Mine')
		self.clock = urwid.Text(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		self.header = urwid.Columns([urwid.Text(u'Discard'), self.usernameText])
		self.footer = urwid.Columns([urwid.Text(u'Created by Dave'), urwid.Padding(self.clock, align='right')])

		# list of panes
		# these panes are useful to determine where the user goes next, ie how to set the body
		self.panes = dict(
			LANDING_PAGE=LandingPage(self),
			MAIN_MENU=MainMenuPage(self),
			NEW_GAME_PAGE=NewGamePage(self),
			PLAYER_LOBBY=PlayerLobby(self),
			# PLAYER_GAME_PAGE=PlayerGamePage(self)
		)
		self.body = urwid.LineBox(self.panes.get(LANDING_PAGE))
		super().__init__(header=self.header, body=self.body, footer=self.footer)

	def refresh_timer(self, loop, data):
		self.clock.set_text(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		loop.set_alarm_in(1, self.refresh_timer)

	def go_to_pane(self, pane):
		self.body = urwid.LineBox(self.panes.get(pane))
		if pane == MAIN_MENU:
			self.usernameText.set_text(self.panes.get(LANDING_PAGE).get_username_text())
		self._invalidate()

	def exit_app(self, *args, **kwargs):
		raise urwid.ExitMainLoop()

if __name__ == '__main__':
	# header = urwid.Text(u'Discard')
	# footer = urwid.Text('u Created by Dave')
	# onclick = lambda x: exec('raise urwid.ExitMainLoop()')
	# #body = urwid.LineBox(urwid.Filler(
	# #	FormControlEdit('Username', next_callback=onclick)
	# #))
	# body = urwid.LineBox(Form())
	window = Window()
	app = urwid.MainLoop(window)
	app.set_alarm_in(1, window.refresh_timer, app)
	app.run()
