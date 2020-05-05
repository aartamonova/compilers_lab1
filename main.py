from smc.dfa import DfaNfa
from smc.nfa import NfaRegex


def check_chain(regex, chain):
    nfa = NfaRegex(regex)
    nfa.build()
    nfa.nfa.draw()
    dfa = DfaNfa(nfa.nfa)
    dfa.build()
    dfa.dfa.draw()
    dfa.minimize()
    dfa.run(chain)


if __name__ == '__main__':
    test_regex = '(a|b)*abb'
    test_chain = 'ababab'
    check_chain(test_regex, test_chain)
