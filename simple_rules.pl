go:-recoger_datos,
    diagnostico.

recoger_datos :-
    ask_number(temperatura),
    ask_number(presion),
    ask_number(oximetria).


ask_number(Variable) :-
    write('Ingrese '), write(Variable), write(': '),
    read(Value), nl,
    assertz(valor(Variable, Value)).


%Hypothesis Identification Rules
fiebre :-
    valor(temperatura,T),
    T>38.
taquicardia :-
    valor(presion,P),
    P>120.

hipoxia :-
    valor(oximetria,O),
    O<90.


verify(Question, Value) :-
    write(Question), write(': '),
    read(Value), nl,
    assertz(valor(Question, Value)).
:- dynamic valor/2.
% Reglas simples

% --- Diagnóstico final ---
diagnostico :-
    ( fiebre -> writeln('El paciente tiene fiebre') ; true ),
    ( taquicardia -> writeln('El paciente tiene taquicardia') ; true ),
    ( hipoxia -> writeln('El paciente tiene hipoxia') ; true ),
    writeln('--- Diagnóstico completado ---').



