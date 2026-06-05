Comand Line Parser
###################


>>> from ftwpki.intermed_creator.cli_parser import CSRIntermediateParser

>>> cip = CSRIntermediateParser()
>>> cip #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
CSRIntermediateParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)

>>> cip.parse_args(["passwort.txt"]) #doctest: +NORMALIZE_WHITESPACE
Traceback (most recent call last):
    ...
argparse.ArgumentError: the following arguments are required: --conf-file, -k/--key/--key-name

>>> required = ["-k","testkey", "--conf-file", "Testfile.toml"]

>>> cip.parse_args(required + ["passwort.txt"]) #doctest: +NORMALIZE_WHITESPACE
Namespace(countryName='', 
    stateOrProvinceName='', 
    localityName='', 
    organizationName='', 
    organizationalUnitName='', 
    commonName='', 
    dnsubject={}, 
    conf_file=PosixPath('Testfile.toml'), 
    key_name='testkey',
    pki_name='',
    privatdir='',
    passphrasefile='passwort.txt',
    private_key='testkey.key.pem', 
    public_key='testkey.pub.pem')

>>> cip.parse_args(required + ["-subj", "/CN=Test" ,"passwort.txt"]) #doctest: +NORMALIZE_WHITESPACE
Namespace(countryName='', 
    stateOrProvinceName='', 
    localityName='', 
    organizationName='', 
    organizationalUnitName='', 
    commonName='Test', 
    dnsubject={'commonName': 'Test'}, 
    conf_file=PosixPath('Testfile.toml'), 
    key_name='testkey',
    pki_name='',
    privatdir='',
    passphrasefile='passwort.txt',
    private_key='testkey.key.pem', 
    public_key='testkey.pub.pem')


>>> from ftwpki.intermed_creator.cli_parser import get_csr_intermed_parser
>>> get_csr_intermed_parser() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
CSRIntermediateParser(prog='...', 
    usage=None, 
    description='...', 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)


>>> cip = CSRIntermediateParser(run_setup=False)
>>> cip #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
CSRIntermediateParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)
