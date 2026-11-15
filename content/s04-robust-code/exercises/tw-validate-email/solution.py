from solution import validate_email


def test_valid_address():
    assert validate_email("ana@ifood.com") is True


def test_needs_exactly_one_at():
    assert validate_email("ana.ifood.com") is False
    assert validate_email("ana@b@ifood.com") is False


def test_empty_local_part():
    assert validate_email("@ifood.com") is False


def test_domain_dot_rules():
    assert validate_email("ana@ifood") is False
    assert validate_email("ana@.ifood.com") is False
    assert validate_email("ana@ifood.com.") is False
    assert validate_email("a.b@ifood") is False


def test_no_spaces():
    assert validate_email("ana @ifood.com") is False
    assert validate_email("ana@ifood .com") is False
    assert validate_email(" ana@ifood.com") is False
    assert validate_email("ana@ifood.com ") is False
