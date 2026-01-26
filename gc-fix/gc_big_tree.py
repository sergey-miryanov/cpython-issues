import sys
import gc
import random
import time
import collections.abc
import statistics

# perf stat -e L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses ./python gc_big_tree.py
# perf stat -e l3_request_g1.caching_l3_cache_accesses,l3_comb_clstr_state.request_miss ./python gc_big_tree.py


class BNode:
    """
    Instance attributes:
      items: list
      nodes: [BNode]
    """
    __slots__ = ['items', 'nodes']

    minimum_degree = 16 # a.k.a. t

    def __init__(self):
        self.items = []
        self.nodes = None

    def is_leaf(self):
        return self.nodes is None

    def __iter__(self):
        if self.is_leaf():
            for item in self.items:
                yield item
        else:
            for position, item in enumerate(self.items):
                for it in self.nodes[position]:
                    yield it
                yield item
            for it in self.nodes[-1]:
                yield it

    def __reversed__(self):
        if self.is_leaf():
            for item in reversed(self.items):
                yield item
        else:
            for item in reversed(self.nodes[-1]):
                yield item
            for position in range(len(self.items) - 1, -1, -1):
                yield self.items[position]
                for item in reversed(self.nodes[position]):
                    yield item

    def iter_from(self, key):
        position = self.get_position(key)
        if self.is_leaf():
            for item in self.items[position:]:
                yield item
        else:
            for item in self.nodes[position].iter_from(key):
                yield item
            for p in range(position, len(self.items)):
                yield self.items[p]
                for item in self.nodes[p + 1]:
                    yield item

    def iter_backward_from(self, key):
        position = self.get_position(key)
        if self.is_leaf():
            for item in reversed(self.items[:position]):
                yield item
        else:
            for item in self.nodes[position].iter_backward_from(key):
                yield item
            for p in range(position - 1, -1, -1):
                yield self.items[p]
                for item in reversed(self.nodes[p]):
                    yield item

    def is_full(self):
        return len(self.items) == 2 * self.minimum_degree - 1

    def get_position(self, key):
        for position, item in enumerate(self.items):
            if item[0] >= key:
                return position
        return len(self.items)

    def search(self, key):
        """(key:anything) -> None | (key:anything, value:anything)
        Return the matching pair, or None.
        """
        position = self.get_position(key)
        if position < len(self.items) and self.items[position][0] == key:
            return self.items[position]
        elif self.is_leaf():
            return None
        else:
            return self.nodes[position].search(key)

    def insert_item(self, item):
        """(item:(key:anything, value:anything))
        """
        assert not self.is_full()
        key = item[0]
        position = self.get_position(key)
        if position < len(self.items) and self.items[position][0] == key:
            self.items[position] = item
        elif self.is_leaf():
            self.items.insert(position, item)
        else:
            child = self.nodes[position]
            if child.is_full():
                self.split_child(position, child)
                if key == self.items[position][0]:
                     self.items[position] = item
                else:
                     if key > self.items[position][0]:
                         position += 1
                     self.nodes[position].insert_item(item)
            else:
                self.nodes[position].insert_item(item)

    def split_child(self, position, child):
        """(position:int, child:BNode)
        """
        assert not self.is_full()
        assert not self.is_leaf()
        assert self.nodes[position] is child
        assert child.is_full()
        bigger = self.__class__()
        middle = self.minimum_degree - 1
        splitting_key = child.items[middle]
        bigger.items = child.items[middle + 1:]
        child.items = child.items[:middle]
        assert len(bigger.items) == len(child.items)
        if not child.is_leaf():
            bigger.nodes = child.nodes[middle + 1:]
            child.nodes = child.nodes[:middle + 1]
            assert len(bigger.nodes) == len(child.nodes)
        self.items.insert(position, splitting_key)
        self.nodes.insert(position + 1, bigger)

    def get_min_item(self):
        """() -> (key:anything, value:anything)
        Return the item with the minimal key.
        """
        if self.is_leaf():
            return self.items[0]
        else:
            return self.nodes[0].get_min_item()

    def get_max_item(self):
        """() -> (key:anything, value:anything)
        Return the item with the maximal key.
        """
        if self.is_leaf():
            return self.items[-1]
        else:
            return self.nodes[-1].get_max_item()

    def get_count(self):
        """() -> int
        How many items are stored in this node and descendants?
        """
        result = len(self.items)
        for node in self.nodes or []:
            result += node.get_count()
        return result

    def get_node_count(self):
        """() -> int
        How many nodes are here, including descendants?
        """
        result = 1
        for node in self.nodes or []:
            result += node.get_node_count()
        return result

    def get_level(self):
        """() -> int
        How many levels of nodes are there between this node
        and descendant leaf nodes?
        """
        if self.is_leaf():
            return 0
        else:
            return 1 + self.nodes[0].get_level()

    def delete(self, key):
        """(key:anything)
        Delete the item with this key.
        This is intended to follow the description in 19.3 of
        'Introduction to Algorithms' by Cormen, Lieserson, and Rivest.
        """
        def is_big(node):
            # Precondition for recursively calling node.delete(key).
            return node and len(node.items) >= node.minimum_degree
        p = self.get_position(key)
        matches = p < len(self.items) and self.items[p][0] == key
        if self.is_leaf():
            if matches:
                # Case 1.
                del self.items[p]
            else:
                raise KeyError(key)
        else:
            node = self.nodes[p]
            lower_sibling = p > 0 and self.nodes[p - 1]
            upper_sibling = p < len(self.nodes) - 1 and self.nodes[p + 1]
            if matches:
                # Case 2.
                if is_big(node):
                    # Case 2a.
                    extreme = node.get_max_item()
                    node.delete(extreme[0])
                    self.items[p] = extreme
                elif is_big(upper_sibling):
                    # Case 2b.
                    extreme = upper_sibling.get_min_item()
                    upper_sibling.delete(extreme[0])
                    self.items[p] = extreme
                else:
                    # Case 2c.
                    extreme = upper_sibling.get_min_item()
                    upper_sibling.delete(extreme[0])
                    node.items = node.items + [extreme] + upper_sibling.items
                    if not node.is_leaf():
                        node.nodes = node.nodes + upper_sibling.nodes
                    del self.items[p]
                    del self.nodes[p + 1]
            else:
                if not is_big(node):
                    if is_big(lower_sibling):
                        # Case 3a1: Shift an item from lower_sibling.
                        node.items.insert(0, self.items[p - 1])
                        self.items[p - 1] = lower_sibling.items[-1]
                        del lower_sibling.items[-1]
                        if not node.is_leaf():
                            node.nodes.insert(0, lower_sibling.nodes[-1])
                            del lower_sibling.nodes[-1]
                    elif is_big(upper_sibling):
                        # Case 3a2: Shift an item from upper_sibling.
                        node.items.append(self.items[p])
                        self.items[p] = upper_sibling.items[0]
                        del upper_sibling.items[0]
                        if not node.is_leaf():
                            node.nodes.append(upper_sibling.nodes[0])
                            del upper_sibling.nodes[0]
                    elif lower_sibling:
                        # Case 3b1: Merge with lower_sibling
                        node.items = (lower_sibling.items + [self.items[p-1]] +
                                      node.items)
                        if not node.is_leaf():
                            node.nodes = lower_sibling.nodes + node.nodes
                        del self.items[p-1]
                        del self.nodes[p-1]
                    else:
                        # Case 3b2: Merge with upper_sibling
                        node.items = (node.items + [self.items[p]] +
                                      upper_sibling.items)
                        if not node.is_leaf():
                            node.nodes = node.nodes + upper_sibling.nodes
                        del self.items[p]
                        del self.nodes[p+1]
                assert is_big(node)
                node.delete(key)
            if not self.items:
                # This can happen when self is the root node.
                self.items = self.nodes[0].items
                self.nodes = self.nodes[0].nodes


class BTree(collections.abc.MutableMapping):
    """
    Instance attributes:
      root: BNode
    """
    __slots__ = ['root']

    def __init__(self, node_constructor=BNode):
        assert issubclass(node_constructor, BNode)
        self.root = node_constructor()

    def __nonzero__(self):
        return bool(self.root.items)

    __bool__ = __nonzero__

    def iteritems(self):
        for item in self.root:
            yield item

    def iterkeys(self):
        for item in self.root:
            yield item[0]

    def itervalues(self):
        for item in self.root:
            yield item[1]

    def items(self):
        return list(self.iteritems())

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def __iter__(self):
        for key in self.iterkeys():
            yield key

    def __reversed__(self):
        for item in reversed(self.root):
            yield item[0]

    def __contains__(self, key):
        return self.root.search(key) is not None

    def has_key(self, key):
        return self.root.search(key) is not None

    def __setitem__(self, key, value):
        self.add(key, value)

    def setdefault(self, key, value):
        item = self.root.search(key)
        if item is None:
            self.add(key, value)
            return value
        return item[1]

    def update(self, *args, **kwargs):
        if args:
            if len(args) > 1:
                raise TypeError(
                    "update expected at most 1 argument, got %s" % len(args))
            items = args[0]
            if hasattr(items, 'iteritems'):
                item_sequence = items.iteritems()
            elif hasattr(items, 'items'):
                item_sequence = items.items()
            else:
                item_sequence = items
            for key, value in item_sequence:
                self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def __getitem__(self, key):
        item = self.root.search(key)
        if item is None:
            raise KeyError(key)
        return item[1]

    def __delitem__(self, key):
        self.root.delete(key)

    def clear(self):
        self.root = self.root.__class__()

    def get(self, key, default=None):
        """(key:anything, default:anything=None) -> anything
        """
        try:
            return self[key]
        except KeyError:
            return default

    def add(self, key, value=True):
        """(key:anything, value:anything=True)
        Make self[key] == val.
        """
        if self.root.is_full():
            # replace and split.
            node = self.root.__class__()
            node.nodes = [self.root]
            node.split_child(0, node.nodes[0])
            self.root = node
        self.root.insert_item((key, value))

    def get_min_item(self):
        """() -> (key:anything, value:anything)
        Return the item whose key is minimal."""
        assert self, 'empty BTree has no min item'
        return self.root.get_min_item()

    def get_max_item(self):
        """() -> (key:anything, value:anything)
        Return the item whose key is maximal."""
        assert self, 'empty BTree has no max item'
        return self.root.get_max_item()

    def __len__(self):
        """() -> int
        Compute and return the total number of items."""
        return self.root.get_count()

    def items_backward(self):
        """() -> generator
        Generate all items in reverse order.
        """
        for item in reversed(self.root):
            yield item

    def items_from(self, key, closed=True):
        """(key, closed=True) -> generator
        If closed is true, generate all items with keys greater than or equal to
        the given key.
        If closed is false, generate all items with keys greater than the
        given key.
        """
        for item in self.root.iter_from(key):
            if closed or item[0] != key:
                yield item

    def get_depth(self):
        """() -> int
        How many levels of nodes are used for this BTree?
        """
        return self.root.get_level() + 1

    def get_node_count(self):
        """() -> int
        How many nodes are used for this BTree?
        """
        return self.root.get_node_count()


class Record:
    def __init__(self, a, b, c, d, e, f):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

def make_tree(num_nodes):
    ids = list(range(num_nodes))
    random.shuffle(ids)
    tree = BTree()

    def add_node(node_id):
        r = Record(*[random.random() for i in range(6)])
        if False:
            # create reference cycle
            r.r = r
        tree[node_id] = r

    for node_id in ids:
        add_node(node_id)

    if True:
        # Re-create part of the tree.  This can cause objects in memory
        # to become more fragmented or shuffled since they are not allocated
        # in sequence.  Since we created nodes with IDs in random order, we
        # can delete the lowest numbered ones and re-make those.
        remake_ids = range(num_nodes // 2)
        for node_id in remake_ids:
            del tree[node_id]
        for node_id in remake_ids:
            add_node(node_id)

    return tree


def main():
    #gc.disable()
    random.seed(0)
    num_nodes = 3_000_00
    if len(sys.argv) > 1:
        num_nodes = int(sys.argv[1])
    t0 = time.perf_counter_ns()
    obj = make_tree(num_nodes)
    t1 = time.perf_counter_ns()
    make_time = (t1 - t0) / 1e6
    print(f'making tree took {make_time:3.1f} ms')

    times = []
    for _ in range(10):
        start = time.perf_counter_ns()
        gc.collect()
        end = time.perf_counter_ns()
        delta = (end - start) / 1e6
        print(f"gc.collect() took {delta:3.1f} ms")
        times.append(delta)
    print(f"Median time {statistics.median(times):3.1f} ms")


if __name__ == '__main__':
    main()
