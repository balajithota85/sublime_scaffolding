import sublime
import sublime_plugin
import functools
import os

settings = sublime.load_settings('Scaffolding.sublime-settings')

def get_project_name():
	project_name = settings.get('new_project_name')
	if not project_name:
		project_name = ''
	return project_name

class ScaffoldingCommand():
 	def create_empty_project(self, path):
 		return

 	def create_scaffold_project(self, path, name):
 		scaffold_folders = settings.get('scaffold_folders')
		project_folders = settings.get('project_folders')

		if not scaffold_folders:
			return

		source_folder_path = path + os.sep + name + os.sep
		for scaffold_folder in scaffold_folders:
			scaffold_folder_path = source_folder_path + scaffold_folder
			os.makedirs(scaffold_folder_path)
			self.create_project_base_files(scaffold_folder_path, scaffold_folder)

			if scaffold_folders:
				for project_folder in project_folders:
					project_folder_path = scaffold_folder_path + os.sep + project_folder
					os.makedirs(project_folder_path)

 	def create_project_base_files(self, path, name):
 		files = settings.get(name + '_project_files')

 		if not files:
 			return

 		for file_name in files:
 			project_file = open(path + os.sep + file_name, 'w')
 			project_file.close()

class ScaffoldingCreateProjectCommand(sublime_plugin.WindowCommand, ScaffoldingCommand):
	def run(self, paths=[]):
		project_name = get_project_name()
		self.window.run_command('hide_panel')
		# self.window.show_input_panel("Project Name:", name, lambda name:self.on_load(paths, name), None, None)
		self.window.show_input_panel("Project Name:", project_name, functools.partial(self.on_load, paths), None, None)

	def on_load(self, paths=[], project_name=""):
		if not paths:
			return

		project_path = paths[0]
		self.create_empty_project(project_path, project_name)

class ScaffoldingCreateBootstrapProjectCommand(sublime_plugin.WindowCommand, ScaffoldingCommand):
	def run(self, paths=[]):
		project_name = get_project_name()
		self.window.run_command('hide_panel')
		# self.window.show_input_panel("Project Name:", name, lambda name:self.on_load(paths, name), None, None)
		self.window.show_input_panel("Project Name:", project_name, functools.partial(self.on_load, paths), None, None)

	def on_load(self, paths=[], project_name=""):
		if not paths:
			return

		project_path = paths[0]
		self.create_scaffold_project(project_path, project_name)