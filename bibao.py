def outer(a):
    b = 5

    def inner():
        c = 7
        print(a + b + c)

    return inner


inner_func = outer(3)
inner_func()
print(inner_func.__closure__)
print(inner_func.__closure__[0].cell_contents)
print(inner_func.__closure__[1].cell_contents)

print("=" * 200)

def outer():
    funcs = []

    for k in range(3):
        def inner():
            return k * k
        funcs.append(inner)
    return funcs

f1, f2, f3 = outer()
print(f1.__closure__[0].cell_contents)
print(f2.__closure__[0].cell_contents)
print(f3.__closure__[0].cell_contents)
print(f1())
print(f2())
print(f3())

