def substring_up_to_nth_occurrence(text, word, n=6):
    index = -1
    start = 0
    for _ in range(n):
        index = text.find(word, start)
        if index == -1:
            return None  # Not enough occurrences
        start = index + len(word)
    return text[:start]

# Example usage:
text = "this is a test. this is only a test. this test is just a test. test again test"
word = "test"
result = substring_up_to_nth_occurrence(text, word, 6)
print("Substring up to 6th occurrence:\n", result)