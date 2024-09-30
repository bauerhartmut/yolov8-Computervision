list1 = [{'a': 1, 'b': 2}, {'c': 3}, {'d': 4}]
list2 = [{'a': 1, 'b': 2}, {'e': 5}, {'c': 3}]

# Finden Sie gemeinsame Dictionaries und entfernen Sie sie
for dict1 in list1[:]:  # Kopie der Liste verwenden
    if dict1 in list2:
        list1.remove(dict1)
        list2.remove(dict1)

print("List1 nach dem Löschen:", list1)
print("List2 nach dem Löschen:", list2)