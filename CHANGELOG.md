# Changelog: ftw-pki-intermed (Creator)

All notable changes to this project will be documented in this file.

###### [0.0.4] - 2026-06-17

###### Added
- Introduce temporary DEV components and implement PKIPackage
- Integrate TomlPreParser into intermediate CSR program

###### Changed
- Migrate CLI parser to factory pattern
- Align intermediate CSR tool with unified key-name schema
- Rename legacy TOML functions to modernize utility interfaces
- Refactor CSR creation to use IntermedPKIConfig and secure passphrase handling
- Adapt to streamlined baselibs

###### Fixed
- Integrate help system and improve parser robustness

###### Testing
- Reach 100% total coverage for intermediate creator components

###### Documentation
- Update documentation and remove obsolete parser rst files

## [0.0.3a2] - 2026-05-18

### Fixed
- Make internal documentation doctests fully platform-independent to ensure consistent verification passes across POSIX and non-POSIX development environments.

### Changed
- Finalize project metadata structures and align repository workflows for cleaner package building.


## [0.0.3a1] - 2026-05-15

### Added
- **Standalone Package**: First independent release following the architectural split from the combined intermediate repository.
- **Namespace Transition**: Migrated all modules to `ftwpki.intermed_creator`.
- **Python 3.15 Support**: Verified compatibility and 100% test coverage for the upcoming Python 3.15.

### Changed
- **Version Bump**: Promoted to 0.0.3a1 to reflect the major structural change and separation from the signing logic.
- **CLI Refinement**: Updated project identity to "Intermediate Certificates Request Tool".

### Fixed
- **Namespace Consistency**: Resolved all internal import errors caused by the module rename.

## [0.0.2a1] - 2026-05-06
- **Pre-Split State**: Final version of the combined intermediate logic before separating into standalone packages.

## [0.0.2] - 2026-05-01
- **API Documentation**: Implemented PEP 257 and Sphinx-compliant docstrings for all core modules.

## [0.0.1] - 2024-11-20
- **Initial Commit**: Basic implementation of Intermediate CSR logic.
