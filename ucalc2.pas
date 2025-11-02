program ucalc;

const m=1000;

var h,p,q:array[-1..m]of boolean;

function deg(var a:array of boolean; n:longint):longint;
var i:longint;
begin
 for i:=n downto 0 do if a[i] then begin deg:=i; exit; end;
 deg:=-1;
end;

function extgcd(n:longint):longint;
var fn,gn,y0,y1,cn:array[-1..m]of boolean;
var kf,kg,sh,k,i:longint;
begin
 fn:=h; gn:=p;
 for i:=-1 to m do begin y0[i]:=false; y1[i]:=false; end;
 y1[0]:=true;
 kf:=deg(fn,n); kg:=deg(gn,n);
 while true do
 begin
  if kg<0 then begin q:=y0; exit(kf); end;
  if kf<kg then begin cn:=fn; fn:=gn; gn:=cn; cn:=y0; y0:=y1; y1:=cn; k:=kf; kf:=kg; kg:=k; end;
  sh:=kf-kg;
  for i:=0 to kf do if i>=sh then begin fn[i]:=fn[i] xor gn[i-sh]; y0[i]:=y0[i] xor y1[i-sh]; end;
  kf:=deg(fn,n);
  if kf<0 then begin q:=y1; exit(kg); end;
 end;
end;

var i:longint;

begin
h[0]:=true;
h[4]:=true;
h[6]:=true;
p[0]:=true;
p[2]:=true;
p[4]:=true;
extgcd(6);
for i:=0 to 6 do
if q[i]  then write(1) else write(0);
readln();
end.