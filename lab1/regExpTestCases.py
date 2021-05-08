testCases = [
    {
        'regExp': 'a',
        'string': 'a',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'a',
        'string': 'aa',
        'expected': False,
        'actual': None
    },
    {
        'regExp': 'a',
        'string': '',
        'expected': False,
        'actual': None
    },

    {
        'regExp': 'ab',
        'string': 'ab',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'ab',
        'string': 'a',
        'expected': False,
        'actual': None
    },
    {
        'regExp': 'ab',
        'string': 'b',
        'expected': False,
        'actual': None
    },
    {
        'regExp': 'ab',
        'string': 'abc',
        'expected': False,
        'actual': None
    },

    {
        'regExp': 'abc',
        'string': 'abc',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'abc',
        'string': 'ab',
        'expected': False,
        'actual': None
    },
    {
        'regExp': 'abc',
        'string': 'a',
        'expected': False,
        'actual': None
    },
    {
        'regExp': 'abc',
        'string': 'abcc',
        'expected': False,
        'actual': None
    },

    {
        'regExp': 'a|b',
        'string': 'a',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'a|b',
        'string': 'b',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'a|b',
        'string': 'ab',
        'expected': False,
        'actual': None
    },

    {
        'regExp': 'ab|bc|cd|de',
        'string': 'ab',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'ab|bc|cd|de',
        'string': 'bc',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'ab|bc|cd|de',
        'string': 'cd',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'ab|bc|cd|de',
        'string': 'de',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'ab|bc|cd|de',
        'string': 'aabbcc',
        'expected': False,
        'actual': None
    },

    {
        'regExp': 'a*',
        'string': '',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'a*',
        'string': 'a',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'a*',
        'string': 'aa',
        'expected': True,
        'actual': None
    },
    {
        'regExp': 'a*',
        'string': 'b',
        'expected': False,
        'actual': None
    },
    {
        'regExp': 'a*',
        'string': 'ab',
        'expected': False,
        'actual': None
    },

    {
        'regExp': '(a|b)*',
        'string': 'a',
        'expected': True,
        'actual': None
    },
    {
        'regExp': '(a|b)*',
        'string': 'b',
        'expected': True,
        'actual': None
    },
    {
        'regExp': '(a|b)*',
        'string': 'ab',
        'expected': True,
        'actual': None
    },
    {
        'regExp': '(a|b)*',
        'string': 'ba',
        'expected': True,
        'actual': None
    },
    {
        'regExp': '(a|b)*',
        'string': 'abab',
        'expected': True,
        'actual': None
    },
    {
        'regExp': '(a|b)*',
        'string': 'aabab',
        'expected': True,
        'actual': None
    }
]
