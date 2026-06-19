The Certificat ASign Request Creation Development
##################################################


.. SECTION - Setup

>>> test_data_pre= "data-inter-base-creator"

>>> from fitzzftw.devtools.testinfra import TestHomeEnvironment
>>> from pathlib import Path
>>> env = TestHomeEnvironment(Path("doc/source/devel/testhome"))
>>> env.setup(True)
>>> env.clean_home()

.. !SECTION
.. SECTION - Prepare

>>> from pathlib import Path


>>> test_paswd_path = env.copy2cwd(f"{test_data_pre}/inter1secret", "inter1secret")


>>> conf_file = env.copy2cwd(f"{test_data_pre}/ca_intermed_hamburg_conf.toml", "ca_intermed_hamburg_conf.toml")

>>> def stub_getpass(prompt:str)->str:
...     print(prompt)
...     return "secret"

>>> cmd_line="--conf-file ca_intermed_hamburg_conf.toml"
>>> cmd_line += " -k hamburg_ca "
>>> cmd_line += " -n M-V-HH-CA "
>>> cmd_line += " inter1secret"

>>> import shlex
>>> sys_argv= shlex.split(cmd_line) 
>>> sys_argv #doctest: +NORMALIZE_WHITESPACE
['--conf-file', 'ca_intermed_hamburg_conf.toml', 
 '-k', 'hamburg_ca', 
 '-n', 'M-V-HH-CA', 
 'inter1secret']

..!SECTION

.. SECTION - Start programm

.. SECTION - Configuration

>>> from ftwpki.baselibs.toml_utils import toml2dn
>>> from ftwpki.intermed_creator.cli_parser import CSRIntermediateParser

>>> from ftwpki.baselibs.configuration import IntermedPKIConfig

>>> pre_parser = CSRIntermediateParser(add_help=False, allow_abbrev=False)
>>> pre_args , _ = pre_parser.parse_known_args(sys_argv)

>>> pki_name = Path(pre_args.conf_file).stem

>>> pre_conf = toml2dn(Path(pre_args.conf_file).read_text())

>>> pre_conf["pki_name"] = pki_name

>>> ca_parser = CSRIntermediateParser(prog="ftwpkicsrinter")

>>> ca_parser.set_defaults(**pre_conf)

>> ca_parser.print_help()

>>> args = ca_parser.parse_args(sys_argv)

>>> args #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
CSRIntermediateArguments(commonName='Muster-Verband Hamburg Regional CA'
    conf_file='ca_intermed_hamburg_conf.toml'
    countryName='DE'
    dnsubject={'countryName': 'DE', 
        'localityName': 'Hamburg', 
        'organizationName': 'Muster-Verband e.V.', 
        'organizationalUnitName': 'Regionalverband Nord', 
        'commonName': 'Muster-Verband Hamburg Regional CA'}
    key_name='hamburg_ca'
    localityName='Hamburg'
    organizationName='Muster-Verband e.V.'
    organizationalUnitName='Regionalverband Nord'
    passphrasefile='inter1secret'
    pki_name='M-V-HH-CA'
    privatdir=''
    stateOrProvinceName='')

>>> config:IntermedPKIConfig = IntermedPKIConfig()


>>> config.current_configfile_entries #doctest: +NORMALIZE_WHITESPACE
{'private_keys': '#zip#', 
 'zip': '#config#.private', 
 'certs': '#zip#', 
 'chains': '#zip#', 
 'passphrases': '#config#.private', 
 'policies': '#zip#', 
 'config_path': '#config#', 
 'data_path': '#data#'}


>> config._paths

..SECTION - Copy passphrasefile

>>> ppf_in_priv = (config.passphrases / args.passphrasefile).is_file()
>>> ppf_in_priv
False

>>> ppf_in_cwd = Path(args.passphrasefile).is_file()
>>> ppf_in_cwd
True



>>> import shutil

>>> if ppf_in_cwd and not ppf_in_priv:
...     _ = shutil.move(Path(args.passphrasefile),config.passphrases / args.passphrasefile )
... elif ppf_in_cwd:
...     Path(args.passphrasefile).unlink(True)

.. !SECTION - Copy passphrasefile


.. !SECTION - Configuration

.. SECTION - Passwordhandling

>>> from ftwpki.baselibs.passwd import PasswordManager
>>> pwd_man = PasswordManager(private_dir=str(config.passphrases))
>>> pwd_man #doctest: +ELLIPSIS
PasswordManager(private_dir='...ftwpki....private')


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


>>> reins_csr #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
CertificateRequest(subject=<Name(...CN=Muster-Verband Hamburg Regional CA...)>)

.. !SECTION - CSR Creation

.. SECTION - Keypair Creation

>>> password = stub_getpass("Enter Password:")
Enter Password:

>>> private_key, public_key = generate_rsa_key_pair(passphrase=pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = password
... ), key_size=4096)


>>> private_key #doctest: +ELLIPSIS
b'-----BEGIN ENCRYPTED PRIVATE KEY-...

>>> public_key #doctest: +ELLIPSIS
b'-----BEGIN PUBLIC KEY---...




.. !SECTION - Keypair Creation

.. SECTION - Save CSR

>>> from ftwpki.baselibs.core import save_pem

>>> csr_pem = reins_csr.build(load_private_key_from_pem(
...    pem_data=private_key, 
...         passphrase= pwd_man.decrypt_password_file(
...             encrypted_filename= args.passphrasefile,
...             password = password
... ))).get_pem()

>>> del password


>>> save_pem(csr_pem, Path(f"{args.pki_name + '.csr'}"), is_private=False)


.. !SECTION - Save CSR

.. SECTION - pki- Container

>>> from ftwpki.baselibs.package import PKIPackage

>>> pki_pack = PKIPackage()

>> conf_file



>>> from ftwpki.baselibs.core import load_private_key_from_pem,load_certificate_from_pem

>> private_key_obj = load_private_key_from_pem(pem_data=private_key,
...     passphrase= pwd_man.decrypt_password_file(
...         encrypted_filename= args.passphrasefile,
...         password = stub_getpass("Enter Passphrase:")
... ))
Enter Passphrase:
>>> conf_file = Path(args.conf_file)
>>> pki_pack.additional_files[f"{args.pki_name}.policy"]=conf_file.read_bytes()

>>> pki_pack.additional_files["CA.key.pem"]=private_key



>>> pki_file = pki_pack.save(config.passphrases/ args.pki_name)

>>> conf_file.unlink()


.. !SECTION - pki- Container

.. !SECTION - Stop programm

.. SECTION - Teardown

>> env.clean_home()
>>> env.teardown()

.. !SECTION
