import csv
import random
from collections import Counter

# Literele frecvente în limba română, folosite pentru ghicirea AI-ului
frecvente = ['E', 'A', 'I', 'R', 'S', 'T', 'N', 'L', 'U', 'O']
# Vocalele, folosite în alternanța vocală-consoană și pattern-uri interioare
vocale = ['A', 'E', 'I', 'O', 'U']
# Consoane uzuale, folosite pentru pattern-uri și alegerea ponderată
consoane_uzuale = ['R', 'S', 'T', 'N', 'L', 'C', 'D', 'M', 'P', 'B', 'F', 'G', 'H']
# Consoane mai rare, folosite doar dacă AI-ul e blocat
consoane_rare = ['V', 'Z', 'X', 'J', 'K', 'Q', 'W', 'Y']
# Diacriticele, considerate ultimele opțiuni pentru ghicire
diacritice = ['Ă', 'Â', 'Î', 'Ș', 'Ț']

# Sufixe uzuale pentru a ghici litere finale
sufixe = ['ARE', 'IRE', 'ION', 'EST', 'ESTE', 'EA', 'UL', 'LE']
# Grupuri fonetice pentru a ghici litere logice după litere cunoscute
grupuri_extinse = {
    'C': ['CH', 'CI', 'CE', 'CHE', 'CHI'],
    'G': ['GE', 'GI', 'GHE', 'GHI'],
    'S': ['SC', 'ȘI', 'SE'],
    'T': ['ȚI', 'TR', 'TE'],
    'L': ['LE', 'LI', 'LA']
}

# Funcție care filtrează cuvintele posibile pe baza literelor deja ghicite
# Păstrează doar cuvintele cu aceeași lungime și aceleași litere la pozițiile cunoscute
def filtreaza_cuvinte(posibile, afisare):
    cuvinte_filtrate = []
    for cuv in posibile:
        if len(cuv) != len(afisare):
            continue
        potrivit = True
        for i in range(len(afisare)):
            if afisare[i] != '*' and afisare[i] != cuv[i]:
                potrivit = False
                break
        if potrivit:
            cuvinte_filtrate.append(cuv)
    return cuvinte_filtrate

# Funcție care alege o literă dintr-o listă de candidați
# Litera are șanse mai mari dacă apare mai des în cuvintele filtrate
def alegere_ponderata(candidati, frecvente_litere):
    scoruri = []
    for litera in candidati:
        scor = frecvente_litere.get(litera, 0)
        scoruri.append((litera, scor))
    total = sum(scor for _, scor in scoruri)
    if total == 0:
        return random.choice(candidati)
    lista_extinsa = []
    for litera, scor in scoruri:
        for _ in range(scor):
            lista_extinsa.append(litera)
    return random.choice(lista_extinsa)

# Funcția principală care decide ce literă să ghicească AI-ul
# Folosește sufixe, grupuri fonetice, pattern-uri, frecvență, alternanță vocală-consoană și fallback
def ghiceste_litera_AI(litere_folosite, afisare, cuvinte_romana):
    partial = ''.join(afisare)
    litere_gasite = [lit for lit in afisare if lit != '*']
    folosite = set(litere_folosite)
    cuvinte_filtrate = filtreaza_cuvinte(cuvinte_romana, afisare)
    toate_literele = ''.join(cuvinte_filtrate)
    frecvente_litere = Counter(toate_literele)

    # Secvență sufixe: dacă sfârșitul cuvântului parțial coincide cu un sufix minus ultima literă
    # AI-ul ghicește ultima literă a sufixului
    sufixe_extinse = sufixe + ['IE', 'IREA', 'ULUI']
    for suf in sufixe_extinse:
        if partial.endswith(suf[:-1]) and suf[-1] not in folosite:
            litere_folosite.append(suf[-1])
            return suf[-1]

    # Secvență grupuri fonetice: dacă o literă cunoscută precede o literă necunoscută
    # AI-ul verifică grupurile fonetice și ghicește litera următoare logic
    for i, lit in enumerate(afisare):
        if lit != '*' and i+1 < len(afisare) and afisare[i+1] == '*':
            if lit in grupuri_extinse:
                for g in grupuri_extinse[lit]:
                    next_lit = g[1] if len(g) > 1 else g[0]
                    if next_lit not in folosite:
                        litere_folosite.append(next_lit)
                        return next_lit

    # Pattern-uri interioare: dacă o literă necunoscută este între două litere cunoscute
    # Decide dacă să ghicească vocală sau consoană în funcție de litera anterioară
    for i in range(1, len(afisare)-1):
        if afisare[i] == '*' and afisare[i-1] != '*' and afisare[i+1] != '*':
            if afisare[i-1] in vocale:
                candidates = [c for c in consoane_uzuale if c not in folosite]
            else:
                candidates = [v for v in vocale if v not in folosite]
            if candidates:
                lit = alegere_ponderata(candidates, frecvente_litere)
                litere_folosite.append(lit)
                return lit

    # Litere frecvente în cuvintele filtrate: alege litera cea mai probabilă
    litere_probabile = [lit for lit, _ in frecvente_litere.most_common() if lit not in folosite]
    if litere_probabile:
        lit = litere_probabile[0]
        litere_folosite.append(lit)
        return lit

    # Alternanță vocală-consoană: dacă ultima literă ghicită e vocală, următoarea probabil e consoană și invers
    if litere_gasite:
        ultima = litere_gasite[-1]
        if ultima in vocale:
            candidates = [c for c in consoane_uzuale if c not in folosite]
        else:
            candidates = [v for v in vocale if v not in folosite]
        if candidates:
            lit = alegere_ponderata(candidates, frecvente_litere)
            litere_folosite.append(lit)
            return lit

    # Fallback: litere frecvente generale
    # Dacă nu găsește altă strategie, alege o literă frecventă nefolosită
    frecvente_ramase = [l for l in frecvente if l not in folosite]
    if frecvente_ramase:
        lit = alegere_ponderata(frecvente_ramase, frecvente_litere)
        litere_folosite.append(lit)
        return lit

    # Litere rare și diacritice: ultima soluție pentru a acoperi toate literele
    rare_ramase = [c for c in consoane_rare + diacritice if c not in folosite]
    if rare_ramase and len(litere_folosite) < 25:
        lit = random.choice(rare_ramase)
        litere_folosite.append(lit)
        return lit

    return -1

# Încarcă cuvinte din CSV și verifică validitatea literelor
def incarca_cuvinte_din_csv(nume_fisier):
    cuvinte = []
    with open(nume_fisier, encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        for linie in reader:
            if len(linie) >= 3 and all(l.isalpha() or l in diacritice for l in linie[2].upper()):
                cuvinte.append((linie[1].upper(), linie[2].upper()))
    return cuvinte

# Simularea jocului AI pe toate cuvintele
# Combină toate strategiile AI-ului și calculează totalul încercărilor
def joc_AI_toti_cuvintele(cuvinte):
    # totalul încercărilor pentru toate cuvintele
    total_incercari = 0
    # lista cu toate cuvintele reale pentru filtrare
    cuvinte_romana = [c[1] for c in cuvinte]

    for index, (cuvant_mascat, cuvant_real) in enumerate(cuvinte):
        # transformăm cuvântul mascat într-o listă pentru a putea modifica caractere
        afisare = list(cuvant_mascat)
        litere_folosite = []
        incercari = 0

        # afișăm cuvântul curent mascat
        print(f"\nCuvântul {index + 1}: {''.join(afisare)}")

        # verificăm dacă lungimile sunt egale pentru siguranță
        if len(afisare) != len(cuvant_real):
            print(f"Warning: lungimi diferite între cuvântul mascat și cel real, sărim cuvântul {index+1}")
            continue

        # buclă principală: ghicim litere până când nu mai sunt '*' în afișare
        while "*" in afisare:
            # obținem litera ghicită de AI
            ghicire = ghiceste_litera_AI(litere_folosite, afisare, cuvinte_romana)
            if ghicire == -1:
                print("AI-ul nu mai are litere disponibile.")
                break

            incercari += 1
            # găsim toate pozițiile unde litera ghicită apare în cuvântul real
            pozitii = [j for j, lit in enumerate(cuvant_real) if lit == ghicire]

            if pozitii:
                # completăm literele ghicite în afișare
                for j in pozitii:
                    if j < len(afisare):  # verificare de siguranță
                        afisare[j] = cuvant_real[j]
                print(f"litera ghicită: {ghicire}\npoziția: {' '.join(map(str, pozitii))}")
            else:
                # dacă litera ghicită nu există în cuvânt, afișăm -1
                print(f"litera ghicită: {ghicire}\npoziția: -1")

            # afișăm progresul curent al cuvântului
            print(''.join(afisare))

        # afișăm numărul total de încercări pentru cuvântul curent
        print(f"\nAI-ul a ghicit cuvântul '{cuvant_real}' în {incercari} încercări")
        total_incercari += incercari

    # returnăm totalul încercărilor pentru toate cuvintele
    return total_incercari


# --- Main ---
if __name__ == "__main__":
    cuvinte = incarca_cuvinte_din_csv("input.csv")  # încărcăm lista de cuvinte din CSV
    total = joc_AI_toti_cuvintele(cuvinte)  # simulăm jocul pentru toate cuvintele

    print(f"Totalul încercărilor: {total}")  # afișăm totalul încercărilor

    # Evaluăm performanța AI-ului
    if total <= 1200:
        print("Succes: totalul încercărilor este sub 1200!")  # performanță excelentă
    elif total <= 1500:
        print("Încă acceptabil: sub 1500.")  # performanță medie
    else:
        print("Prea mare: peste 1500.")  # performanță slabă, AI-ul a folosit prea multe încercări
