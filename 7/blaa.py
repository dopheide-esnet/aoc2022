#!/usr/bin/env python3

class Blaa:
	def __init__(self,name,parent):
		self.name = name
		self.parent = parent
		self.content = dict()


root = Blaa("root",None)

print(root.name)
print(root.parent)

next = Blaa("two",root)

current = root

current.content["two"] = next

print(current.content["two"].name)

current = current.content["two"].parent

print(current.name)

current = current.content["two"]

print(current.name)

current = current.parent

print(current.name)
