program rcalc5;

const m=10000;

type TVEC=array[-1..m]of boolean;

var f,g:array[-2..0]of TVEC;

procedure fg(n:longint);
var ni,nt,k:longint;
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
end;

function gcd(n:longint;fn,gn:TVEC; var rn:TVEC):longint;
var cn:TVEC;
var k,kg,kf,kt:longint;
begin
kf:=-1; for k:=n downto 0 do if fn[k] then begin kf:=k; break; end;
kg:=-1; for k:=n downto 0 do if gn[k] then begin kg:=k; break; end;
if kf<0 then begin rn:=gn; gcd:=kg; exit; end;
if kg<0 then begin rn:=fn; gcd:=kf; exit; end;
if kf<kg then begin cn:=fn; fn:=gn; gn:=cn; k:=kf; kf:=kg; kg:=k; end;
repeat
 kt:=-1;
 for k:=0 to kf do
  begin
   if k>=(kf-kg) then fn[k]:=fn[k] xor gn[k-(kf-kg)];
   if fn[k] then kt:=k;
  end;
 if kt=-1 then begin rn:=gn; gcd:=kg; exit; end
 else if kt<kg then begin cn:=fn; fn:=gn; gn:=cn; kf:=kg; kg:=kt; end
 else kf:=kt;
until false;
end;

function rank(n:longint):longint;
var r:TVEC;
var k:longint;
begin
fg(n);
rank:=gcd(n,f[0],g[0],r);
write(n,#9);for k:=0 to n do if r[k] then write(1) else write(0);writeln();
end;

var i:longint;
begin
for i:=0 to 20 do writeln(i,#9,rank(i));
end.
