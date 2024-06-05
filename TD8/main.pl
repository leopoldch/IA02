% EXERCICE 1 :

solve(X1, X2, X) :- generate(X1, X2),test(X1, X2, X).
chiffre(X) :- member(X, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]).
generate(X1, X2) :- chiffre(X1),chiffre(X2).
test(X1, X2, X) :- X is X1+X2, X1\=X2.

% EXERCICE 2

habite(X1,Y1,Z1,X2,Y2,Z2,X3,Y3,Z3) :- Y1=espagnol,Y2=norvegien,Y3=italien,X1\=1, Z2=bleu, X3=2, Z1\=rouge.

habite(X, Y, Z) :- Y=espagnol,X\=1.
habite(X, Y, Z) :- Y=norvegien, Z=bleu.
habite(X, Y, Z) :- X=2, Y=italien.
habite(X, Y, Z) :- chiffre2(X), person(Y), couleur(Z).

chiffre2(X) :- member(X, [1, 2, 3]).
couleur(Z) :- member(Z, [rouge, bleu, vert]).
person(Y) :- member(Y, [espagnol, norvegien, italien]).

generate2(X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3) :- chiffre2(X1), couleur(Z1), person(Y1), chiffre2(X2), couleur(Z2), person(Y2),chiffre2(X3), couleur(Z3), person(Y3).

test2(X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3) :-
    habite(X1, Y1, Z1,X2, Y2, Z2,X3, Y3, Z3),
    X1 \= X2, X1 \= X3, X2 \= X3,
    Y1 \= Y2, Y1 \= Y3, Y2 \= Y3,
    Z1 \= Z2, Z1 \= Z3, Z2 \= Z3.

solve2(X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3) :-
    generate2(X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3),
    test2(X1, Y1, Z1, X2, Y2, Z2, X3, Y3, Z3).

