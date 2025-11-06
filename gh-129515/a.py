# import ast

# for stmt in [
#     "x = pass if 1 else 1",
#     "x = break if 1 else 1",
#     "x = continue if 1 else 1",
#     "x = pass if 1 else pass",
#     "x = break if 1 else pass",
#     "x = continue if 1 else pass",
#     "x = continue if 1 else import ast",
#     "x = continue if 1 else a=1",
#     "x = continue if 1 else yield 1",
#     "x = continue if 1 else raise 1",
#     "x = 1 if 1 else local ",
# ]:
#     try:
#         ast.parse(stmt)
#     except Exception as e:
#         import traceback
#         print (e)
#         for _ in traceback.format_exception(e):
#             print (_)

# x = 1 if 1 else pass
x = 1 if 1 else 2

a=1
b=2
x = del a if True else 1
