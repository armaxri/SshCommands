#!/usr/bin/env python3
"""
Sublime Text plugin to send commands to other computers using SSH.
"""
import os
import sys

import paramiko

import sublime
import sublime_plugin

DEBUG = False

ADD_MISSING_HOST = 'add_missing_known_hosts'
KNOWN_HOSTS = 'known_host_keys_file_path'
HOSTNAME = 'hostname'
PORT = 'port'
USERNAME = 'username'
PASSWORD = 'password'
RSA_KEY = 'rsa_key_path'

COMMAND_GROUP = 'commands'
SINGLE_COMMANDS_GOUP = 'single_commands'

DEFAULT_VALUES = {ADD_MISSING_HOST : False, KNOWN_HOSTS : None, HOSTNAME : '127.0.0.1', PORT : 22, USERNAME : None, PASSWORD : None, RSA_KEY : None, SINGLE_COMMANDS_GOUP : ['cd /']}

SETTINGS_FILENAME = 'SshCommands.sublime-settings'

def trace(message):
    """
    print a debug messgae
    """
    if DEBUG:
        print(message)
        sys.stdout.flush()


def plugin_loaded():
    """
    Load the plugin
    """
    settings = sublime.load_settings(SETTINGS_FILENAME)
    global DEBUG
    DEBUG = settings.get('debug')
    trace('SSH commands loaded')


def plugin_unloaded():
    """
    Unload the plugin
    """
    trace('SSH commands unloaded')


class SshCommands(sublime_plugin.WindowCommand):

    def run(self):
        trace('run SSH commands sender')
        names = self.get_commands()
        sublime.active_window().show_quick_panel(names, self.on_select_command)


    def get_commands(self):
        trace('get all defined commands')
        settings = sublime.load_settings(SETTINGS_FILENAME)
        ret = list()
        commands = settings.get(COMMAND_GROUP)
        if commands:
            ret = list(commands.keys())
        else:
            trace('None commands')
        return ret


    def load_command_settings(self, item):
        params = dict()
        param_types = [ADD_MISSING_HOST, KNOWN_HOSTS, HOSTNAME, PORT, USERNAME, PASSWORD, RSA_KEY, SINGLE_COMMANDS_GOUP]

        settings = sublime.load_settings(SETTINGS_FILENAME)

        super_commands = settings.get(COMMAND_GROUP)
        command_dict = list(super_commands.values())[item]

        trace('selected command name: "' + list(super_commands.keys())[item])

        for setting_key in param_types:
            # Set the default setting for the parameter (not really useful and good values).
            if setting_key in params:
                params[setting_key] = command_dict[DEFAULT_VALUES]

            # If exists load the global setting for the parameter and override the default setting.
            if settings.has(setting_key):
                params[setting_key] = settings.get(setting_key)

            # If exists load the command specific setting and override the default or global setting.
            # Hopefully there is a useful value after this point...
            if setting_key in command_dict:
                params[setting_key] = command_dict[setting_key]

        return params


    def on_select_command(self, item):
        if -1 == item:
            trace('cancel ...')
            return

        params = self.load_command_settings(item)

        output_view = self.window.new_file()

        try:
            client = paramiko.SSHClient()
            if KNOWN_HOSTS in params:
                trace('unsing known hosts file: "' + params[KNOWN_HOSTS] + '"')
                client.load_system_host_keys(filename=params[KNOWN_HOSTS])
            else:
                client.load_system_host_keys()

            if params[ADD_MISSING_HOST]:
                trace('add missing hosts: true')
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            else:
                trace('add missing hosts: false')
                client.set_missing_host_key_policy(paramiko.WarningPolicy)

            # This is more like a bad workaround for now.
            # If there is set a password, it will use the password over
            # the RSA key. I choose this strategy since I believe it's more
            # common to set a global RSA key than a global password.
            # 
            # ToDo: Search for a better strategy!
            if PASSWORD in params:
                client.connect(params[HOSTNAME], port=params[PORT], username=params[USERNAME], password=params[PASSWORD])
            else:
                client.connect(params[HOSTNAME], port=params[PORT], username=params[USERNAME], pkey=params[RSA_KEY])

            for command in params[SINGLE_COMMANDS_GOUP]:
                self.handle_command(client, command, output_view)

        except Exception as e:
            print('*** Caught exception: %s: %s' % (e.__class__, e))
            trace(print_exc())
            try:
                client.close()
            except:
                pass


    def handle_command(self, client, command, view):
        trace('sending command: "' + command + '"')
        stdin, stdout, stderr = client.exec_command(command)
        message = stdout.read().decode("utf-8") 
        trace('return of command: \n' + message + '\n')

        message_4_output = '$ ' + command + '\n' + message
        view.run_command("insert", {"characters": message_4_output})
        return message

