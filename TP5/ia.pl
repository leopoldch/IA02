% ================================================================
% =                    TP MASTERMIND IA02 P24                    =
% ================================================================

jouons(M, N, Max) :-codeur(M, N, CodeSecret),write('Code : '), write(CodeSecret), nl, jouer(CodeSecret, Max).

jouer(CodeSecret, 0) :-write('Vous avez perdu. Le code était : '), write(CodeSecret), nl.

jouer(CodeSecret, Essais) :-Essais > 0,
    write('Il reste '), write(Essais), write(' coup(s).'), nl,
    write('Donner un code : '), read(Proposition),
    \+ gagne(Proposition, CodeSecret),
    enleveBP(Proposition, CodeSecret, PropositionSansBP, CodeSecretSansBP),
    nBienPlace(Proposition, CodeSecret, NbBienPlaces),
    nMalPlaces(PropositionSansBP, CodeSecretSansBP, NbMalPlaces),
    write('BP: '), write(NbBienPlaces), write('/MP: '), write(NbMalPlaces), nl,
    NouveauEssais is Essais - 1,
    jouer(CodeSecret, NouveauEssais);
    gagne(Proposition,CodeSecret), write('Gagné !').


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


nMalPlaces([], _, 0).
% si element on enleve et incrémente 
nMalPlaces([C1|R], Code2, MP) :-element(C1, Code2), enleve(C1, Code2, Code2SansC1), 
    nMalPlaces(R, Code2SansC1, K), 
    MP is K + 1.
% si pas un element on continue
nMalPlaces([C1|R], Code2, MP) :- \+ element(C1, Code2), nMalPlaces(R, Code2, MP).


codeur(M, N, Code) :-longueur(Code, N),generer_code(M, Code).

generer_code(_, []).
generer_code(M, [C|Cs]) :-random(1, M, C),generer_code(M, Cs).


% ================================================================
% =                           PARTIE 2                           =
% ================================================================


liste_couleurs(X, X, [X]).
liste_couleurs(MI, MA, [MI|L]) :-K is MI + 1,liste_couleurs(K, MA, L).

get_number(L,X) :- member(X,L).
encode(_, [], 0).
encode(L, [T|R], N) :- N > 0, K is N - 1,get_number(L, T),encode(L, R, K).
gen(M,N,Code) :- liste_couleurs(1,M,COLORS),encode(COLORS,Code,N).

test(Code, Historique) :-  \+ member(Code,Historique).% on écarte ce qui est dans l'historique
% reproduire le nombre d'éléments bien placés ? 
test(Code, Historique) :- 

