jouons(M, N, Max) :-codeur(M, N, CodeSecret),jouer(CodeSecret, Max).

jouer(CodeSecret, 0) :-write('Vous avez perdu. Le code était : '), write(CodeSecret), nl.

jouer(CodeSecret, Essais) :-Essais > 0,
    write('Il reste '), write(Essais), write(' coup(s).'), nl,
    write('Donner un code : '), read(Proposition),
    \+ gagne(Proposition, CodeSecret),
    enleveBP(Proposition, CodeSecret, PropositionSansBP, CodeSecretSansBP),
    nBienPlace(Proposition, CodeSecret, NbBienPlaces),
    nMalPlacesAux(PropositionSansBP, CodeSecretSansBP, NbMalPlaces),
    write('BP: '), write(NbBienPlaces), write('/MP: '), write(NbMalPlaces), nl,
    NouveauEssais is Essais - 1,
    jouer(CodeSecret, NouveauEssais).

jouer(CodeSecret, Essais) :-Essais > 0,
    write('Il reste '), write(Essais), write(' coup(s).'), nl,
    write('Donner un code : '), read(Proposition),
    gagne(Proposition, CodeSecret), 
    write('Gagne'), nl.


nBienPlace([], [], 0).
nBienPlace([H1|T1], [H2|T2], N) :- H1 = H2, nBienPlace(T1, T2, N1), N is N1 + 1.
nBienPlace([H1|T1], [H2|T2], N) :- H1 \= H2, nBienPlace(T1, T2, N).


longueur([], 0).
longueur([_|Q], N) :- longueur(Q, K), N is K+1.

gagne(Liste1, Liste2) :- nBienPlace(Liste1, Liste2, N), longueur(Liste1, N).

element(El, [El|_]).
element(El, [_|Queue]) :- element(El, Queue).

enleve(_, [], []).
enleve(El, [El|Queue], Queue).
enleve(El, [Tete|Queue], [Tete|Resultat]) :- enleve(El, Queue, Resultat).

enleveBP([], [], [], []).
enleveBP([C1|R1], [C2|R2], C1Bis, C2Bis) :-C1 = C2, enleveBP(R1, R2, R1Bis, R2Bis),enleve(C1, R1Bis, C1Bis),
    enleve(C1, R2Bis, C2Bis).
enleveBP([C1|R1], [C2|R2], [C1|C1Bis], [C2|C2Bis]) :-C1 \= C2, enleveBP(R1, R2, C1Bis, C2Bis),
    longueur([C1|C1Bis], Q),
    longueur([C2|C2Bis], Q).


nMalPlacesAux([], _, 0).
nMalPlacesAux([C1|R], Code2, MP) :-element(C1, Code2), enleve(C1, Code2, Code2SansC1), nMalPlacesAux(R, Code2SansC1, K), 
    MP is K + 1.
nMalPlacesAux([C1|R], Code2, MP) :-
    \+ element(C1, Code2), 
    nMalPlacesAux(R, Code2, MP).


codeur(M, N, Code) :-longueur(Code, N),generer_code(M, Code).

generer_code(_, []).
generer_code(M, [C|Cs]) :-random(1, M, C),generer_code(M, Cs).
