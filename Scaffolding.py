import sublime
import sublime_plugin
import functools
import os
import urllib2
import threading

settings = sublime.load_settings('Scaffolding.sublime-settings')

def get_project_name():
	project_name = settings.get('new_project_name')
	if not project_name:
		project_name = ''
	return project_name

class URLDownloader(threading.Thread):
	def __init__(self, url, file_path):
		self.url = url
		self.file_path = file_path
		threading.Thread.__init__(self)

	def run(self):
		try:
			print "thread:" + self.url
			response = urllib2.urlopen(self.url)
			self.result = response.read()
			script_file = open(self.file_path, 'w')
			script_file.write(self.result)
			script_file.close()
			return

		except (urllib2.HTTPError) as (e):
			err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))
		except (urllib2.URLError) as (e):
			err = '%s: URL error %s contacting API' % (__name__, str(e.reason))

		sublime.error_message(err)
		self.result = False

class ScaffoldingCommand():
 	def create_project(self, path, name):
 		if not path or not name:
 			return

		source_folder_path = path + os.sep + name
		os.makedirs(source_folder_path)

		project_folders = settings.get('project_folders')

		if project_folders:
			for project_folder in project_folders:
				project_folder_path = source_folder_path + os.sep + project_folder
				os.makedirs(project_folder_path)

		self.create_project_base_files(source_folder_path, 'app')

 	def create_scaffold_project(self, path, name):
 		if not path or not name:
 			return

 		scaffold_folders = settings.get('scaffold_folders')
		project_folders = settings.get('project_folders')

		if not scaffold_folders:
			return

		source_folder_path = path + os.sep + name + os.sep
		for scaffold_folder in scaffold_folders:
			scaffold_folder_path = source_folder_path + scaffold_folder
			os.makedirs(scaffold_folder_path)
			
			if project_folders:
				for project_folder in project_folders:
					project_folder_path = scaffold_folder_path + os.sep + project_folder
					os.makedirs(project_folder_path)

			self.create_project_base_files(scaffold_folder_path, scaffold_folder)

 	def create_project_base_files(self, path, name):
 		files = settings.get(name + '_project_files')

 		if files:
	 		for file_name in files:
	 			project_file = open(path + os.sep + file_name, 'w')
	 			project_file.close()

	 	for resource in ['scripts', 'styles', 'images']:
			self.populate_resources(path, name, resource)

	def handle_script_threads(self, threads):
		return

	def populate_resources(self, path, name, resource_name):
		resources_folder_name = settings.get(resource_name + '_folder')
		resources = settings.get(name + '_' + resource_name)
 		resources_threads = []
 		if resources:
 			no_of_resources = len(resources)
 			for resource in resources:
				last_slash_index = resource.rfind('/')
				if last_slash_index != -1:
					resource_file_name = resource[last_slash_index+1:]
				else:
					resource_file_name = resource_name + no_of_resources + '.txt'
					no_of_resources -= 1
				
				resource_file_path = path
				resource_file_path += os.sep + resources_folder_name + os.sep + resource_file_name

				print "resource: " + resource_file_name
				resource_thread = URLDownloader(resource, resource_file_path)
				resources_threads.append(resource_thread)
				resource_thread.start()
		return

	def populate_styles(self, path, name):
		return
class ScaffoldingCreateProjectCommand(sublime_plugin.WindowCommand, ScaffoldingCommand):
	def run(self, paths=[]):
		if not paths:
			current_view_path = sublime.active_window().active_view().file_name()
			current_view_last_index = current_view_path.rfind(os.sep)
			if current_view_last_index != -1:
				current_view_folder_path = current_view_path[0:current_view_last_index]
				# print current_view_folder_path
				paths = [current_view_folder_path]
			else:
				return

		project_name = get_project_name()
		self.window.run_command('hide_panel')
		# self.window.show_input_panel("Project Name:", name, lambda name:self.on_load(paths, name), None, None)
		self.window.show_input_panel("Project Name:", project_name, functools.partial(self.on_load, paths), None, None)

	def on_load(self, paths=[], project_name=""):
		if not paths:
			return

		project_path = paths[0]
		self.create_project(project_path, project_name)

class ScaffoldingCreateScaffoldProjectCommand(sublime_plugin.WindowCommand, ScaffoldingCommand):
	def run(self, paths=[]):
		if not paths:
			current_view_path = sublime.active_window().active_view().file_name()
			current_view_last_index = current_view_path.rfind(os.sep)
			if current_view_last_index != -1:
				current_view_folder_path = current_view_path[0:current_view_last_index]
				# print current_view_folder_path
				paths = [current_view_folder_path]
			else:
				return

		project_name = get_project_name()
		self.window.run_command('hide_panel')
		# self.window.show_input_panel("Project Name:", name, lambda name:self.on_load(paths, name), None, None)
		self.window.show_input_panel("Project Name:", project_name, functools.partial(self.on_load, paths), None, None)

	def on_load(self, paths=[], project_name=""):
		if not paths:
			return

		project_path = paths[0]
		self.create_scaffold_project(project_path, project_name)