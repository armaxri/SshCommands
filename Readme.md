SshCommands
===========
A plugin for **SublimeText 3** developed to send commands to SSH servers. This can be useful if you use **SublimeText 3** to edit files on a remote system and trigger build or other processes on that system.

<span style="color:red">The plugin is currently only working on Windows and only if you have installed the required Python plugins. A installation guide for these tools will follow.</span>

## Installation:
ToDo

## Usage :

### To configure :

Use <kbd>ctrl</kbd>+<kbd>shift</kbd>+<kbd>P</kbd> then `SshCommands: Settings - User` to change the user settings and add your commands, which you want to send via SSH.

The configuration is structured as following: Under "commands" you can add your with names of your choosing. The actual commands, which are going to be send to the server, have to be saved in a array named "single_commands".

There are also other settings, which can be set global for all commands and locally for a single command (local settings overwrite global settings). Are both a password and a RSA key given, the tool will use the password.

For Example::

```js
{
    "add_missing_known_hosts": false,
    "known_host_keys_file_path": "C:\\Users\\<username>\\.ssh\\known_hosts",
    "rsa_key_path": "C:\\Users\\<username>\\.ssh\\id_rsa",
    "port": 22,
    "commands":
    {
        "Example: create files":
        {
            "hostname": "raspberrypi",
            "username": "pi",
            "password": "root",
            "single_commands":
            [
                "echo \"blub1\" > test1.txt",
                "sleep 2",
                "echo \"blub2\" > test2.txt",
                "sleep 2",
                "echo \"blub3\" > test3.txt",
                "sleep 2",
                "echo \"blub4\" > test4.txt",
                "sleep 2",
            ]
        },
        "Example: read files":
        {
            "hostname": "raspberrypi",
            "username": "pi",
            "password": "root",
            "single_commands":
            [
                "less test1.txt",
                "sleep 2",
                "less test2.txt",
                "sleep 2",
                "less test3.txt",
                "sleep 2",
                "less test4.txt",
                "sleep 2",
            ]
        },
        "Example: show files":
        {
            "hostname": "raspberrypi",
            "port": 22,
            "username": "pi",
            "password": "root",
            "single_commands":
            [
                "ls -l",
                "sleep 2",
            ]
        },
    }
}
```

### To send :

 - use <kbd>ctrl</kbd>+<kbd>shift</kbd>+<kbd>P</kbd> then `SshCommands: Execute Command` to show the list of your defined commands and just select your command.
 - use <kbd>ctrl</kbd>+<kbd>alt</kbd>+<kbd>C</kbd> to show the list of your defined commands and just select your command.ts.

## Known Issues :

- Calling "more" will make the plugin stuck.
- There is currently no error handling. Your configuration has to work.
- There is no timeout functionality.

## Support :

- Any bugs about Markdown Preview please feel free to report [here][issue].
- And you are welcome to fork and submit pull requests.

## License :

The code is available at github [project][home] under [MIT licence][licence].


[issue]: https://github.com/armaxri/SshCommands/issues
[home]: https://github.com/armaxri/SshCommands
[licence]: https://github.com/armaxri/SshCommands/blob/master/LICENSE

