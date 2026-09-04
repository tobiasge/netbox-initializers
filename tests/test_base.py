import io
from unittest.mock import patch

from netbox_initializers.initializers.base import BaseInitializer


class TestSplitParams:
    def test_default_unique_params(self) -> None:
        initializer = BaseInitializer("")
        params = {"name": "Test Site", "slug": "test-site", "description": "A site"}
        matching, remaining = initializer.split_params(params)

        assert matching == {"name": "Test Site", "slug": "test-site"}
        assert remaining == {"description": "A site"}
        # Verify in-place mutation of input dictionary
        assert params == {"description": "A site"}

    def test_custom_unique_params(self) -> None:
        initializer = BaseInitializer("")
        params = {"cid": "CIR-001", "name": "Link A", "status": "active"}
        matching, remaining = initializer.split_params(params, unique_params=["cid"])

        assert matching == {"cid": "CIR-001"}
        assert remaining == {"name": "Link A", "status": "active"}

    def test_partial_unique_params(self) -> None:
        initializer = BaseInitializer("")
        params = {"name": "Test Site", "description": "Missing slug"}
        matching, remaining = initializer.split_params(params)

        assert matching == {"name": "Test Site"}
        assert "slug" not in matching
        assert remaining == {"description": "Missing slug"}

    def test_no_matching_unique_params(self) -> None:
        initializer = BaseInitializer("")
        params = {"description": "No name or slug"}
        matching, remaining = initializer.split_params(params)

        assert matching == {}
        assert remaining == {"description": "No name or slug"}


class TestPopCustomFields:
    def test_pop_custom_field_data(self) -> None:
        initializer = BaseInitializer("")
        params: dict[str, object] = {"name": "Test", "custom_field_data": {"owner": "admin"}}
        cf_data = initializer.pop_custom_fields(params)

        assert cf_data == {"owner": "admin"}
        assert "custom_field_data" not in params

    def test_pop_deprecated_custom_fields_logs_warning(self) -> None:
        stderr = io.StringIO()
        initializer = BaseInitializer("", stderr=stderr, verbosity=1)
        params: dict[str, object] = {"name": "Test", "custom_fields": {"owner": "admin"}}
        cf_data = initializer.pop_custom_fields(params)

        assert cf_data == {"owner": "admin"}
        assert "custom_fields" not in params
        assert "⚠️ Please rename 'custom_fields' to 'custom_field_data'!" in stderr.getvalue()

    def test_pop_custom_fields_none(self) -> None:
        initializer = BaseInitializer("")
        params: dict[str, object] = {"name": "Test"}
        cf_data = initializer.pop_custom_fields(params)

        assert cf_data is None
        assert params == {"name": "Test"}


class TestLogging:
    def test_log_verbosity_0_suppressed(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        initializer = BaseInitializer("", stdout=stdout, stderr=stderr, verbosity=0)

        initializer.log("info message")
        initializer.log_warning("warning message")
        initializer.log_debug("debug message")

        assert stdout.getvalue() == ""
        assert stderr.getvalue() == ""

    def test_log_verbosity_1_normal(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        initializer = BaseInitializer("", stdout=stdout, stderr=stderr, verbosity=1)

        initializer.log("info message")
        initializer.log_warning("warning message")
        initializer.log_debug("debug message")

        assert "info message" in stdout.getvalue()
        assert "warning message" in stderr.getvalue()
        assert "debug message" not in stdout.getvalue()

    def test_log_verbosity_2_debug(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        initializer = BaseInitializer("", stdout=stdout, stderr=stderr, verbosity=2)

        initializer.log("info message")
        initializer.log_warning("warning message")
        initializer.log_debug("debug message")

        assert "info message" in stdout.getvalue()
        assert "warning message" in stderr.getvalue()
        assert "debug message" in stdout.getvalue()

    def test_log_warning_fallback_to_stdout(self) -> None:
        stdout = io.StringIO()
        initializer = BaseInitializer("", stdout=stdout, stderr=None, verbosity=1)

        initializer.log_warning("warning to stdout")
        assert "warning to stdout" in stdout.getvalue()

    def test_log_fallback_to_print_when_no_streams(self) -> None:
        initializer = BaseInitializer("", stdout=None, stderr=None, verbosity=1)

        with patch("builtins.print") as mock_print:
            initializer.log("printed message")
            mock_print.assert_called_once_with("printed message")

        with patch("builtins.print") as mock_print:
            initializer.log_warning("printed warning")
            mock_print.assert_called_once_with("printed warning")
