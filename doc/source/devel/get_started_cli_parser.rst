Comand Line Parser
###################


>>> from ftwpki.intermed_creator.cli_parser import CSRIntermediateParser

>>> cip = CSRIntermediateParser()
>>> cip #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
PKIBaseParser(prog='...', 
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
CSRIntermediateArguments(commonName=''
    conf_file='Testfile.toml'
    countryName=''
    dnsubject={}
    key_name='testkey'
    localityName=''
    organizationName=''
    organizationalUnitName=''
    passphrasefile='passwort.txt'
    pki_name=''
    privatdir=''
    stateOrProvinceName='')

>>> cip.parse_args(required + ["-subj", "/CN=Test" ,"passwort.txt"]) #doctest: +NORMALIZE_WHITESPACE
CSRIntermediateArguments(commonName='Test'
    conf_file='Testfile.toml'
    countryName=''
    dnsubject={'commonName': 'Test'}
    key_name='testkey'
    localityName=''
    organizationName=''
    organizationalUnitName=''
    passphrasefile='passwort.txt'
    pki_name=''
    privatdir=''
    stateOrProvinceName='')


>>> from ftwpki.intermed_creator.cli_parser import get_csr_intermed_parser
>>> get_csr_intermed_parser() #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
PKIBaseParser(prog='ftwpkiintermedcsr', 
    usage=None, 
    description='Create a Certificate Signing Request (CSR) for an 
                    Intermediate CA.', 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)


