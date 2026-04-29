Comand Line Parser
###################


>>> from ftwpki.intermed.cli_parser import CSRIntermediateParser

>>> cip = CSRIntermediateParser()
>>> cip #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
CSRIntermediateParser(prog=..., 
    usage=None, 
    description=None, 
    formatter_class=<class 'argparse.HelpFormatter'>, 
    conflict_handler='error', 
    add_help=True)

>>> cip.parse_args(["passwort.txt"]) #doctest: +NORMALIZE_WHITESPACE
Namespace(countryName='', 
    stateOrProvinceName='', 
    localityName='', 
    organizationName='', 
    organizationalUnitName='', 
    commonName='', 
    dnsubject={}, 
    conf_file=None, 
    private_key='', 
    public_key='', 
    privatdir='',
    passphrasefile='passwort.txt')

>>> cip.parse_args(["-subj", "/CN=Test" ,"passwort.txt"]) #doctest: +NORMALIZE_WHITESPACE
Namespace(countryName='', 
    stateOrProvinceName='', 
    localityName='', 
    organizationName='', 
    organizationalUnitName='', 
    commonName='Test', 
    dnsubject={'commonName': 'Test'}, 
    conf_file=None, 
    private_key='',
    public_key='', 
    privatdir='',
    passphrasefile='passwort.txt')

