from core.chain import Transfiguration
from core.chain import ChainOfTransfiguration
import unittest


class TransfigurationSpell(Transfiguration):

    static_spell_counter = 0

    def __init__(self, identity):
        super().__init__()
        self._name = identity

    def transfigure(self):
        print('[{}] is performing Transfiguration'.format(self._name))
        TransfigurationSpell.static_spell_counter +=1

        if self._next:
            print('{} is next'.format(self._next._name))


class TestTransfigurationSpell(unittest.TestCase):

    def setUp(self):
        print('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        print('Unit Test [{}] Stop'.format(self.id()))

    def test_transfiguration(self):
        one = TransfigurationSpell('Harry Potter')
        two = TransfigurationSpell('Ron Weasley')
        three = TransfigurationSpell('Hermione Granger')

        one.set_next(two)
        two.set_next(three)

        self.assertEqual(one.get_next(), two)
        self.assertEqual(two.get_next(), three)

    def test_chain(self):
        one = TransfigurationSpell('Harry Potter')
        two = TransfigurationSpell('Ron Weasley')
        three = TransfigurationSpell('Hermione Granger')

        one.set_next(two)
        two.set_next(three)

        chain = ChainOfTransfiguration(one)
        chain.execute()

        self.assertEqual(TransfigurationSpell.static_spell_counter, 3)

if __name__ == '__main__':
    unittest.main()