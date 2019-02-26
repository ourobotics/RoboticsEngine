from functools import partial
def hello(var1, var2):
    print("hello")
    print(var1, var2)

x = {
    "test": "hello"
}

var1 = "rewq"
var2 = "fdsa"

y = {
    "test": (var1, var2)
}

# print(x["test"])
# print(y["test"])

# x["test"](y["test"])
# hello(var1,var2, "var3")
func = partial(hello, var1, var2)
func()