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

from ftwpki.baselibs.cert_request import CertificateRequest
from ftwpki.baselibs.cli_parser import TomlPreParser
from ftwpki.baselibs.configuration import IntermedPKIConfig
from ftwpki.baselibs.core import (
    create_csr_name,
    create_distinguished_name,
    generate_rsa_key_pair,
    load_private_key_from_pem,
    save_pem,
)
from ftwpki.baselibs.passwd import PasswordManager
from ftwpki.baselibs.policies import (
    IntermediatePolicy,
)
from ftwpki.baselibs.toml_utils import (
    toml2_dn,
    toml2dn,
)
from ftwpki.intermed_creator.cli_parser import CSRIntermediateParser


# SECTION - Programm Create CSR
def prog_intermediate_csr(argv: list[str] | None = None) -> int:
    """
    Main entry point for generating an Intermediate CA CSR. (rw)

    :param argv: Optional list of command-line arguments.
    :returns: Exit code (0 for success, 1 for error).
    """
    try:
        # SECTION - Configuration
        pre_parser = TomlPreParser()
        pre_args, _ = pre_parser.parse_known_args(argv)
        config: IntermedPKIConfig = IntermedPKIConfig()
        config.set_config("intermed")

        ca_parser = CSRIntermediateParser(prog="ftwpkiintermedcsr")
        ca_parser.set_defaults(**toml2dn(pre_args.conf_file))
        # ca_parser.set_defaults(**toml2_dn(argv))
        args = ca_parser.parse_args(argv)
        # SECTION - Copy passphrasefile
        ppf_in_priv: bool = (config.config_path / args.privatdir / args.passphrasefile).is_file()
        ppf_in_cwd: bool = Path(args.passphrasefile).is_file()
        if ppf_in_cwd and not ppf_in_priv:
            shutil.move(
                Path(args.passphrasefile), config.config_path / args.privatdir / args.passphrasefile
            )
        elif ppf_in_cwd:
            Path(args.passphrasefile).unlink(True)
        # !SECTION - Copy passphrasefile
        # !SECTION - Configuration
        # SECTION - Passwordhandling
        pwd_man = PasswordManager(private_dir=str(config.config_path / args.privatdir))
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
        priv, pub = generate_rsa_key_pair(
            passphrase=pwd_man.decrypt_password_file(
                encrypted_filename=args.passphrasefile,
                password=getpass.getpass("Enter Passphrase:"),
            ),
            key_size=4096,
        )
        # !SECTION - Keypair Creation
        # SECTION - Save Keys and CSR
        save_pem(priv, config.config_path / f"{args.privatdir}/{args.private_key}", is_private=True)
        save_pem(pub, config.data_path / f"{args.public_key}", is_private=False)

        save_pem(
            reins_csr.build(
                load_private_key_from_pem(
                    pem_data=priv,
                    passphrase=pwd_man.decrypt_password_file(
                        encrypted_filename=args.passphrasefile,
                        password=getpass.getpass("Enter Passphrase:"),
                    ),
                )
            ).get_pem(),
            Path(create_csr_name(args.commonName, args.localityName)),
            is_private=False,
        )
        # !SECTION - Save Keys and CSR
        return 0
    except KeyboardInterrupt:
        return 1
    except Exception as e:
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

    # Pfad zu den dokumentierenden Tests
    testfiles_dir = Path(__file__).parents[3] / "doc/source/devel"
    test_file = testfiles_dir / "get_started_programms.rst"
    test_file = testfiles_dir / "get_started_run_programms.rst"
    # test_file = testfiles_dir / "get_started_prog_intermed_sign.rst"

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
