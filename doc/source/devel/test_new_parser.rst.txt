:orphan:
>>> import sys

>>> from ftwpki.intermed_creator.cli_parser import CSRIntermediateParser,csr_intermediate_parser

>>> from ftwpki.intermed_creator.cli_parser import CSRIntermediateArguments, get_csr_intermed_parser

>>> cip_c=CSRIntermediateParser() #doctest: +SKIP
>>> cip = csr_intermediate_parser()#doctest: +SKIP

>>> cip.print_help(file=sys.stderr) #doctest: +SKIP
>>> cip_c.print_help(file=sys.stderr) #doctest: +SKIP


>>> csr_args = CSRIntermediateArguments() #doctest: +SKIP

>>> csr_args #doctest: +SKIP

>>> csr_intermediate_parser.__doc__ #doctest: +SKIP


>>> cip_f = get_csr_intermed_parser()

>>> cip_f.print_help(file=sys.stderr) #doctest: -SKIP


