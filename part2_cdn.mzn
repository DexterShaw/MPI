%include "part2_cdn.dzn";

QuadrFloat = true;

int: V_; %number of edge servers
int: M_; %number of movies
int: CTR; % cost of transmitting 1 MB/km

int: max_instances;


set of int: V = 1..V_; %set of edge servers
set of int: M = 1..M_; %set of movies

array[V] of int: RS; %instance storage capacity [MB]
array[V] of int: RT_OUT; %instance transmittion capacity [MB/s] (outgoing)


array[M] of int: HS; %movie size [MB]
array[M] of int: HB; %movie bitrate in [MB/s]
array[V,M] of int: HP; %movie popularity from server [n/s]


array[V,V] of int: ED; %edge distances [km]

array[V,M] of int: CA; %cost for allocating movie M on server V
array[V] of int: CI; %instance cost on server v

array[1..max_instances] of int: erlang_table;

%result variables
array[V,M] of var 0..1: x; %1 means movie K is on server V
array[V,V,M] of var 0..9999: y; %how many MB of movie m are transitted from v1 to v2 
array[V] of var 1..max_instances: z;  %number of instances running in location V


constraint
    forall(m in M)(
    	sum (v in V)(x[v,m]) >= 1 
    	); %each movie is stored in at least one place
    
constraint
    forall(v in V)(
    	sum (m in M)(x[v,m]*HS[m]) <= RS[v]*z[v]
    	); %sum of movie sizes does not exceed server storage capacity
    	
constraint
    forall(v1 in V)(
        sum(v2 in V, m in M)(y[v1,v2,m]*HB[m]) <= RT_OUT[v1]*z[v1] 
    ); %transmitted data from a server does not exceed server outgoing transmission capacity

constraint
    forall(m in M, v2 in V)(
        sum(v1 in V where ED[v1,v2] > 0)(y[v1,v2,m]*x[v1,m]) >= HB[m]*(1-x[v2,m])
    ); %movie transmitted to v2 if not stored on v2
    
constraint
    forall(v in V)(
        10000 *
        (
            sum(m in M)(x[v,m]*HP[v,m]) + 
            sum(v2 in V, m in M where y[v,v2,m] > 0)(1)
        )
        *
        (
            sum(m in M)(HS[m]*x[v,m])
        ) 
        <= erlang_table[z[v]] * sum(m in M)(x[v,m]) 
    ); %assuming in given timeframe comes lambda requests, and 1/mi is equal to average movie sizes asked from v, lambda * 1/mi must not exceed max possible load
    
%target cost minimu,
var int: cost;

%Running cost
var int: running_cost = sum(v in V)(z[v]*CI[v]);

% Allocation cost
var int: allocation_cost = sum(v in V, m in M)(x[v,m] * CA[v,m]);

% Transmission cost
var int: transmission_cost = sum(v1 in V, v2 in V, m in M)(
    y[v1,v2,m] * ED[v1,v2] * HB[m] * CTR 
); %transmission cost depends amount transmitted, required bitrate, distance, standard cost (and movie popularity)

% Total cost
cost = running_cost + allocation_cost + transmission_cost;

solve minimize cost;
%solve satisfy;

output[
    show(cost) ++ " = " ++ show(running_cost) ++ " + " ++ show(allocation_cost) ++ " + " ++ show(transmission_cost) ++ "\n"
] ++
[
    concat([show(z[i]) ++ " " | i in 1..V_]) ++ "\n"
] ++
[
    concat([
        concat([show(x[j,i]) ++ " " | i in 1..M_]) ++ "\n" | j in 1..V_
        ]) ++ "\n"
]++
[
    show(m) ++ "\n" ++
    concat([
    	concat([
    		show(y[i, j, m]) ++ " " | j in 1..V_
    		]) ++ "\n" | i in 1..V_
    	]) | m in 1..M_
];
