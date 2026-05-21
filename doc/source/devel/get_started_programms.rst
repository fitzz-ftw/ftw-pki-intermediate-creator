The Certificat ASign Request Creation
#########################################




.. SECTION - Setup

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

.. SECTION - Start programm

.. SECTION - Configuration

>>> from ftwpki.baselibs.toml_utils import toml2dn
>>> from ftwpki.intermed_creator.cli_parser import CSRIntermediateParser

>>> from ftwpki.baselibs.configuration import IntermedPKIConfig

>>> config:IntermedPKIConfig = IntermedPKIConfig()
>>> config.set_config()

>>> ca_parser = CSRIntermediateParser(prog="ftwpkicsrinter")
>>> ca_parser.set_defaults(**toml2dn(sys_argv))
>>> args = ca_parser.parse_args(sys_argv)
>>> args #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS 
Namespace(countryName='DE', 
    stateOrProvinceName='Mystate', 
    localityName='Somewherecity', 
    organizationName='Fitzz TeXnik Welt', 
    organizationalUnitName='Security', 
    commonName='Fitzz Reinshagen', 
    dnsubject={'countryName': 'DE', 
        'stateOrProvinceName': 'Mystate', 
        'organizationName': 'Fitzz TeXnik Welt', 
        'commonName': 'Fitzz Reinshagen', 
        'localityName': 'Somewherecity', 
        'organizationalUnitName': 'Security'}, 
    conf_file=PosixPath('ca_root_conf.toml'),
    key_name='reinsha', 
    privatdir='.private',
    passphrasefile='testpasswd', 
    private_key='reinsha.key.pem', 
    public_key='reinsha.pub.pem')

..SECTION - Copy passphrasefile

>>> (config.config_path / args.privatdir / args.passphrasefile).is_file()
False

>>> Path(args.passphrasefile).is_file()
True

>>> import shutil

>>> _ = shutil.move(Path(args.passphrasefile),config.config_path / args.privatdir / args.passphrasefile )


.. !SECTION - Copy passphrasefile


.. !SECTION - Configuration

.. SECTION - Passwordhandling

>>> from ftwpki.baselibs.passwd import PasswordManager
>>> pwd_man = PasswordManager(private_dir=str(config.config_path / args.privatdir))
>>> pwd_man #doctest: +ELLIPSIS
PasswordManager(private_dir='...ftwpki/.private')

..!SECTION - Passwordhandling

.. SECTION - CSR Creation

>>> from ftwpki.baselibs.cert_request import CertificateRequest
>>> from ftwpki.baselibs.policies import IntermediatePolicy
>>> from ftwpki.baselibs.core import (
...         create_distinguished_name,
...         load_private_key_from_pem, 
...         generate_rsa_key_pair,
...         )


>>> subject = create_distinguished_name(
...     country=args.countryName,
...     state=args.stateOrProvinceName,
...     location=args.localityName,
...     organization=args.organizationName,
...     common_name=args.commonName,
...     organizational_unit=args.organizationalUnitName,
... )



>>> reins_csr = CertificateRequest(
...     subject = subject,
...     policy = IntermediatePolicy(),
... )

>>> reins_csr #doctest: +NORMALIZE_WHITESPACE
CertificateRequest(subject=<Name(CN=Fitzz Reinshagen,OU=Security,O=Fitzz TeXnik Welt,L=Somewherecity,ST=Mystate,C=DE)>)

.. !SECTION - CSR Creation

.. SECTION - Keypair Creation


>>> priv, pub = generate_rsa_key_pair(passphrase=pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = getpasswd("Enter Passphrase:")
... ), key_size=4096)
Enter Passphrase:

>>> priv #doctest: +ELLIPSIS
b'-----BEGIN ENCRYPTED PRIVATE KEY-...

>>> pub #doctest: +ELLIPSIS
b'-----BEGIN PUBLIC KEY---...

.. !SECTION - Keypair Creation

.. SECTION - Save Keys and CSR

>>> from ftwpki.baselibs.core import save_pem
>>> save_pem(priv, 
...     config.config_path / f"{args.privatdir}/{args.private_key}", 
...     is_private=True)
>>> save_pem(pub, config.data_path /f"{args.public_key}", is_private=False)

>> reins_csr.build(passphrase= pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = getpasswd("Enter Passphrase:")
... ))
Enter Passphrase:


>> reins_csr.build(load_private_key_from_pem(pem_data=priv, 
...     passphrase= pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = getpasswd("Enter Passphrase:")
... )))
Enter Passphrase:

>>> save_pem(reins_csr.build(load_private_key_from_pem(pem_data=priv, passphrase= pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = getpasswd("Enter Passphrase:")
... ))).get_pem(), Path(f"{args.organizationName.replace(' ','-')+ args.localityName.replace(' ','-') + '.csr'}"), is_private=False)
Enter Passphrase:

.. !SECTION - Save Keys and CSR

.. !SECTION - Stop programm

.. SECTION - Teardown

>>> env.clean_home()
>>> env.teardown()

.. !SECTION
