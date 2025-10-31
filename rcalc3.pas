program rcalc3;

const m=10000;
var f,g:array[-2..0,-1..m]of boolean;

function rank(n:longint):longint;
var fn,gn,cn:array[-1..m]of boolean;
var ni,nt,k,kg,kf,kt:longint;
begin
if f[0,n-1]=false then begin f[0,0]:=true;g[0,0]:=true;nt:=1;end else nt:=n;
for ni:=nt to n do
begin
f[-2]:=f[-1];f[-1]:=f[0];g[-2]:=g[-1];g[-1]:=g[0];
for k:=0 to ni do
begin
f[0,k]:=f[-1,k-1] xor f[-2,k];
g[0,k]:=g[-1,k-1] xor g[-1,k] xor g[-2,k];
end;
end;
fn:=f[0];gn:=g[0];
kg:=n;kf:=n;
repeat
kt:=-1;
for k:=0 to kf do
begin 
if k>=(kf-kg) then fn[k]:=fn[k] xor gn[k-(kf-kg)];
if fn[k] then kt:=k;
end;
if kt=-1 then rank:=kg;
if kt<kg then begin cn:=fn;fn:=gn;gn:=cn;kf:=kg;kg:=kt;end else kf:=kt;
until kt=-1;
end;

var i:longint;
begin
for i:=1 to m do writeln(i,#9,rank(i));
end.
