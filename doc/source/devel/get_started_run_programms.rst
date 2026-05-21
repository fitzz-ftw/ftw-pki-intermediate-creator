The Certificat ASign Request Creation
#########################################




.. SECTION - Setup

>>> import getpass

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)
>>> env.clean_home()

.. !SECTION
.. SECTION - Prepare

>>> from pathlib import Path
>>> private_dir:Path = Path("privat")
>>> private_dir.mkdir(parents=True, exist_ok=True)
>>> test_paswd_path = env.copy2cwd("privat/testpasswd","testpasswd")
>>> conf_file = env.copy2cwd("ca_root_conf.toml")

>>> def getpasswd(prompt:str)->str:
...     print(prompt)
...     return "strenggeheim"

>>> getpass.getpass = getpasswd

>>> cmd_line="--conf-file ca_root_conf.toml -ST Mystate --commonName 'Fitzz Reinshagen' "
>>> cmd_line += " -k reinsha "
>>> cmd_line += " --private-dir .private"
>>> cmd_line += " testpasswd"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf-file', 'ca_root_conf.toml', 
 '-ST', 'Mystate', 
 '--commonName', 'Fitzz Reinshagen',
 '-k', 'reinsha',
 '--private-dir', '.private',
 'testpasswd']

..!SECTION

>>> from ftwpki.intermed_creator.programms import prog_intermediate_csr

>>> prog_intermediate_csr(sys_argv)
Enter Passphrase:
Enter Passphrase:
0


>>> conf_file = env.copy2cwd("ca_root_conf.toml")

>>> test_paswd_path = env.copy2cwd("privat/testpasswd","testpasswd")

>>> prog_intermediate_csr(sys_argv)
Enter Passphrase:
Enter Passphrase:
0


.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION
