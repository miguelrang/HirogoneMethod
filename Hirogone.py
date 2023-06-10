from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel

import matplotlib.colors as mcolors
from random import randint as rand
import re


class Suggestion(MDLabel):
	text = StringProperty()


class Hirogone(Screen):
	def __init__(self, **kwargs):
		super(Hirogone, self).__init__(**kwargs)
		global app
		app = MDApp.get_running_app()


	def onTextNumbs(self, field:object, text:str):
		"""	We validate the user is wrating a valid number
		Args:
			field (object): Field the user is editing
			text (str): field text
		"""
		field.text = text.replace(' ', '')
		if field.text != '':
			invalid_char = False
			groups = text.replace('-', '')
			for char in groups:
				if not char.isnumeric():
					text = text.replace(char, '')
					invalid_char = True

			if invalid_char:
				app.openDialog(
					title='Advertencia',
					text='Has agregado un caracter invalido.',
				)
			field.text = text

	def validNum(self, text:str) -> bool:
		"""	When the user press the button we validate the
			number is correct.
		Args:
			text (str): Number (Ej. 35-928-1290)
		Returns:
			bool: True= Number is valid False=Not valid
		"""
		correct = True
		validation = re.compile(r'(([0-9][0-9]|[0-9][0-9]-)|([0-9][0-9][0-9]|[0-9][0-9][0-9]-)|([0-9][0-9][0-9][0-9]|[0-9][0-9][0-9][0-9]-))+')
		if validation.fullmatch(text):
			if text[len(text)-1] == '-':
				app.openDialog(
					title='Error',
					text='Tu número no es valido. Verifica que no haya agregado un caracter invalido.'
				)
				correct = False
		else:
			app.openDialog(
				title="Error",
				text='El número no cumple con el formato solicitado (Ejemplo: 32/32-59/325-982/3259-8215/32-59-82-15...).'
			)
			correct = False

		return correct


	def validInputs(self, this:object, one:str=None, two:str=None, three:str=None, four:str=None, five:str=None, six:str=None, seven:str=None, eight:str=None, nine:str=None, zero:str=None):
		"""	We validate the keys addes by the user.
		Args:
			this (object): The actual text input the user is editing.
			one (str|None): TextInput value (when the user is editing)|None (when text input unfocus)
			.
			.
			.
		"""
		if this.text != '':
			if this.focus == False:
				letters:list = this.text.split('-')
				all_letters:str = f"{one}-{two}-{three}-{four}-{five}-{six}-{seven}-{eight}-{nine}-{zero}"
				all_letters:list = all_letters.split('-')
				for x in this.text.split('-'):
					try:
						all_letters.remove(x)
					except:
						pass
				#print(all_letters)
				
				invalids:list = []
				for letter in letters.copy():
					if letter in all_letters: letters.remove(letter), invalids.append(letter) 

				if invalids: app.openDialog(
					title='Aviso',
					text='\'{}\' Ya está(n) en en otro campo'.format(', '.join(invalids))
				)
				this.text = '-'.join(letters)
			elif one == None:
				this.text = this.text.upper().replace(' ', '').replace('--', '')

				validation = re.compile(r'([A-Z]-|-[A-Z]|[A-Z])+')
				if not validation.fullmatch(this.text):
					for char in this.text.split('-'):
						if char not in '-ABCHDEFGIJKLLMNÑOPQRSTUVWXYZ':
							if char != '':
								this.text = this.text.replace(char, char[0])
				
				else:
					text = this.text.split('-')
					for char in text.copy():
						if char != '':
							if text.count(char) > 1:
								text.remove(char)
								this.text = '-'.join(text)

							elif len(char) == 2 and char not in ['CH','LL']:
								this.text = this.text.replace(char, char[0])

							elif char in ['A','E','I','O','U']:
								this.text = this.text.replace(char, '')


	def generateWords(self, keys:dict, num:list):
		"""	Generate the words for the numbers taking the inputs keys.
		Args:
			keys (dict): Inputs keys (Ej. '1': 'R-RR'...)
			num (list): Number added by the user converted to list (Ej. ['325','290'...])
		"""
		span_words = app.span_words
		self.ids.recycle.data = []
		values:dict = {}
		for x in num:  # Example num = ['42', '9104', '3377'] -> x = 42/9104/3377
			nums = list(x)
			word = '(?:a|e|i|o|u)*'
			for y in nums:  # Example nums = ['4', '2'] -> y = 4/2
				word += '{}(?:a|e|i|o|u)*'.format(f"(?:{keys[str(y)].lower().replace('-', '|')})")
				#print(word)
			
			validation = re.compile(fr'\b{word}\b')
			found:list = validation.findall(', '.join(span_words))
			if found:
				values[x] = found

			else: # not found
				app.openDialog(
					title='Sin coincidencias',
					text='Lo sentimos, no pudimos encontrar una coincidencia para: {}. Por favor, intente agrupando de otra manera.'.format(x)
				)
				values = {}
				break

		#print(values)
		if values:
			n = 1
			for num in values.keys():  # Ex. num = 32
				r = rand(0, 255)
				g = rand(0, 255)
				b = rand(0, 255)
				color = mcolors.rgb2hex((r/255, g/255, b/255, 1))
				for value in values[num]:  # Ex. values[num] = ['v1', 'v2',...] -> value = 'v1'/'v2'/...
					self.ids.recycle.data.append(
						{
							"viewclass": "Suggestion",
							"text": "[b]{}[/b]: [color=#B02907]{}[/color]->[color={}]{}[/color]".format(n, num, color, value),
						}
					)
					n += 1

