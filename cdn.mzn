include "cdn.dzn";

int: V_; %number of edge servers
int: M_; %number of movies
int: CTR; % cost of transmitting 1 MB/km

set of int: V = 1..V_; %set of edge servers
set of int: M = 1..M_; %set of movies

array[V] of int: RS; %edge server storage capacity [MB]
array[V] of int: RT_OUT; %edge server transmittion capacity [MB/s] (outgoing)


array[M] of int: HS; %movie size [MB]
array[M] of int: HB; %movie bitrate in [MB/s]
array[V,M] of int: HP; %movie popularity from server [n/s]

array[V,V] of int: ED; %edge distances [km]

array[V,M] of int: CA; %cost for allocating movie M on server V

%result
array[V,M] of var 0..1: x; %1 means movie K is on server V
array[V,V,M] of var int: y; %how many MB of movie m are transitted from v1 to v2 


constraint
    forall(m in M)(
    	sum (v in V)(x[v,m]) >= 1
    	); %each movie is stored in at least one place
    
constraint
    forall(v in V)(
    	sum (m in M)(x[v,m]*HS[m]) <= RS[v]
    	); %sum of movie sizes does not exceed server storage capacity

constraint
    forall(v1 in V)(
        sum(v2 in V, m in M)(y[v1,v2,m]*HB[m]) <= RT_OUT[v1] %transmitted data from a server does not exceed server outgoing transmission capacity
    );

constraint
    forall(m in M, v2 in V)(
        sum(v1 in V)(y[v1,v2,m]) = HB[m] * HP[v2,m] * (1 - x[v2,m]) %movie transmitted to v2 exactly HP[v2,m] times if not stored on v2
    );
    
%target cost minimu,
var int: cost;

% Allocation cost
var int: allocation_cost = sum(v in V, m in M)(x[v,m] * CA[v,m]);

% Transmission cost
var int: transmission_cost = sum(v1 in V, v2 in V, m in M)(
    y[v1,v2,m] * ED[v1,v2] * HB[m] * CTR %transmission cost depends amount transmitted, required bitrate, distance, standard cost (and movie popularity)
);

% Total cost
cost = allocation_cost + transmission_cost;

solve minimize cost

