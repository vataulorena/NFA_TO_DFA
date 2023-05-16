def lambda_inchid(stari, nfa):
    # lista cu starile inchiderii
    inchid = set(stari)
    while True:
        # lista inchiderilor pentru fiecare stare in parte
        lista = set()
        for poz in inchid:
            # unim toate starile lambda
            lista |= set(nfa.get(poz, {}).get('x', []))
        #scapam de dubluri
        lista -= inchid
        #daca nu avem lambda ne oprim
        if not lista:
            break
        inchid |= lista
    return sorted(list(inchid))

def nfa_to_dfa(nfa,prima,alfabet):
    # cream lambda inchiderea pt prima stare, ca sa putem pleca din ea
    init = sorted(lambda_inchid([prima], nfa))
    # adaugam prima inchidere in lista in care avem toate starile de parcurs in prelucrare
    lista = [init]
    # starile deja prelucrate
    drum = set()
    dfa = {}

    # pana nu mai avem stari de parcurs
    while lista:
        # ne luam starea de prelucrat din lista
        prelucram_stare = lista.pop(0)
        # daca nu am ajuns pe ea trebuie prelucrata
        if tuple(prelucram_stare) in drum:
            continue
        # o adaugam ca sa stim pe unde am mers
        drum.add(tuple(prelucram_stare))
        # cream linia din matrice pentru starea in care ne aflam
        dfa[tuple(prelucram_stare)] = {}
        # trecem prin fiecare stare din alfabet ca sa aflam urmatoarea mutare
        for lit in alfabet:
            next = set()
            for nfa_state in prelucram_stare:
                # punem in next stare toate starile din nfa care pleaca cu litera respectiva
                next |= set(nfa.get(nfa_state, {}).get(lit, []))
            # cautam si mutarile cu lambda
            lambda_mutare = sorted(lambda_inchid(next, nfa))
            # daca nu am trecut prin starile urmatoare deja cu prelucarea le adaugam in lista
            if tuple(lambda_mutare) not in drum:
                lista.append(lambda_mutare)
            # nu uitam sa adaugam mutarea si cu lambda la mutarile starii
            dfa[tuple(prelucram_stare)][lit] = tuple(lambda_mutare)
    return dfa

def afis_dfa(dfa, fisier, finale):
    with open(fisier, 'w') as f:
        # scoatem starea inițială din DFA pentru a o afișa
        initial = next(iter(dfa))
        f.write(f"INITIALA: {initial}\n\n")

        # Parcurgem starile finale initiale și cele din DFA și le afișăm doar pe acelea care le includ pe cele finale inițiale
        finale2 = [stare for stare in dfa if any(x in stare for x in finale)]
        f.write(f"FINALE: {', '.join(str(stare) for stare in finale2)}\n\n")

        # accesăm fiecare stare și, dacă este diferită de mulțimea vidă, afișăm mutările
        for stare in dfa:
            if stare != ():
                # Parcurgem matricea și formatăm output-ul
                for lit in dfa[stare]:
                    starea_urm = dfa[stare][lit]
                    f.write(f"{stare} ({lit})--> {starea_urm}\n")
                f.write("\n")


nfa = {}
alfabet = ('a', 'b', 'c')
with open('fisier.in') as file:
    # Citim starea inițială
    init = file.readline().strip()
    # Citim starile finale
    fin = file.readline().strip().split()
    for line in file:
        line = line.strip().split(' ')
        prima = line[0]
        litera = line[1]
        a_doua = line[2]
        # Înlocuim lambda cu x
        if litera == 'lambda':
            litera = 'x'
        # Dacă nu există, o formam
        if prima not in nfa:
            nfa[prima] = {}
        # Dacă există în NFA, dar nu ca simbol, o formam
        if litera not in nfa[prima]:
            nfa[prima][litera] = [a_doua]
        # Dacă există în NFA și există ca simbol, doar adăugăm încă o dată
        else:
            nfa[prima][litera] += [a_doua]

dfa = nfa_to_dfa(nfa, init, alfabet)
afis_dfa(dfa, 'fisier.out', fin)
