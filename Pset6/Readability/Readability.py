from cs50 import get_string

text = get_string("Text: ")
n = len(text)
letters = 0
words = 0
sentences = 0

for i in range(n):
    if text[i].isalpha():
        letters += 1
        if text[i + 1] == ' ' or text[i + 1] == ',' or text[i + 1] == '\0' or text[i + 1] == ';' or text[i + 1] == '?' or text[i + 1] == '!' or text[i + 1] == '.':
            words += 1
    elif text[i] == '.' or text[i] == '!' or text[i] == '?':
        sentences += 1

l = (letters / words) * 100
s = (sentences / words) * 100
index = round(0.0588 * l - 0.296 * s - 15.8)

if index < 1:
    print("Before Grade 1")

elif index >= 1 and index < 16:
    print(f"Grade {index}")

else:
    print("Grade 16+")