def custom_sort(strings, sub1, sub2):
    def sort_key(s):
        # Count how many of the substrings are present
        matches = int(sub1 in s) + int(sub2 in s)
        # Priority: more matches come first (-matches for descending order)
        # Then by length, then alphabetically
        return (-matches, len(s), s)
    
    return sorted(strings, key=sort_key)


# Example usage
strings = [
    "apple banana",
    "apple pie",
    "banana split",
    "cherry tart",
    "apple banana smoothie",
    "grape"
]

sub1 = "apple"
sub2 = "banana"

result = custom_sort(strings, sub1, sub2)
print(result)