'''
You have a singly-linked list  and want to check if it contains a cycle.
A singly-linked list is built with nodes, where each node has:
node.next—the next node in the list.
node.value—the data held in the node. 
For example, if our linked list stores people in line at the movies, 
node.value might be the person's name.

For example:

  class LinkedListNode(object):

    def __init__(self, value):
        self.value = value
        self.next  = None

A cycle occurs when a node’s next points back to a previous node in the list. 
The linked list is no longer linear with a beginning and end—instead, it cycles through a loop of nodes.

Write a function contains_cycle() that takes the first node in a singly-linked list 
and returns a boolean indicating whether the list contains a cycle.
'''

def contains_cycle(node):
    slow_node = node
    fast_node = node.next

    while fast_node and slow_node:
        if slow_node.next:
            slow_node = slow_node.next
        else:
            return False

        if fast_node.next and fast_node.next.next:
            fast_node = fast_node.next.next
        else:
            return False

        print("Slow: {} Fast: {}".format(slow_node.value, fast_node.value))
        if fast_node == slow_node:
            return True

class LinkedListNode(object):
    def __init__(self, value):
        self.value = value
        self.next  = None


node1 = LinkedListNode(1)
node2 = LinkedListNode(2)
node3 = LinkedListNode(3)
node4 = LinkedListNode(4)
node5 = LinkedListNode(5)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = None

assert contains_cycle(node1) == False

# Cycle at End
node5.next = node1
assert contains_cycle(node1) == True

# Cycle in Middle
node3.next = node1
assert contains_cycle(node1) == True
