"""Test the Path class."""

from tuya_vacuum.map.path import Path


def test_vacuum_path_header_v12():
    """Test how a version 12 vacuum path header is parsed.

    Captured from a Kabum "Robô Aspirador de Pó 700", a rebranded Tuya
    vacuum whose path data is always uncompressed and has a shorter header
    than other versions (no total_count/theta/length_after_compression
    fields).
    """

    with open("./tests/path_12.bin", "rb") as file:
        data = file.read()

        path = Path(data)

        assert path.version == 12


def test_vacuum_path_body_v12():
    """Test how a version 12 vacuum path body is parsed."""

    with open("./tests/path_12.bin", "rb") as file:
        data = file.read()

        path = Path(data)

        assert len(path._path_data) == 2790
        assert path._path_data[0] == {"x": 2.3, "y": -23.0}
        assert path._path_data[-1] == {"x": 3.6, "y": -24.7}

        # Should not raise.
        path.to_image(459, 240, (104.0, 65.0))
