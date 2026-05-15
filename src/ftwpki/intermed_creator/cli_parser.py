# File: src/ftwpki/intermed/cli_parser.py
# Author: Fitzz TeXnik Welt
# Email: FitzzTeXnikWelt@t-online.de
# License: LGPLv2 or above
"""
cli_parser
===============================

Parser for Intermediate CA Certificate Signing Requests (CSR). (rw)
"""

from argparse import Namespace
from pathlib import Path
from typing import cast

from ftwpki.baselibs.cli_parser import CSRParser
from ftwpki.intermed_creator.protocols import CSRIntermediateProtocol


# CLASS - CSRIntermediateParser
class CSRIntermediateParser(CSRParser):
    """
    CLI parser for creating Intermediate CA signing requests. (rw)
    """

    def _setup_parser(self) -> None:
        """
        Configure the parser with intermediate-specific arguments. (ro)
        """
        super()._setup_parser()
        self.add_argument(
            "passphrasefile", help="Filename of the encrypted secret for the intermediate key."
        )

    def parse_args(
        self, args: list[str] | None = None, namespace: Namespace | None = None
    ) -> CSRIntermediateProtocol:
        """
        Parse arguments and cast to CSRIntermediateProtocol. (ro)

        :param args: Optional list of argument strings.
        :param namespace: Optional Namespace object.
        :returns: Parsed arguments adhering to the protocol.
        """
        return cast(CSRIntermediateProtocol, super().parse_args(args, namespace))
# !CLASS - CSRIntermediateParser

#FUNCTION - get_csr_intermed_parser()
def get_csr_intermed_parser() -> CSRIntermediateParser:
    """
    Factory function to create and return a configured CSRIntermediateParser instance. (ro)

    :returns: An instance of CSRIntermediateParser.
    """
    parser = CSRIntermediateParser(
        prog="ftwpkiintermedcsr",
        description="Create a Certificate Signing Request (CSR) for an Intermediate CA.",
    )
    return parser
# !FUNCTION - get_csr_intermed_parser()

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
    test_file = testfiles_dir / "get_started_cli_parser.rst"

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
