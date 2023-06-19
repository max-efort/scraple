"""
Contain the core function of implementation for "custom tree structure"
used in this package.
"""


def appender(num, list_):
    if num != 1:
        list_[-1] = num
    else:
        list_.append(num)


def create_Tree(body, dictionary_tree=None, id_f=None, first_caller=True):
    if first_caller:
        dictionary_tree, id_f = {}, []
    count = 1
    for element in body:
        if element.name is not None:
            node = node_constructor(element)
            appender(count, id_f)
            dictionary_tree[tuple(id_f)] = node
            create_Tree(element, dictionary_tree, id_f.copy(), False)
            count += 1
    if first_caller:
        return dictionary_tree


def node_constructor(element):
    node = element.name
    if 'class' in element.attrs:
        for class_ in element.attrs["class"]:
            node = node + "." + class_
    node = node + "#" + element.attrs["id"] if 'id' in element.attrs else node
    return node


def identity_to_branch(identity, tree):
    branch = None
    for i in range(1, len(identity) + 1):
        branch = branch + ' ' + tree[identity[:i]] if branch is not None else tree[identity[:i]]
    return branch


def find_node(identity, tree):
    return tree[identity]
