# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.events

class NotifyprowlPlugin(octoprint.plugin.SettingsPlugin,
                        octoprint.plugin.AssetPlugin,
                        octoprint.plugin.StartupPlugin,
                        octoprint.plugin.TemplatePlugin,
                        octoprint.plugin.EventHandlerPlugin):

	def __init__(self):
		self.prowlPriority = 0  # 0=Normal, -1=Moderate, -2=VeryLow, 1=High, 2=Emergency
				
	def on_after_startup(self):
		# populate API key from settings
		self.apikey = self._settings.get(["apikey"])

	# EventPlugin API
	def on_event(self, event, payload):
		import os
		import prowler

		self.apikey = self._settings.get(["apikey"])
		
		# By default, don't send a message
		sendMessage = False
		
		# Name of app to report to Prowl
		prowlApp = "OctoPrint"

		# Print Complete
		if event == octoprint.events.Events.PRINT_DONE:
				self._logger.info("NotifyProwl received PRINT_DONE event")
				
				filename = payload["name"]
				time = payload["time"]
								
				sendMessage = True
				prowlMessage = filename + " finished printing"
				prowlPriority = self.prowlPriority
				prowlEvent = "Print Complete"

		# Send the message to Prowl
		if sendMessage == True and self.apikey != "":
			try:
			  prowler.post(key=self.apikey, message=prowlMessage, priority=prowlPriority, app=prowlApp, event=prowlEvent)
			except Exception as msg:
			  self._logger.info("Prowl notification failed: " + str(msg) + " using key " + self.apikey)


	##~~ SettingsPlugin mixin

	def get_settings_defaults(self):
		return dict(
			# put your plugin's default settings here
			apikey="enter your API key here"
		)
	
	def get_template_configs(self):
		return [
			dict(type="settings", custom_bindings=False)
		]
		
	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/NotifyProwl.js"],
			css=["css/NotifyProwl.css"],
			less=["less/NotifyProwl.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			NotifyProwl=dict(
				displayName="Notifyprowl Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="mrcompsci",
				repo="OctoPrint-NotifyProwl",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/mrcompsci/OctoPrint-NotifyProwl/archive/{target_version}.zip"
			)
		)


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "NotifyProwl"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = NotifyprowlPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

