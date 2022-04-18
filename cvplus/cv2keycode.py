from __future__ import annotations

from enum import Enum


class KeyCodes(Enum):
    key0 = ord("0")
    key1 = ord("1")
    key2 = ord("2")
    key3 = ord("3")
    key4 = ord("4")
    key5 = ord("5")
    key6 = ord("6")
    key7 = ord("7")
    key8 = ord("8")
    key9 = ord("9")

    a = ord("a")
    b = ord("b")
    c = ord("c")
    d = ord("d")
    e = ord("e")
    f = ord("f")
    g = ord("g")
    h = ord("h")
    i = ord("i")
    j = ord("j")
    k = ord("k")
    l = ord("l")  # noqa: E741
    m = ord("m")
    n = ord("n")
    o = ord("o")
    p = ord("p")
    q = ord("q")
    r = ord("r")
    s = ord("s")
    t = ord("t")
    u = ord("u")
    v = ord("v")
    w = ord("w")
    x = ord("x")
    y = ord("y")
    z = ord("z")

    connma = ord(",")

    esc = 0x1B
    space = ord(" ")
    enter = 0xD
    backspace = 0x8
