from kivy.config import Config
Config.set('graphics', 'resizable', False)
#Config.set('graphics', 'fullscreen', True)
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
#from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRectangleFlatButton

from Hirogone import Hirogone


class WindowManager(ScreenManager):
	def __init__(self, **kwargs):
		super(WindowManager, self).__init__(**kwargs)


class main(MDApp):
	def build(self):

		#Window.fullscreen = True
		kv = WindowManager()
		kv.add_widget(Builder.load_file("Hirogone.kv"))

		return kv


	def openDialog(self, title, text):
		def closeDialog(*args):
			dialog.dismiss()

		dialog = MDDialog(
			title=title,
			text=text,
			buttons=[
				MDRectangleFlatButton(
					text="Aceptar",
					on_press=closeDialog
				)
			]
		)
		dialog.open()


	def on_start(self):
		with open('dictEsp.txt', 'r', encoding='utf-8') as f:
			self.span_words = list(map(lambda s: s.replace('\n', ''), f.readlines()))


if __name__ == "__main__":
	main().run()
