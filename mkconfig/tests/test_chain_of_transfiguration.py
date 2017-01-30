from mkconfig.core.transfig import Transfiguration, ContextAwareTransfiguration
from mkconfig.core.chain import ChainOfTransfiguration
import unittest
from mkconfig.core.error import IllegalStateException
import logging
import mkconfig.env


logger = logging.getLogger(__name__)


class TransfigurationSpell(Transfiguration):

    static_spell_counter = 0

    def __init__(self, identity):
        super().__init__()
        self._name = identity

    def perform(self, context):
        logger.info('[{}] is performing Transfiguration'.format(self._name))
        TransfigurationSpell.static_spell_counter +=1


class AdditiveContextAwareTransfiguration(ContextAwareTransfiguration):

    _number = 0

    def __init__(self, number):
        super().__init__()
        self._number = number

    def perform(self, context):
        if 'answer' in context :
            context['answer'] += self._number
        else :
            raise IllegalStateException("Context['answer'] does not exist!")

        return context


class TestTransfigurationSpell(unittest.TestCase):

    def setUp(self):
        logger.info('Unit Test [{}] Start'.format(self.id()))

    def tearDown(self):
        logger.info('Unit Test [{}] Stop'.format(self.id()))

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

    def test_functional_chain_piping(self):
        one = AdditiveContextAwareTransfiguration(1)
        two = AdditiveContextAwareTransfiguration(2)
        three = AdditiveContextAwareTransfiguration(3)

        chain = ChainOfTransfiguration()
        chain.add(one)
        chain.add(two)
        chain.add(three)

        context = {'answer' : 0}
        chain.execute(context)

        self.assertEqual(6, context['answer'])


if __name__ == '__main__':
    unittest.main()