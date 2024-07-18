/*********************************************
 * OPL 12.10.0.0 Model
 * Author: Administrator
 * Creation Date: Apr 21, 2024 at 4:20:37 PM
 *********************************************/

int NI = ...;
int NJ = ...;
int NT = ...;

range I = 1 .. NI;
range J = 1 .. NJ;
range T = 1 .. NT;

int C = ...;
float f[i in I] = ...;
float f_bar[i in I] = ...;
float CR[t in T] = ...;
int w [t in T][j in J] = ...;
int y[i in I][t in T][j in J]=...;


dvar float+ N_C;
dvar boolean x[i in I][t in T];
dvar boolean meyo[i in I][t in T];
dvar boolean meyo_bar[i in I][t in T];
dvar boolean z[t in T][j in J];




dexpr float C_cost = C*N_C;
dexpr float C_in = sum (i in I) x[i][1]*f[i] + sum(i in I, t in 2..NT) meyo[i][t]*f[i];
dexpr float C_unin = sum (i in I) x[i][NT]*f_bar[i] + sum (i in I, t in 2..NT) meyo_bar[i][t]*f_bar[i];


minimize C_cost + C_in + C_unin;
subject to {
  
 forall(i in I, t in 2..NT)
  meyo[i][t] >= x[i][t] - x[i][t-1];
 
 forall(i in I, t in 2..NT)
  meyo_bar[i][t] >= x[i][t-1] - x[i][t];
  
forall (t in T)
  sum(j in J) z[t][j]*w[t][j] >= CR[t]*sum(j in J)w[t][j];
  
forall(i in I, t in T, j in J)
  x[i][t]*y[i][t][j] <= z[t][j];
  
forall( t in T, j in J)
  sum (i in I) x[i][t]*y[i][t][j] >= z[t][j];
  
  
forall(t in T)  
N_C >=sum(i in I) x[i][t];

forall (i in I, t in T)
  x[i][t] <= sum(j in J) y[i][t][j];
  
}