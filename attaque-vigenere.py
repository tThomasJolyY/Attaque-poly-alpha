from termcolor import colored

def find_pattern(texte,pattern):
  indices = []
  j = 0
  for i in range(len(texte)):
    if texte[i] == pattern[j]:
      if j == len(pattern)-1:
        indices.append(i-j)
        j = 0
      else:
        j+=1
    else:
      j = 0
  distances = []
  if len(indices) > 1:
    for i in range(0,len(indices)-1):
      distances.append(indices[i+1]-indices[i])
    return len(indices), min(distances), distances
  else:
    return len(indices), len(texte), distances

def test_pattern_size(texte, size, howmany):
  all_patterns = {}
  max_occurences = []
  for j in range(size):
    for i in range(j,len(texte),size):
      pattern = texte[i:i+size]
      if len(pattern) == size:
        nb_occurences, dmin, distances = find_pattern(texte, pattern)
        all_patterns[pattern] = {"Nb occurences": nb_occurences, "Distance Min":dmin, "Distances":distances}
  res = {}
  for i in range(howmany):
    maxv = 0
    ind = 0
    for k in all_patterns:
      if all_patterns[k]["Nb occurences"] > maxv:
          maxv = all_patterns[k]["Nb occurences"]
          ind = k
    res[ind] = all_patterns[ind]
    del all_patterns[ind]

  for k in res:
    diviseurs = {"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0}
    for d in res[k]["Distances"]:
      for i in range(2,10):
        if d % i == 0:
          diviseurs[str(i)]+=1
    diviseurs = sorted(diviseurs.items(), key=lambda x: x[1], reverse=True)
    res[k]["diviseurs"] = diviseurs

  return res

def decoupe(texte, taille):
  res = []
  for i in range(0,len(texte),taille):
    res.append(texte[i:i+taille])
  return res

def count_occurences(texte_decoupe):
  occurences = {}
  for bloc in texte_decoupe:
    for c in range(len(bloc)):
      if bloc[c]+" à la position "+ str(c) not in occurences.keys():
        occurences[bloc[c]+" à la position "+ str(c)] = 1
      else:
        occurences[bloc[c]+" à la position "+ str(c)] += 1
  occurences = sorted(occurences.items(), key=lambda x: x[1], reverse=True)
  return occurences

def remplace(ogtexte, dic_regles, size, vigeTable):
  i = 0
  j = 0
  texte = list(ogtexte)
  charset="abcdefghijklmnopqrstuvwxyz"
  while j < len(texte):
    if texte[j] in charset:
      ind = vigeTable[dic_regles[i%9]].index(texte[j])
      texte[j] = charset[ind]
      i+=1
      j+=1
    else:
      j+=1
  return "".join(texte)

with open("texte.txt", "r") as fichier:
  content = fichier.read()

charset = "abcdefghijklmnopqrstuvwxyz"
#On applique les transformations suivantes pour ignorer les caractères qui n'ont pas été chiffrés
special_car = ["\n",".","?",",","1","2","3","4","5","6","7","8","9","0","'",'"',":","ç","-","ù","û","î","ô",";","/","!","%","*","ï","$","€","&",
    "&","é","#","{","(","[","|","è","`","_","\\","^","à","@",")","]","=","+","}"]

texte = content.replace(" ","")
for car in special_car:
    texte = texte.replace(car,"")

texte = texte.lower()
for c in texte:
  if c not in charset:
    print("T'as oublié d'enlever",c)

entree = input("$> Entrez la taille des patterns que vous souhaitez analyser (next pour passer à l'étape suivante) : ")

while entree != "next":

  taille = int(entree)

  res = test_pattern_size(texte, taille, 10)

  for e in res:
    print(e,":","\n     Nb occurences=",res[e]["Nb occurences"],"\n     Distances=",res[e]["Distances"],"\n     Diviseurs=",end=" ")
    for t in res[e]["diviseurs"]:
        print(colored(t[0],"red"),"=>",colored(t[1],"light_green"),"|",end=" ")
    print()

  entree = input("$> Entrez la taille des patterns que vous souhaitez analyser (next pour passer à l'étape suivante) : ")

entree = input("$> Entrez la taille supposée de la clé : ")

taille = int(entree)

nvtexte = decoupe(texte, taille)

occurences = count_occurences(nvtexte)

for o in occurences:
  print(o[0],":",o[1], end="   |||   ")
print("")

print(content)

table = {}

for i in range(len(charset)):
  cpy = list(charset)
  tmp = []
  for j in range(i):
    tmp.append(cpy[0])
    del cpy[0]
  for j in range(i):
    cpy.append(tmp[j])
  table[charset[i]] = "".join(cpy)

dic_regles = {}
for i in range(taille):
    dic_regles[i]="a"

entree = input("$> Entrez un indice de clé que vous pensez etre bon (ex: 8=a) (stop pour quitter) : ")

while entree != "stop":
  regle = entree.split("=")

  dic_regles[int(regle[0])] = regle[1]

  tmpcontent = content.lower()

  nv_texte = remplace(tmpcontent, dic_regles, taille, table)

  for o in occurences:
    print(o[0],":",o[1], end="   |||   ")
  print("")

  print(nv_texte)
  cle = ""
  for k in dic_regles:
    cle+=dic_regles[k]
  print("Clee actuelle :",cle)

  entree = input("$> Entrez un indice de clé que vous pensez etre bon (ex: 8=a) (stop pour quitter) : ")
