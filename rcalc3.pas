program rcalc3;

const m=10000;

var f,g:array[-1..m+1,-1..m+1]of boolean;
var fn,gn,cn:array[0..m]of boolean;
var k:longint;
var kg,kf,kt,kc:longint;

procedure fx(n:longint);
begin
if (n=0) then f[n,n]:=true
else for k:=0 to m do f[n,k]:=f[n-1,k-1] xor f[n-2,k];
end;

procedure gx(n:longint);
begin
if (n=0) then g[n,n]:=true
else for k:=0 to m do g[n,k]:=g[n-1,k-1] xor g[n-1,k] xor g[n-2,k];
end;

function gcd(n:longint):longint;
begin
//writeln();
for k:=0 to n do fn[k]:=f[n,k];
for k:=0 to n do gn[k]:=g[n,k];
kg:=n;
kf:=n;
repeat
kc:=kf-kg;
kt:=-1;
//writeln('@');
//for k:=0 to kf do if fn[k] then write('#') else write('.');writeln();
//for k:=0 to kf do if gn[k] then write('#') else write('.');writeln();
for k:=0 to kf do begin if k>=kc then fn[k]:=fn[k] xor gn[k-kc];if fn[k] then kt:=k;
//if fn[k] then write('#') else write('.');
end;
//writeln(#9,kf,#9,kg,#9,kc,#9,kt);
//readln();
if kt=-1 then gcd:=kg;
if kt<kg then
  begin
  for k:=0 to kg do begin cn[k]:=fn[k];fn[k]:=gn[k];gn[k]:=cn[k];end;
  kf:=kg;
  kg:=kt;
  end
else
  kf:=kt;
until kt=-1;
end;

var i:longint;

begin
for i:=0 to m do
  begin
  fx(i);
//  for k:=0 to i do if f[i,k] then write('#') else write('.');writeln;
  gx(i);
//  for k:=0 to i do if g[i,k] then write('#') else write('.');writeln;
  {if i=5 then} writeln(i,#9,gcd(i));
//  for k:=0 to i do if fn[k] then write('#') else write('.');writeln;
//  writeln('####################')
  end;
end.
