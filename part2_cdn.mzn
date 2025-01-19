%include "part2_cdn.dzn";

int: V_; %number of edge servers
int: M_; %number of movies
int: CTR; % cost of transmitting 1 MB/km

int: max_instances;
float: target_pB;

set of int: V = 1..V_; %set of edge servers
set of int: M = 1..M_; %set of movies

array[V] of int: RS; %instance storage capacity [MB]
array[V] of int: RT_OUT; %instance transmittion capacity [MB/s] (outgoing)
array[V] of int: RC; %instance cost

array[M] of int: HS; %movie size [MB]
array[M] of int: HB; %movie bitrate in [MB/s]
array[V,M] of int: HP; %movie popularity from server [n/s]
array[V,M] of var 0..1: HA; %watch full probability

array[V,V] of int: ED; %edge distances [km]

array[V,M] of int: CA; %cost for allocating movie M on server V

array[1..max_instances] of float: erlang_table;

%result variables
array[V,M] of var 0..1: x; %1 means movie K is on server V
array[V,V,M] of var 0..9999: y; %how many MB of movie m are transitted from v1 to v2 
array[V] of var 0..max_instances: z;  %number of instances running in location V


function float: PB(float: A, int: n) = 
	if n = 0 then
		1
	else
		let {
			float: prev = PB(A, n-1)
		} in
		(A * prev) / (A*prev + n)
	endif;
	
%function float: find_max_offered_load(int: n, float: target_pB, float: low, float: high) =
%    let {
%        float: mid = (low + high) / 2.0,
%        float: pB = PB(mid, n)
%    } in
%    if abs(pB - target_pB) < 1e-4 then
%        mid
%    else if pB > target_pB then
%        find_max_offered_load(n, target_pB, low, mid)
%    else
%        find_max_offered_load(n, target_pB, mid, high)
%    endif;


%constraint
%    forall(n in 1..max_instances)(
%        erlang_table[n] = find_max_offered_load(n, target_pB, 0.0, 30.0)
%    );


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
        sum(v1 in V)(y[v1,v2,m]*x[v1,m]*erlang_table[z[v1]] + x[v2,m]*erlang_table[z[v2]]*HB[m]) >= HB[m]*HP[v2,m]*HA[v2,m]
    ); %movie transmitted to v2 if not stored on v2
    
    
%target cost minimu,
var int: cost;

%Running cost
var int: running_cost = sum(v in V)(z[v]*RC[v]);

% Allocation cost
var int: allocation_cost = sum(v in V, m in M)(x[v,m] * CA[v,m]);

% Transmission cost
var int: transmission_cost = sum(v1 in V, v2 in V, m in M)(
    y[v1,v2,m] * ED[v1,v2] * HB[m] * CTR 
); %transmission cost depends amount transmitted, required bitrate, distance, standard cost (and movie popularity)

% Total cost
cost = running_cost + allocation_cost + transmission_cost;

solve minimize cost;
%solve satisfy

output[
    show(cost) ++ "\n"
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
