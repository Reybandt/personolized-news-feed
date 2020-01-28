import string

def clean(s):
	translator = str.maketrans("", "", string.punctuation)
	return s.translate(translator).lower()
