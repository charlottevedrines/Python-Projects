import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)


#{"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}
def cosine_similarity(vec1, vec2):
    temp = []
    for i in vec1.keys():
      if i in vec2.keys():
        temp.append(vec1[i] * vec2[i])
      else:
        temp.append(0)
    top = sum(temp)

    mag1 = []
    mag2 = []
    for j in vec1.values():
      mag1.append(j**2)
    for k in vec2.values():
      mag2.append(k**2)
    bottom = math.sqrt(sum(mag1) * sum(mag2))

    return top/bottom

#print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))

def build_semantic_descriptors_dict(sentences):
    ''' builds base dictionary for semantic descriptors function'''
    d = {}

    for s in sentences:
      for word in set(s):
        if word not in d:
          d[word] = {}

    return d


def build_semantic_descriptors(sentences):
    d = build_semantic_descriptors_dict(sentences)

    for s in sentences:
      for word in set(s):
        for word2 in set(s):
          if word2 != word:
            if word2 in d[word]:
              d[word][word2] += 1
            else:
              d[word][word2] = 1

    return d


def build_semantic_descriptors_from_files(filenames):
    readfile = " "
    for i in range(len(filenames)):
      openfile = open(filenames[i], "r", encoding="latin1")
      readfile  += " " + openfile.read().lower()

    l = []
      #gets rid of all the other punctuation so that the sentence enders are all only "." and all other punctuation is a space
      #then splits into sentences seperated by a "."
    sentences = readfile.replace("!",".").replace("?",".").replace(","," ").replace("-"," ").replace("--"," ").replace(";"," ").replace(":"," ").replace("\n", " ").split(".")
    for i in sentences:
      l.append(i.split())

    return build_semantic_descriptors(l)

#filenames = ["text.txt", "text2.txt"]
#print(build_semantic_descriptors_from_files(filenames))


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    temp = []
    for c in choices:
      if c in semantic_descriptors.keys():
      #print (c)
      #print(semantic_descriptors[word])
      #print(semantic_descriptors[c])
        temp.append(similarity_fn(semantic_descriptors[word], semantic_descriptors[c]))
      else:
        temp.append(-1)
    choice = temp.index(max(temp))
    return choices[choice]

#sem_descriptors = build_semantic_descriptors_from_files(["sample_case.txt"])
#print(sem_descriptors)
#choices = ["existence","closer"]
#print(most_similar_word("forest", choices, sem_descriptors, cosine_similarity))

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    score = 0
    total = 0
    with open(filename) as file:
      for line in file:
        q = line.rstrip().split()
        total += 1
        answer = most_similar_word(q[0], q[2:], semantic_descriptors, similarity_fn)
        if answer == q[1]:
          score += 1
        else:
          score = score

    return (score/total) * 100

#sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
#res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
#print(res, "of the guesses were correct")
