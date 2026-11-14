from solution import title_case


def test_basic():
    assert title_case("hELLO wORLD") == "Hello World"


def test_single_letter_words():
    assert title_case("a b c") == "A B C"


def test_keeps_spaces():
    assert title_case("a  b") == "A  B"


def test_empty():
    assert title_case("") == ""


def test_apostrophe_and_edge_spaces():
    assert title_case("o'neil mcDONALD") == "O'neil Mcdonald"
    assert title_case(" a ") == " A "
