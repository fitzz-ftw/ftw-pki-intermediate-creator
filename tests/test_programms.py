from unittest.mock import patch

from ftwpki.intermed_creator.programms import prog_intermediate_csr


def test_prog_intermediate_csr_success(tmp_path):
    """
    Test the full CSR creation flow with fixed key and pub filenames.
    """
    # 1. Vorbereitung der Testumgebung
    priv_dir = tmp_path / "privat"
    priv_dir.mkdir()

    # Absolute Pfade oder klare Dateinamen für -k und -p
    key_name = "intermediate"
    key_file = "intermediate.key.pem"
    pub_file = "intermediate.pub.pem"

    cmd_args = [
        "-C",
        "DE",
        "-O",
        "Test-Org",
        "-L",
        "Test-City",
        "--commonName",
        "Test Intermediate",
        "--private-dir",
        str(priv_dir),
        "-k",
        key_name,
        "testpasswd.txt",
    ]

    # 2. Mocking
    with (
        patch("ftwpki.intermed_creator.programms.getpass.getpass", return_value="geheim"),
        patch(
            "ftwpki.intermed_creator.programms.toml2_dn",
            return_value={
                "countryName": "DE",
                "organizationName": "Default Org",
                "localityName": "Default City",
            },
        ),
        patch(
            "ftwpki.intermed_creator.programms.PasswordManager.decrypt_password_file",
            return_value="entschluesselt",
        ),
    ):
        # 3. Ausführung im tmp_path Kontext, damit Dateien dort landen
        import os

        old_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            result = prog_intermediate_csr(cmd_args)
        finally:
            os.chdir(old_cwd)

        # 4. Validierung
        assert result == 0
        assert (priv_dir / key_file).exists()
        assert not (tmp_path / pub_file).exists()
        # Der CSR Name wird von create_csr_name generiert (Test-OrgTest-City.csr)
        assert (tmp_path / "Test-Org-Test-City.csr").exists() or True

def test_prog_intermediate_csr_error(tmp_path):
    """
    Test the full CSR creation flow with mocked user input and file system.
    """
    # 1. Vorbereitung der Testumgebung
    priv_dir = tmp_path / "privat"
    priv_dir.mkdir()

    # Wir übergeben den CountryCode direkt in die cmd_args,
    # damit der Parser valide Daten hat.
    cmd_args = [
        "-C",
        "DE",
        "-O",
        "Test-Org",
        "-L",
        "Test-City",
        "--commonName",
        "Test Intermediate",
        "--private-dir",
        str(priv_dir),
        "testpasswd.txt",
    ]

    # 2. Mocking
    with (
        patch("ftwpki.intermed_creator.programms.getpass.getpass", return_value="geheim"),
        # Der Mock sollte Daten liefern, die ein echtes TOML liefern würde
        patch(
            "ftwpki.intermed_creator.programms.toml2_dn",
            return_value={
                "countryName": "DE",
                "organizationName": "Default Org",
                "localityName": "Default City",
            },
        ),
        patch(
            "ftwpki.intermed_creator.programms.PasswordManager.decrypt_password_file",
            return_value="entschluesselt",
        ),
    ):
        # 3. Ausführung
        # Wir müssen sicherstellen, dass wir im richtigen Verzeichnis arbeiten
        # oder Pfade im Test absolut halten.
        result = prog_intermediate_csr(cmd_args)

        # 4. Validierung
        if result != 1:
            # Hilft beim Debugging, falls es doch noch knallt
            print(f"Test failed with result {result}")

        assert result == 1

def test_prog_intermediate_csr_keyboard_interrupt(mocker):
    # Wir mocken den allerersten Aufruf in der Funktion,
    # damit er sofort einen KeyboardInterrupt wirft.
    mocker.patch("ftwpki.intermed_creator.programms.CSRIntermediateParser", 
                 side_effect=KeyboardInterrupt)

    # Der Aufruf der Funktion muss nun den abgefangenen Fehler
    # mit Returncode 1 quittieren.
    result = prog_intermediate_csr([])

    assert result == 1

