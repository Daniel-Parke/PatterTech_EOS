"""emailkit: address validation that agrees with the mail servers."""

import netcheck

__version__ = "2.4.1"


class InvalidAddress(ValueError):
    """The address will not deliver."""


def normalise(address):
    """Trim and case fold the domain half."""
    address = (address or "").strip()
    if address.count("@") != 1:
        return address
    local, domain = address.split("@", 1)
    return local + "@" + domain.lower()


def validate(address):
    """Return the normalised address or raise InvalidAddress."""
    address = normalise(address)
    if not address or " " in address or address.count("@") != 1:
        raise InvalidAddress(address)
    local, domain = address.split("@", 1)
    if not local or not domain:
        raise InvalidAddress(address)
    if not netcheck.domain_is_deliverable(domain):
        raise InvalidAddress(address)
    return address


def is_valid(address):
    try:
        validate(address)
    except InvalidAddress:
        return False
    return True
