# flatten a list of lists
list_of_lists = [[1, 2], [3], [4, 5], [6, 7, 8]]
sum(list_of_lists, [])
[1, 2, 3, 4, 5, 6, 7, 8]

# more explicit
import itertools
list(itertools.chain(*list_of_lists))
[1, 2, 3, 4, 5, 6, 7, 8]

#not recursive though
list_of_lists = [[1, 2], [3], [4, 5], [6, 7, 8, [1, [2, [3, 4]]]]]
list(itertools.chain(*list_of_lists)) # or itertools.chain.from_iterable
[1, 2, 3, 4, 5, 6, 7, 8, [1, [2, [3, 4]]]]