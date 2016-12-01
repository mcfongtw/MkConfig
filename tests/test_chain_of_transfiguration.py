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


class TestTransfigurationSpell(unittest.TestCase):

    def setUp(self):
        print('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        print('Unit Test [{}] Stop'.format(self.id()))

    def test_functional_chain(self):
        one = TransfigurationSpell('Harry Potter')
        two = TransfigurationSpell('Ron Weasley')
        three = TransfigurationSpell('Hermione Granger')

        chain = ChainOfTransfiguration()
        chain.add(one)
        chain.add(two)
        chain.add(three)

        self.assertEqual(one, chain.get(0))
        self.assertEqual(two, chain.get(1))
        self.assertEqual(three, chain.get(2))
        self.assertEqual(3, chain.size())

        chain.execute()

        self.assertEqual(TransfigurationSpell.static_spell_counter, 3)

if __name__ == '__main__':
    unittest.main()