# File: src/ftwpki/intermed/programms.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
programms
===============================

Main entry points for Intermediate CA operations. (rw)
"""

import getpass
import shutil
from pathlib import Path

from ftwpki.baselibs._cli_parser import PKIBaseParser
from ftwpki.baselibs.cert_request import CertificateRequest
from ftwpki.baselibs.configuration import IntermedPKIConfig
from ftwpki.baselibs.core import (
    create_distinguished_name,
    generate_rsa_key_pair,
    load_private_key_from_pem,
    save_pem,
)
from ftwpki.baselibs.package import PKIPackage
from ftwpki.baselibs.passwd import PasswordManager
from ftwpki.baselibs.policies import (
    IntermediatePolicy,
)
from ftwpki.baselibs.toml_utils import (
    toml2dn,
)
from ftwpki.intermed_creator.cli_parser import (
    CSRInt,
    CSRIntermediateParser,
)


# SECTION - Programm Create CSR
def prog_intermediate_csr(argv: list[str] | None = None) -> int:
    """
    Main entry point for generating an Intermediate CA CSR. (rw)

    :param argv: Optional list of command-line arguments.
    :returns: Exit code (0 for success, 1 for error).
    """
    try:
        # SECTION - Configuration
        pre_parser: PKIBaseParser[CSRInt] = CSRIntermediateParser(
             add_help=False, allow_abbrev=False
        )
        pre_args, _ = pre_parser.parse_known_args(argv)
        pre_conf =  {}
        if pre_args.conf_file:
            pki_name = Path(pre_args.conf_file).stem
            pre_conf = toml2dn(Path(pre_args.conf_file).read_text())
            pre_conf["pki_name"] = pki_name
        ca_parser: PKIBaseParser[CSRInt] = CSRIntermediateParser(
            
        )
        ca_parser.set_defaults(**pre_conf)
        args = ca_parser.parse_args(argv)
        config: IntermedPKIConfig = IntermedPKIConfig()

       # SECTION - Copy passphrasefile
        ppf_in_priv: bool = (config.passphrases / args.passphrasefile).is_file()
        ppf_in_cwd: bool = Path(args.passphrasefile).is_file()
        if ppf_in_cwd and not ppf_in_priv:
            shutil.move(Path(args.passphrasefile), config.passphrases / args.passphrasefile)
        elif ppf_in_cwd:
            Path(args.passphrasefile).unlink(True)
        # !SECTION - Copy passphrasefile
        # !SECTION - Configuration
        # SECTION - Passwordhandling
        pwd_man = PasswordManager(private_dir=str(config.passphrases))
        # !SECTION - Passwordhandling
        # SECTION - CSR Creation
        subject = create_distinguished_name(
            country=args.countryName,
            state=args.stateOrProvinceName,
            location=args.localityName,
            organization=args.organizationName,
            common_name=args.commonName,
            organizational_unit=args.organizationalUnitName,
        )
        reins_csr = CertificateRequest(
            subject=subject,
            policy=IntermediatePolicy(),
        )
        # SECTION - CSR Creation
        # SECTION - Keypair Creation
        password =getpass.getpass("Enter Password:")
        private_key, public_key = generate_rsa_key_pair(
            passphrase=pwd_man.decrypt_password_file(
                encrypted_filename=args.passphrasefile,
                password=password,
            ),
            key_size=4096,
        )
        # !SECTION - Keypair Creation
        # SECTION - Save CSR

        csr_pem = reins_csr.build(
                load_private_key_from_pem(
                    pem_data=private_key,
                    passphrase=pwd_man.decrypt_password_file(
                        encrypted_filename=args.passphrasefile,
                        password=password,
                    ),
                )
            ).get_pem()
        del password
        save_pem(csr_pem, Path(f"{args.pki_name + '.csr'}"), is_private=False)
        # !SECTION - Save  CSR
        # SECTION - pki - Container
        pki_pack = PKIPackage()
        conf_file = Path(args.conf_file)
        pki_pack.additional_files[f"{args.pki_name}.policy"] = conf_file.read_bytes()
        pki_pack.additional_files["CA.key.pem"] = private_key
        pki_pack.save(config.passphrases / args.pki_name)
        conf_file.unlink()
        # !SECTION - pki- Container
        return 0
    except KeyboardInterrupt:
        return 1
    except BaseException as e:
        # traceback.print_exc()
        print(e)
        return 1


# !SECTION - Programm Create CSR


if __name__ == "__main__":  # pragma: no cover
    from doctest import FAIL_FAST, testfile

    be_verbose = False
    be_verbose = True
    option_flags = 0
    option_flags = FAIL_FAST
    test_sum = 0
    test_failed = 0
    passed_files = 0

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"

    test_files = [
        "get_started_programms.rst",
        "get_started_run_programms.rst",
        "get_started_run_programms_infra.rst",
        "get_started_run_programms_member.rst",
    ]
    for file in test_files:
        test_file = testfiles_dir / file
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
            if doctestresult.failed > 0 and option_flags & FAIL_FAST:
                print(f"Doctest result for {test_file.name}: {doctestresult}")
                print(
                    f"\nKeep going! You already passed {passed_files} files "
                    f"with {test_sum} tests before this hit."
                )
                break  # Stop on first failure if FAIL_FAST is set
            passed_files += 1
        else:
            print(f"⚠️ Warning: Test file {test_file.name} not found.")
    if test_failed == 0:
        print(f"\nDocTests passed without errors, {test_sum} tests.")
    else:
        if not option_flags & FAIL_FAST:
            print(f"\nDocTests failed: {test_failed} tests out of {test_sum}.")
