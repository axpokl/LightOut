program ucalc;
const m=1000;
var h,p,q:array[0..m]of boolean;

function extgcd(n:longint):longint;
var fn,gn,y0,y1,cn:array[0..m]of boolean;
var kf,kg,sh,i,t,res:longint;
var done:boolean;
begin
for i:=0 to m do begin fn[i]:=h[i]; gn[i]:=p[i]; y0[i]:=false; y1[i]:=false; end;
y1[0]:=true;
kf:=-1; for i:=n downto 0 do if fn[i] then begin kf:=i; break; end;
kg:=-1; for i:=n downto 0 do if gn[i] then begin kg:=i; break; end;
done:=false; res:=-1;
while not done do
begin
 if kf<0 then begin for i:=0 to n do q[i]:=y1[i]; res:=kg; done:=true; end
 else if kg<0 then begin for i:=0 to n do q[i]:=y0[i]; res:=kf; done:=true; end
 else
  begin
   if kf<kg then begin for i:=0 to n do begin cn[i]:=fn[i]; fn[i]:=gn[i]; gn[i]:=cn[i]; cn[i]:=y0[i]; y0[i]:=y1[i]; y1[i]:=cn[i]; end; t:=kf; kf:=kg; kg:=t; end;
   sh:=kf-kg;
   for i:=n downto sh do if gn[i-sh] then fn[i]:=fn[i] xor true;
   for i:=n downto sh do if y1[i-sh] then y0[i]:=y0[i] xor true;
   kf:=-1; for i:=n downto 0 do if fn[i] then begin kf:=i; break; end;
  end;
end;
extgcd:=res;
end;

var i:longint;
begin
h[0]:=true; h[4]:=true; h[6]:=true;
p[0]:=false; p[2]:=true; p[4]:=true;
extgcd(6);
for i:=0 to 6 do if q[i] then write(1) else write(0);
writeln;
readln;
end.
