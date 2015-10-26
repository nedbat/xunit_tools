"""Python classes to help with xunit.xml structure."""


class Summable(object):
    """An object whose attributes can be added together easily.

    Subclass this and define `fields` on your derived class.

    """
    def __init__(self):
        for name in self.fields:
            setattr(self, name, 0)

    @classmethod
    def from_element(cls, element):
        """Construct a Summable from an xml element with the same attributes."""
        self = cls()
        for name in self.fields:
            setattr(self, name, int(element.get(name)))
        return self

    def __add__(self, other):
        result = type(self)()
        for name in self.fields:
            setattr(result, name, getattr(self, name) + getattr(other, name))
        return result


class TestResults(Summable):
    """A test result, makeable from a nosetests.xml <testsuite> element."""

    fields = ["tests", "errors", "failures", "skip"]

    def __str__(self):
        msg = "{0.tests:4d} tests, {0.errors} errors, {0.failures} failures, {0.skip} skipped"
        return msg.format(self)
