from solution import is_valid_ip


def test_valid():
    assert is_valid_ip("192.168.0.1")
    assert is_valid_ip("0.0.0.0")
    assert is_valid_ip("255.255.255.255")


def test_wrong_part_count():
    assert not is_valid_ip("1.2.3")
    assert not is_valid_ip("1.2.3.4.5")


def test_out_of_range():
    assert not is_valid_ip("256.1.1.1")
    assert not is_valid_ip("1.1.1.300")


def test_leading_zero():
    assert not is_valid_ip("192.168.01.1")
    assert not is_valid_ip("00.1.1.1")


def test_bad_characters_and_empty():
    assert not is_valid_ip("")
    assert not is_valid_ip("a.b.c.d")
    assert not is_valid_ip("1.2.3.-4")
    assert not is_valid_ip("1..2.3")
    assert not is_valid_ip("1.2.3. 4")


def test_signs_and_non_ascii_digits():
    assert not is_valid_ip("+1.2.3.4")
    assert not is_valid_ip("1.2.3.4 ")
    assert not is_valid_ip("１.2.3.4")
    assert not is_valid_ip("1.2.3.²")


def test_longer_leading_zeros():
    assert not is_valid_ip("000.1.1.1")
    assert not is_valid_ip("1.2.3.007")
    assert not is_valid_ip("1.2.3.00")


def test_other_formats_rejected():
    assert not is_valid_ip("::1")
    assert not is_valid_ip("1:2:3:4")
    assert not is_valid_ip("1,2,3,4")
    assert not is_valid_ip("1_0.2.3.4")
    assert not is_valid_ip("1.2.3.4a")
    assert not is_valid_ip("0x1.2.3.4")
    assert not is_valid_ip("1.2.3.4\n")


def test_more_valid():
    assert is_valid_ip("10.20.30.40")
    assert is_valid_ip("249.250.251.252")
    assert is_valid_ip("1.2.3.0")
