import sublime, sublime_plugin

import os, stat

DEFAULT_THEME_PACKAGE = 'Theme - Default'
DEFAULT_THEME = 'Default.sublime-theme'

DEFAULT_COLOR_SCHEME_PACKAGE = 'Color Scheme - Default'
DEFAULT_COLOR_SCHEME = 'Packages/Color Scheme - Default/Monokai.tmTheme'

DEFAULT_PACKAGES = [
	'ActionScript', 'AppleScript', 'ASP', 'Batch File', 'C#', 'C++', 'Clojure',
	'Color Scheme - Default', 'CSS', 'D', 'Default', 'Diff', 'Erlang', 'Go',
	'Graphviz', 'Groovy', 'Haskell', 'HTML', 'Java', 'JavaScript',
	'Language - English', 'LaTeX', 'Lisp', 'Lua', 'Makefile', 'Markdown',
	'Matlab', 'Objective-C', 'OCaml', 'Pascal', 'Perl', 'PHP', 'Python',
	'R', 'Rails', 'Regular Expressions', 'RestructuredText', 'Ruby',
	'Scala', 'ShellScript', 'SQL', 'TCL', 'Text', 'Textile',
	'Theme - Default', 'Vintage', 'XML', 'YAML', 'Issues'
]

class IssuesClipboardInformationSystem(sublime_plugin.WindowCommand):
	def run(self):
		pass

	def is_enabled(self):
		return False

class IssuesClipboardInformationPackages(sublime_plugin.WindowCommand):
	def run(self):
		pass

	def is_enabled(self):
		return False

class IssuesPastebinInformationSystem(sublime_plugin.WindowCommand):
	def run(self):
		pass

	def is_enabled(self):
		return False

class IssuesPastebinInformationPackages(sublime_plugin.WindowCommand):
	def run(self):
		pass

	def is_enabled(self):
		return False

class IssuesCleanCache(sublime_plugin.WindowCommand):
	def run(self):
		"""
			This should shutdown ST, remove the following files and folders, and restart ST:
				1. Clean the "cache" folder: sublime.cache_path()
				2. Clean the "index" folder: sublime.cache_path()/../Index/
				3. Remove the files:
					sublime.packages_path()/../Local/Session.sublime_metrics
					sublime.packages_path()/../Local/Session.sublime_session
					sublime.packages_path()/../Local/Auto Save Session.sublime_session
				4. ??
		"""
		clean_caches()
		restart_sublime_text()

	def is_enabled(self):
		return False

class IssuesPackageControlInstall(sublime_plugin.WindowCommand):
	def run(self):
		pass

	def is_enabled(self):
		return False

class IssuesPackageControlUpgradePackages(sublime_plugin.WindowCommand):
	def run(self):
		pass

	def is_enabled(self):
		return False

class IssuesPackagesDisableNonDefault(sublime_plugin.WindowCommand):
	def run(self):
		"""
			This should:
				1. DONE - Restore the default theme and color scheme (just in case we are going to disable some custom theme and color scheme)
				2. DONE - Backup the list of ignored packages
				3. DONE - Disable any non-default package
				4. Restart Sublime Text
		"""
		if sublime.ok_cancel_dialog('Disable non-default Packages?'):
			st = sublime.load_settings('Preferences.sublime-settings')
			issues = sublime.load_settings('Issues.sublime-settings')

			IssuesFixThemeColorSchemeRestoreDefault(sublime_plugin.WindowCommand).run(False)

			issues.set('ignored_packages', st.get('ignored_packages', []))

			st.set('ignored_packages', [package for package in package_list() if package not in DEFAULT_PACKAGES])

			sublime.save_settings('Issues.sublime-settings')
			sublime.save_settings('Preferences.sublime-settings')

			clean_caches()
			restart_sublime_text()

class IssuesPackagesRenableLastDisable(sublime_plugin.WindowCommand):
	def run(self):
		"""
			This should:
				1. DONE - Restore the previous list of ignored packages
				2. Restart Sublime Text
		"""
		if sublime.ok_cancel_dialog('Restore User enabled Packages?'):
			st = sublime.load_settings('Preferences.sublime-settings')
			issues = sublime.load_settings('Issues.sublime-settings')

			IssuesFixThemeColorSchemeRestoreUser(sublime_plugin.WindowCommand).run(False)

			st.set('ignored_packages', issues.get('ignored_packages', []))

			issues.erase('ignored_packages')

			sublime.save_settings('Issues.sublime-settings')
			sublime.save_settings('Preferences.sublime-settings')

			clean_caches()
			restart_sublime_text()

	def is_enabled(self):
		issues = sublime.load_settings('Issues.sublime-settings')
		return issues.has('ignored_packages')

class IssuesRecordActionsStart(sublime_plugin.WindowCommand):
	def run(self):
		pass

	def is_enabled(self):
		return False

class IssuesRecordActionsStop(sublime_plugin.WindowCommand):
	def run(self):
		pass

	def is_enabled(self):
		return False

class IssuesFixThemeColorSchemeRestoreDefault(sublime_plugin.WindowCommand):
	def run(self, ask = True):
		"""
			This should:
				1. Check if the default themes are not present or modified
				2. Restore the default theme and color scheme
				3. DONE - Set in Preferences the default theme and color scheme
				4. DONE - Remove these from the list of ignored packages
				5. Clean caches, and Restart ST
		"""
		if ask and sublime.ok_cancel_dialog('Restore Default Theme and Default Color Scheme?') or not ask:
			st = sublime.load_settings('Preferences.sublime-settings')
			issues = sublime.load_settings('Issues.sublime-settings')

			issues.set('color_scheme', st.get('color_scheme', DEFAULT_COLOR_SCHEME) or DEFAULT_COLOR_SCHEME)
			issues.set('theme', st.get('theme', DEFAULT_THEME) or DEFAULT_THEME)

			st.set('color_scheme', DEFAULT_COLOR_SCHEME)
			st.set('theme', DEFAULT_THEME)

			st.set('ignored_packages', [package for package in st.get('ignored_packages', []) if package != DEFAULT_THEME_PACKAGE and package != DEFAULT_COLOR_SCHEME_PACKAGE])

			sublime.save_settings('Issues.sublime-settings')
			sublime.save_settings('Preferences.sublime-settings')

			if ask:
				clean_caches()
				restart_sublime_text()

class IssuesFixThemeColorSchemeRestoreUser(sublime_plugin.WindowCommand):

	def run(self, ask = True):
		"""
			This should:
				1. DONE - Restore Users theme and color scheme settings from a previous backup
				2. Clean caches, and Restart ST
		"""
		issues = sublime.load_settings('Issues.sublime-settings')
		if issues.has('color_scheme') and issues.has('theme') and (ask and sublime.ok_cancel_dialog('Restore User Theme and User Color Scheme?') or not ask):
			st = sublime.load_settings('Preferences.sublime-settings')
			issues = sublime.load_settings('Issues.sublime-settings')

			st.set('color_scheme', issues.get('color_scheme', DEFAULT_COLOR_SCHEME))
			st.set('theme', issues.get('theme', DEFAULT_THEME))

			# TODO, if the user package is disable, we should re enable.
			# st.set('ignored_packages', [package for package in st.get('ignored_packages', []) if package != DEFAULT_THEME_PACKAGE and package != DEFAULT_COLOR_SCHEME_PACKAGE])

			issues.erase('color_scheme')
			issues.erase('theme')

			sublime.save_settings('Issues.sublime-settings')
			sublime.save_settings('Preferences.sublime-settings')
			if ask:
				clean_caches()
				restart_sublime_text()

	def is_enabled(self):
		issues = sublime.load_settings('Issues.sublime-settings')
		return issues.has('color_scheme') and issues.has('theme')

class IssuesResetSublimeText(sublime_plugin.WindowCommand):
	def run(self):
		pass

	def is_enabled(self):
		return False



def restart_sublime_text():
	if sublime.ok_cancel_dialog('Sublime Text Needs Restarting. Do You Want to Close It?'):
		sublime.active_window().run_command('exit')
	else:
		sublime.message_dialog('Please Restart Sublime Text')

def clean_caches():
	pass

def package_list():
	packages = []
	if os.path.lexists(sublime.packages_path()):
		for file in os.listdir(sublime.packages_path()):
			packages.append(file.replace('.sublime-package', ''))
	if sublime.installed_packages_path():
		for file in os.listdir(sublime.installed_packages_path()):
			packages.append(file.replace('.sublime-package', ''))

	packages = [package for package in list(set(packages)) if package]
	packages.sort()
	return packages

def path_is_none(path):
	if path == None or path == '' or path == '.' or path == '..' or path == './' or path == '../' or path == '/' or path == '//' or path == '\\' or path == '\\\\' or path == '\\\\\\\\' or path == '\\\\?\\' or path == '\\\\?' or path == '\\\\\\\\?\\\\':
		return True
	else:
		return False

def elevate_permissions(function, path, excinfo):
	if not os.access(path, os.W_OK):
		try:
			os.chmod(path, stat.S_IWUSR)
		except:
			pass
		function(path)
	else:
		pass