"""
Tests for diko CLI interface
"""

import tempfile
import os
from click.testing import CliRunner

from diko.cli import main, load_library
from diko.utils import sha256sum


class TestCLI:
    def setup_method(self):
        self.runner = CliRunner()

    def test_version(self):
        result = self.runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_help(self):
        result = self.runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "diko" in result.output

    def test_list_command(self):
        result = self.runner.invoke(main, ["list"])
        assert result.exit_code == 0
        assert "Available distributions" in result.output
        assert "ubuntu" in result.output
        assert "debian" in result.output

    def test_load_library(self):
        library = load_library()
        assert isinstance(library, dict)
        assert "ubuntu" in library
        ubuntu = library["ubuntu"]
        assert "name" in ubuntu
        assert "mirrors" in ubuntu and isinstance(ubuntu["mirrors"], list)


class TestUtils:
    def test_sha256sum(self):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
            f.write("Hello, World!")
            temp_file = f.name
        try:
            result = sha256sum(temp_file)
            assert len(result) == 64
            assert all(c in "0123456789abcdef" for c in result.lower())
            expected = (
                "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
            )
            assert result.lower() == expected
        finally:
            os.unlink(temp_file)