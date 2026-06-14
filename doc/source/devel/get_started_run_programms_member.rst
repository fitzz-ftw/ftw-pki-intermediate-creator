The Certificat ASign Request Creation Development
##################################################


.. SECTION - Setup
>>> test_data_pre= "data-inter-member-creator"

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)
>>> env.clean_home()

.. !SECTION
.. SECTION - Prepare

>>> from pathlib import Path


>>> test_paswd_path = env.copy2cwd(f"{test_data_pre}/membersecret", "membersecret")


>>> conf_file = env.copy2cwd(f"{test_data_pre}/M-V-HH-Member-CA.toml", "M-V-HH-Member-CA.toml")

>>> def stub_getpass(prompt:str)->str:
...     print(prompt)
...     return "secret"

>>> def stub_keyboard_interrupt(prompt:str)->str:
...     print(prompt)
...     raise KeyboardInterrupt



>>> cmd_line="--conf-file M-V-HH-Member-CA.toml"
>>> cmd_line += " -k hamburg_ca "
>>> cmd_line += " -n M-V-HH-CA "
>>> cmd_line += " membersecret"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf-file', 'M-V-HH-Member-CA.toml', 
 '-k', 'hamburg_ca', 
 '-n', 'M-V-HH-CA', 
 'membersecret']

..!SECTION

>>> import getpass

>>> getpass.getpass = stub_getpass

>>> from ftwpki.intermed_creator.programms import prog_intermediate_csr

>>> prog_intermediate_csr(sys_argv)
Enter Password:
0


>>> test_paswd_path = env.copy2cwd(f"{test_data_pre}/membersecret", "membersecret")

>> conf_file = env.copy2cwd(f"{test_data_pre}/M-V-HH-Member-CA.toml", "M-V-HH-Member-CA.toml")


>>> prog_intermediate_csr(sys_argv)
[Errno 2] No such file or directory: 'M-V-HH-Member-CA.toml'
1

>>> conf_file = env.copy2cwd(f"{test_data_pre}/M-V-HH-Member-CA.toml", "M-V-HH-Member-CA.toml")
>>> prog_intermediate_csr(sys_argv)
Enter Password:
0



>>> conf_file = env.copy2cwd(f"{test_data_pre}/M-V-HH-Member-CA.toml", "M-V-HH-Member-CA.toml")
>>> prog_intermediate_csr(sys_argv)
Enter Password:
0

>>> getpass.getpass = stub_keyboard_interrupt

>>> conf_file = env.copy2cwd(f"{test_data_pre}/M-V-HH-Member-CA.toml", "M-V-HH-Member-CA.toml")
>>> prog_intermediate_csr(sys_argv)
Enter Password:
1

>>> cmd_line = " -k hamburg_ca "
>>> cmd_line += " -n M-V-HH-CA "
>>> cmd_line += " membersecret"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> prog_intermediate_csr(sys_argv)
the following arguments are required: --conf-file
1



.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION
