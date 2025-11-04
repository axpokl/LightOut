{$define disp}
program diandeng;

{$ifdef disp}
uses display;
{$endif}

const m=1000; wm=(m+31) div 32; WB=32;

type TRow=array[-1..wm] of LongWord;
type TMat=array[-1..m] of TRow;
type TVec=array[-1..wm] of LongWord;
type TVeci=array[-1..m] of longint;

var n:longword;
var a,l,t,f,e,h:TMat;
var i,j:longint;
var wbr,wbp:longint;
var maskr,maskp:LongWord;

{$ifdef disp}
var bb:pbitbuf;
var b:pbitmap;
{$endif}

procedure VecClearN(var v:TVec; wb:longint); var k:longint; begin for k:=0 to wb-1 do v[k]:=0; end;
procedure VecCopyN(const s:TVec; var d:TVec; wb:longint); var k:longint; begin for k:=0 to wb-1 do d[k]:=s[k]; end;
procedure VecXorN(var d:TVec; const s:TVec; wb:longint); var k:longint; begin for k:=0 to wb-1 do d[k]:=d[k] xor s[k]; end;
procedure VecMaskLast(var v:TVec; wb:longint; mask:LongWord); begin if wb>0 then v[wb-1]:=v[wb-1] and mask; end;
procedure VecShl1N(const s:TVec; var d:TVec; wb:longint; mask:LongWord); var k:longint; c:LongWord; begin c:=0; for k:=0 to wb-1 do begin d[k]:=(s[k] shl 1) or c; c:=s[k] shr 31; end; VecMaskLast(d,wb,mask); end;
procedure VecShr1N(const s:TVec; var d:TVec; wb:longint); var k:longint; c:LongWord; begin c:=0; for k:=wb-1 downto 0 do begin d[k]:=(s[k] shr 1) or c; c:=s[k] shl 31; end; end;
procedure VecShiftXorN(var d:TVec; const s:TVec; sh,wb:longint; mask:LongWord); var sw,rb,k:longint; lo,hi:LongWord; begin if sh<=0 then exit; sw:=sh shr 5; rb:=sh and 31; for k:=wb-1 downto 0 do begin lo:=0; hi:=0; if (k-sw)>=0 then lo:=s[k-sw] shl rb; if (rb<>0) and ((k-sw-1)>=0) then hi:=s[k-sw-1] shr (32-rb); d[k]:=d[k] xor (lo or hi); end; VecMaskLast(d,wb,mask); end;
function GetBitV(const v:TVec; idx:longint):boolean; var w,b:longint; begin if idx<0 then exit(false); w:=idx shr 5; b:=idx and 31; GetBitV:=((v[w] shr b) and 1)=1; end;
procedure SetBitV(var v:TVec; idx:longint; bval:boolean); var w,b:longint; m:LongWord; begin if idx<0 then exit; w:=idx shr 5; b:=idx and 31; m:=LongWord(1) shl b; if bval then v[w]:=v[w] or m else v[w]:=v[w] and not m; end;
procedure FlipBitV(var v:TVec; idx:longint); var w,b:longint; begin if idx<0 then exit; w:=idx shr 5; b:=idx and 31; v[w]:=v[w] xor (LongWord(1) shl b); end;
function DegN(const v:TVec; wb:longint):longint; var k,b:longint; x:LongWord; begin for k:=wb-1 downto 0 do if v[k]<>0 then begin x:=v[k]; for b:=31 downto 0 do if ((x shr b) and 1)<>0 then exit(k*32+b); end; DegN:=-1; end;
procedure VecSwap(var a,b:TVec; wb:longint); var k:longint; t:LongWord; begin for k:=0 to wb-1 do begin t:=a[k]; a[k]:=b[k]; b[k]:=t; end; end;

procedure PrintMat(mat:TMat);
begin
writeln();
for j:=0 to n-1 do
  begin
  for i:=0 to n-1 do if GetBitV(mat[j],i) then write('#') else write('.');
  writeln();
  end;
writeln();
end;

{$ifdef disp}
procedure DrawMat(mat:TMat);
begin
while IsNextMsg() do ;
for j:=0 to n-1 do
  for i:=0 to n-1 do
    if GetBitV(mat[j],i) then SetBBPixel(bb,i,j,black) else SetBBPixel(bb,i,j,white);
SetBB(bb);
FreshWin();
end;

procedure PrintMat(s:ansistring;mat:TMAT);
begin
DrawMat(mat);
b:=CreateBMP(n,n);
DrawBMP(_pmain,b,0,0,n,n,0,0,n,n);
SaveBMP(b,'png'+s+'/'+i2s(n)+'.png');
ReleaseBMP(b);
end;
{$endif}

procedure MakeMat();
var v1,v2,v3,tmp:TVec;
begin
VecClearN(l[0],wbr);
for j:=1 to n do begin VecShl1N(l[j-1],v1,wbr,maskr); VecCopyN(l[j-1],v2,wbr); VecShr1N(l[j-1],v3,wbr); VecCopyN(l[j-2],tmp,wbr); VecXorN(v1,v2,wbr); VecXorN(v1,v3,wbr); VecXorN(v1,tmp,wbr); for i:=0 to wbr-1 do l[j][i]:=not v1[i]; VecMaskLast(l[j],wbr,maskr); end;
for j:=0 to n do if not GetBitV(a[j],j) then if not GetBitV(a[0],0) then SetBitV(a[0],0,true) else begin VecShl1N(a[j-1],v1,wbr,maskr); VecCopyN(a[j-1],v2,wbr); VecShr1N(a[j-1],v3,wbr); VecCopyN(a[j-2],tmp,wbr); VecXorN(v1,v2,wbr); VecXorN(v1,v3,wbr); VecXorN(v1,tmp,wbr); VecCopyN(v1,a[j],wbr); end;
for j:=0 to n do if not GetBitV(f[j],j) then if not GetBitV(f[0],0) then SetBitV(f[0],0,true) else begin VecShl1N(f[j-1],v1,wbp,maskp); VecCopyN(f[j-2],tmp,wbp); VecCopyN(v1,f[j],wbp); VecXorN(f[j],tmp,wbp); end;
for j:=0 to n do if not GetBitV(e[j],j) then if not GetBitV(e[0],0) then SetBitV(e[0],0,true) else begin VecShl1N(e[j-1],v1,wbr,maskr); VecShr1N(e[j-1],v2,wbr); VecCopyN(v1,e[j],wbr); VecXorN(e[j],v2,wbr); end;
end;

function gcd(n:longint;vf,vg:TVec; var vr:TVec):longint;
var kf,kg:longint;
begin
kf:=DegN(vf,wbp); kg:=DegN(vg,wbp);
if kf<0 then begin VecCopyN(vg,vr,wbp); exit(kg); end;
if kg<0 then begin VecCopyN(vf,vr,wbp); exit(kf); end;
if kf<kg then begin VecSwap(vf,vg,wbp); kf:=kg; kg:=DegN(vg,wbp); end;
repeat
VecShiftXorN(vf,vg,kf-kg,wbp,maskp);
kf:=DegN(vf,wbp);
if kf=-1 then begin VecCopyN(vg,vr,wbp); exit(kg); end else if kf<kg then begin VecSwap(vf,vg,wbp); kf:=kg; kg:=DegN(vg,wbp); end;
until false;
end;

procedure rev(vf,vg:TVec;var vr:TVec);
var kf,kg:longint; vt,vx,vy:TVec;
begin
VecClearN(vx,wbp); VecClearN(vy,wbp); vy[0]:=1;
kf:=DegN(vf,wbp); kg:=DegN(vg,wbp);
while true do
  begin
  if kf<0 then begin VecCopyN(vy,vr,wbp); exit; end else if kg<0 then begin VecCopyN(vx,vr,wbp); exit; end else
    begin
    if kf<kg then begin VecSwap(vf,vg,wbp); VecSwap(vx,vy,wbp); kf:=kg; kg:=DegN(vg,wbp); end;
    VecShiftXorN(vf,vg,kf-kg,wbp,maskp);
    VecShiftXorN(vx,vy,kf-kg,wbp,maskp);
    kf:=DegN(vf,wbp);
    end;
  end;
end;

procedure CalcMat2;
var p,q,x,y,z,c,g:TVec;
var r:TVeci;
var k:longint; v1,vr,vl:TVec;
begin
write('p',#9);
VecClearN(p,wbp);
for j:=0 to n-1 do if GetBitV(a[n],j) then VecXorN(p,f[j],wbp);
write('q',#9);
rev(f[n],p,q);
write('y',#9);
VecCopyN(l[n],y,wbr);
write('z',#9);
VecClearN(z,wbr);
for j:=0 to n-1 do
  begin
  if GetBitV(q,j) then VecXorN(z,y,wbr);
  VecShl1N(y,vl,wbr,maskr);
  VecShr1N(y,vr,wbr);
  VecCopyN(vl,y,wbr); VecXorN(y,vr,wbr);
  end;
write('g',gcd(n,p,f[n],g),#9);
write('h',#9);
VecClearN(h[0],wbr);
for j:=0 to n-1 do if GetBitV(g,j) then VecXorN(h[0],e[j],wbr);
for j:=1 to n-1 do begin VecShl1N(h[j-1],vl,wbr,maskr); VecShr1N(h[j-1],vr,wbr); VecCopyN(vl,h[j],wbr); VecXorN(h[j],vr,wbr); VecXorN(h[j],h[j-2],wbr); end;
write('r',#9);
for j:=0 to n-1 do begin r[j]:=-1; for i:=0 to n-1 do if GetBitV(h[i],j) then begin r[j]:=i; break; end; end;
write('x',#9);
VecClearN(x,wbr);
for i:=0 to n-1 do
 if GetBitV(z,i) then
 begin
  k:=-1;
  for j:=i to n-1 do if r[j]=i then begin k:=j; break; end;
  if k<0 then break;
  for j:=0 to n-1 do if GetBitV(h[j],k) then FlipBitV(z,j);
  if GetBitV(x,k) then SetBitV(x,k,false) else SetBitV(x,k,true);
 end;
write('t',#9);
VecCopyN(x,t[0],wbr);
end;

function GeneMat():boolean;
var vl,vr,vx,vu:TVec; ok:boolean; i2:longint;
begin
for j:=1 to n-1 do
  begin
  VecShl1N(t[j-1],vl,wbr,maskr);
  VecShr1N(t[j-1],vr,wbr);
  VecCopyN(vl,vx,wbr); VecXorN(vx,t[j-1],wbr); VecXorN(vx,vr,wbr); VecCopyN(t[j-2],vu,wbr); for i2:=0 to wbr-1 do t[j][i2]:=not (vx[i2] xor vu[i2]); VecMaskLast(t[j],wbr,maskr);
  end;
ok:=true;
VecShl1N(t[n-1],vl,wbr,maskr);
VecShr1N(t[n-1],vr,wbr);
VecCopyN(vl,vx,wbr); VecXorN(vx,t[n-1],wbr); VecXorN(vx,vr,wbr); VecXorN(vx,t[n-2],wbr);
for i:=0 to wbr-1 do if (vx[i] and (LongWord($FFFFFFFF)))<>0 then begin ok:=false; break; end;
GeneMat:=ok;
write(GeneMat);
end;

begin
{$ifdef disp}
CreateWin(m,m);
bb:=CreateBB(GetWin());
b:=CreateBMP(m,m);
{$endif}
for n:=1 to m do
  begin
  wbr:=(n+31) shr 5; wbp:=((n+1)+31) shr 5;
  if (n and 31)=0 then maskr:=$FFFFFFFF else maskr:=(LongWord(1) shl (n and 31)) - 1;
  if (((n+1) and 31)=0) then maskp:=$FFFFFFFF else maskp:=(LongWord(1) shl (((n+1) and 31))) - 1;
  write(n,#9);
  write('m',#9);MakeMat();
  write('c',#9);CalcMat2();
  write('g',#9);GeneMat();{$ifdef disp}write('%');PrintMat('_T2',t);{$endif}
  {$ifdef disp}if not(iswin()) then halt;{$endif}
  writeln();
  end;
end.
