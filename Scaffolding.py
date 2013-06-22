import sublime
import sublime_plugin

class ScaffoldingCommand(sublime_plugin.WindowCommand):
	def run(self, paths = [], name = ""):
		sublime.active_window().new_file();
