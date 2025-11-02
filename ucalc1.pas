program ucalc;

const m=1000;

var h,p,q:array[-1..m]of boolean;

function extgcd(n:longint):longint;
var fn,gn,y0,y1,cn:array[-1..m]of boolean;
var kf,kg,kt,k,sh:longint;
begin
fn:=h; gn:=p;
for k:=-1 to m do begin y0[k]:=false; y1[k]:=false; end;
y1[0]:=true;
kf:=n; kg:=n;
repeat
kt:=-1;
sh:=kf-kg;
for k:=0 to kf do
begin
 if k>=sh then begin fn[k]:=fn[k] xor gn[k-sh]; y0[k]:=y0[k] xor y1[k-sh]; end;
 if fn[k] then kt:=k;
end;
if kt=-1 then begin q:=y1; extgcd:=kg;end
else if kt<kg then begin cn:=fn; fn:=gn; gn:=cn; cn:=y0; y0:=y1; y1:=cn; kf:=kg; kg:=kt; end else kf:=kt;
until kt=-1;
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