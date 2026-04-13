# File: src/ftwpki/intermed/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================


Modul programms documentation
"""
import getpass
from pathlib import Path

from ftwpki.baselibs.core import (
    create_csr_name,
    create_distinguished_name,
    generate_rsa_key_pair,
    load_private_key_from_pem,
    save_pem,
)
from ftwpki.baselibs.passwd import PasswordManager
from ftwpki.baselibs.policies import IntermediatePolicy
from ftwpki.baselibs.request import CertificateRequset
from ftwpki.baselibs.utils import toml2dn
from ftwpki.intermed.cli_parser import CSRIntermediateParser


def prog_intermediate_csr(argv:list[str]|None=None) ->int:
    try:
        ca_parser = CSRIntermediateParser(prog="ftwpkicsrinter")
        ca_parser.set_defaults(**toml2dn(argv))
        args = ca_parser.parse_args(argv)
        pwd_man = PasswordManager(private_dir=args.privatdir)
        subject = create_distinguished_name(
                 country=args.countryName,
                 state=args.stateOrProvinceName,
                 location=args.localityName,
                 organization=args.organizationName,
                 common_name=args.commonName,
                 organizational_unit=args.organizationalUnitName,
             )

        reins_csr = CertificateRequset(
                             subject = subject,
                             policy = IntermediatePolicy(),
                         )
        priv, pub = generate_rsa_key_pair(passphrase=pwd_man.decrypt_password_file(
                         encrypted_filename= args.passphrasefile,
                         password = getpass.getpass("Enter Passphrase:")
                 ), key_size=4096)
        save_pem(priv, 
                 Path(f"{args.privatdir}/{args.private_key}"), 
                 is_private=True)
        save_pem(pub, Path(f"{args.public_key}"), is_private=False)

        save_pem(reins_csr.build(load_private_key_from_pem(
                            pem_data=priv, 
                            passphrase= pwd_man.decrypt_password_file(
                            encrypted_filename= args.passphrasefile,
                            password = getpass.getpass("Enter Passphrase:")
                     ))).get_pem(), 
                     Path(create_csr_name(args.organizationName, args.localityName)), 
                     is_private=False)

        return 0
    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__": # pragma: no cover
    from doctest import FAIL_FAST, testfile
    
    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    
    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_file = testfiles_dir / "get_started_programms.rst"
    
    if test_file.exists():
        print(f"--- Running Doctest for {test_file.name} ---")
        doctestresult = testfile(
            str(test_file),
            module_relative=False,
            verbose=be_verbose,
            optionflags=option_flags,
        )
        test_failed += doctestresult.failed
        test_sum += doctestresult.attempted
        if test_failed == 0:
            print(f"\nDocTests passed without errors, {test_sum} tests.")
        else:
            print(f"\nDocTests failed: {test_failed} tests.")
    else:
        print(f"⚠️ Warning: Test file {test_file.name} not found.")
