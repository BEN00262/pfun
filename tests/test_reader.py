from .monad_test import MonadTest
from .strategies import anything, unaries, readers
from hypothesis import given, assume
from pfun import reader, identity, compose


class TestReader(MonadTest):
    @given(anything(), anything())
    def test_right_identity_law(self, value, context):
        assert (reader.value(value).and_then(reader.value).run(context) ==
                reader.value(value).run(context))

    @given(unaries(readers()), anything(), anything())
    def test_left_identity_law(self, f, value, context):
        assert (reader.value(value).and_then(f).run(context) ==
                f(value).run(context))

    @given(readers(), unaries(readers()), unaries(readers()), anything())
    def test_associativity_law(self, r, f, g, context):
        assert (r.and_then(f).and_then(g).run(context) ==
                r.and_then(lambda x: f(x).and_then(g)).run(context))

    @given(anything(), anything())
    def test_equality(self, value, context):
        assert reader.value(value).run(context) == reader.value(value).run(context)

    @given(anything(), anything(), anything())
    def test_inequality(self, first, second, context):
        assume(first != second)
        assert reader.pure(first)(context) != reader.pure(second)(context)

    @given(anything(), anything())
    def test_identity_law(self, value, context):
        assert (reader.pure(value).map(identity)(context) ==
                reader.pure(value)(context))

    @given(unaries(), unaries(), anything(), anything())
    def test_composition_law(self, f, g, value, context):
        h = compose(f, g)
        assert (reader.pure(value).map(h)(context) ==
                (reader.pure(value).map(g).map(f))(context))