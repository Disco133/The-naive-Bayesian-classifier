import re
import string
import pymorphy2
from math import log

morph = pymorphy2.MorphAnalyzer()
message = str(input('Введите сообщение '))

with open("Spam.txt", "r", encoding="utf-8") as f:
    spam = f.read()
with open("Kredit.txt", "r", encoding="utf-8") as f:
    kredit = f.read()


# функция очистки и нормализации
def clear(x):
    x = x.translate(str.maketrans('', '', string.punctuation))
    x = re.split(' |\n', x)
    for i in range(len(x)):
        t = morph.parse(x[i])[0]
        x[i] = t.normal_form
    return x


spam_d = {}
kredit_d = {}
spam = clear(spam)
kredit = clear(kredit)

# вероятности каждого слова в словарях
for v in set(spam):
    spam_d[v] = spam.count(v) / len(spam)

for v in set(kredit):
    kredit_d[v] = kredit.count(v) / len(kredit)

message = clear(message)
# доли спам и не спам в общем количестве слов
coef_spam = len(spam) / (len(spam) + len(kredit))
coef_kredit = len(kredit) / (len(spam) + len(kredit))


# функция прогнозирования
def predict(text):
    val_spam, val_kredit = 0, 0
    for i in text:
        if i in spam_d:
            val_spam += abs(log(spam_d[i]))
        if i in kredit_d:
            val_kredit += abs(log(kredit_d[i]))
    val_spam += coef_spam
    val_kredit += coef_kredit
    if val_kredit > val_spam:
        return ('Это не спам!')
    else:
        return('Это СПАМ!')



print(predict(message))