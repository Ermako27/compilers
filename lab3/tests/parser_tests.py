from unittest import TestCase

from parser import Parser


class ParserTest(TestCase):

    def test1(self):
        p = Parser("~A ! ~B & ~C")
        self.assertEqual(True, p.accept_string())

    def test2(self):
        p = Parser("~B")
        self.assertEqual(True, p.accept_string())

    def test3(self):
        p = Parser("~A | C")
        self.assertEqual(False, p.accept_string())

    def test4(self):
        p = Parser("A true")
        self.assertEqual(False, p.accept_string())

    def test5(self):
        p = Parser("true & ~true")
        self.assertEqual(True, p.accept_string())

    def test6(self):
        p = Parser("A & ~ CDD & true")
        self.assertEqual(True, p.accept_string())

    def test7(self):
        p = Parser("true")
        self.assertEqual(True, p.accept_string())

    def test8(self):
        p = Parser("falsse")
        self.assertEqual(False, p.accept_string())

    def test9(self):
        p = Parser("1+2*3")
        self.assertEqual(False, p.accept_string())

    def test10(self):
        p = Parser("false & ~ A ! ~true & B")
        self.assertEqual(True, p.accept_string())
