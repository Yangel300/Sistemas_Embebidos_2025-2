go:-recoger_datos,
    diagnostico(_). % Variable anonima "_" por que no la estoy usando

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
hipotermia :-
    valor(temperatura,T),
    T<28.
bradicardia :-
    valor(presion,P),
    P<60.

:- dynamic valor/2.
% Reglas simples

% --- Diagnóstico final ---
%Predicado(Argumento)
diagnostico(Resultado) :-
    %findall/3 sirve para recolectar todas las soluciones de una consulta en una lista
    %Mensaje es lo que quiero recolectar
    findall(Mensaje,
           %bloque de condiciones, fiebre, taquicardia, hipoxia
           %El ; significa "o" en Prolog, asi que intenta todas esas posibilidades
        ( (fiebre, Mensaje = 'El paciente tiene fiebre')
        ; (taquicardia, Mensaje= 'El paciente tiene taquicardia')
        ; (hipoxia, Mensaje = 'El paciente tiene hipoxia')
        ; (hipotermia, Mensaje = 'El paciente tiene hipotermia')
        ; (bradicardia, Mensaje = 'El paciente tiene bradicardia')), 
        %ListaFinal es donde se guardan los resultado
        ListaPre), 
        sort(ListaPre, ListaFinal), %short ordena la lista y elimina duplicados
            
        %Condicional en prolog Si la lista está vacía ([]), entonces el resultado sera 'No se detectaron problemas' si no ; imprime la listaFinal
   ( ListaFinal = [] -> 
   Resultado = ['No se detectaron problemas'] 
   ; Resultado = ListaFinal  ).
