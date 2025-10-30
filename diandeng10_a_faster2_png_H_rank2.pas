{$define disp}
program diandeng;

{$ifdef disp}
uses display;
{$endif}

const m=1000;

type TMat=array[-1..m,-1..m]of Boolean;

var n:longword;
var a,l,r,t:TMat;
var i,j,k:longint;

{$ifdef disp}
var bb:pbitbuf;
var s:longword=0;
var b:pbitmap;
{$endif}

procedure PrintMat(mat:TMat);
var i,j:longint;
begin
writeln();
for j:=0 to n-1 do
  begin
//  if mat[j,-1] then write('#') else write('.');
  for i:=0 to n-1 do
    if mat[j,i] then write('#') else write('.');
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
    if mat[j,i] then SetBBPixel(bb,i,j,black) else SetBBPixel(bb,i,j,white);
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
begin
for i:=0 to n-1 do l[0,i]:=False;
l[-1,0]:=False;
for j:=1 to n do
  for i:=0 to n-1 do
    begin
    l[j,i]:=not(l[j-1,i-1] xor l[j-1,i] xor l[j-1,i+1] xor l[j-2,i]);
    l[j,i]:=l[j,i] xor a[j-1,i];
    end;
for i:=0 to n-1 do l[-1,i]:=False;
l[-1,0]:=True;
for j:=0 to n-1 do
  for i:=0 to n-1 do
    begin
    l[j,i]:=(l[j-1,i-1] xor l[j-1,i] xor l[j-1,i+1]);
    if j>0 then l[j,i]:=l[j,i] xor l[j-2,i];
    end;
for i:=0 to n-1 do l[0,i]:=l[n-1,i];
for j:=1 to n-1 do
  for i:=0 to n-1 do
    begin
    l[j,i]:=(l[j-1,i-1] xor l[j-1,i+1]);
    if j>1 then l[j,i]:=l[j,i] xor l[j-2,i];
    end;
for i:=0 to n-1 do begin l[i,-1]:=l[n,i];l[n,i]:=False;end;
for i:=0 to n-1 do for j:=0 to n-1 do r[i,j]:=(i=j);
end;

procedure CalcMat();
var j0:longint;
begin
for k:=0 to n-1 do
  begin
  j0:=-1;
  for j:=n-1 downto k do
    if l[j,k] then j0:=j;
  j:=j0;
  if j>=0 then
    begin
    if j<>k then
      for i:=-1 to n-1 do
        begin
        l[j,i]:=l[j,i] xor l[k,i];
        l[k,i]:=l[j,i] xor l[k,i];
        l[j,i]:=l[j,i] xor l[k,i];
        r[j,i]:=r[j,i] xor r[k,i];
        r[k,i]:=r[j,i] xor r[k,i];
        r[j,i]:=r[j,i] xor r[k,i];
        end;
    for j:=k+1 to n-1 do
      if l[j,k] then
        begin
        for i:=0 to n-1 do //for a-1
          begin
          l[j,i]:=l[j,i] xor l[k,i];
          r[j,i]:=r[j,i] xor r[k,i];
          end;
        l[j,-1]:=l[j,-1] xor l[k,-1];
        r[j,-1]:=r[j,-1] xor r[k,-1];
        end;
    end;
  end;
for i:=n-1 downto 0 do
  if l[i,i] then
    for j:=i-1 downto 0 do
      if l[j,i] then
        begin
        for k:=0 to n-1 do // for a-1
          begin
          l[j,k]:=l[j,k] xor l[i,k];
          r[j,k]:=r[j,k] xor r[i,k];
          end;
        l[j,-1]:=l[j,-1] xor l[i,-1];
        r[j,-1]:=r[j,-1] xor r[i,-1];
        end;
end;

function rank(n:LongInt):LongInt;
var len,i,k,da,db,shift,j,resdeg:LongInt;
    f0,f1,fn,tmp,fa:array[0..m+1] of Byte;
    g0,g1,tmp2,fb:array[0..m+1] of Byte;
    A,B,R:array[0..m+1] of Byte;
    zeroB:Boolean;
begin
  len:=n+2;
  for i:=0 to len-1 do begin f0[i]:=0;f1[i]:=0;fn[i]:=0;tmp[i]:=0;fa[i]:=0;g0[i]:=0;g1[i]:=0;tmp2[i]:=0;fb[i]:=0;A[i]:=0;B[i]:=0;R[i]:=0;end;
  f0[0]:=1;
  if len>1 then f1[1]:=1;
  if n=0 then begin for i:=0 to len-1 do fa[i]:=f0[i]; end
  else if n=1 then begin for i:=0 to len-1 do fa[i]:=f1[i]; end
  else begin
    for k:=1 to n-1 do begin
      for i:=0 to len-1 do tmp[i]:=0;
      for i:=1 to len-1 do tmp[i]:=f1[i-1];
      for i:=0 to len-1 do fn[i]:=tmp[i] xor f0[i];
      for i:=0 to len-1 do f0[i]:=f1[i];
      for i:=0 to len-1 do f1[i]:=fn[i];
    end;
    for i:=0 to len-1 do fa[i]:=f1[i];
  end;
  for i:=0 to len-1 do begin g0[i]:=0;g1[i]:=0;tmp2[i]:=0;end;
  g0[0]:=1;
  g1[0]:=1;
  if len>1 then g1[1]:=1;
  if n=0 then begin for i:=0 to len-1 do fb[i]:=g0[i]; end
  else if n=1 then begin for i:=0 to len-1 do fb[i]:=g1[i]; end
  else begin
    for k:=1 to n-1 do begin
      for i:=0 to len-1 do begin
        if i=0 then tmp2[i]:=g1[0] else tmp2[i]:=g1[i] xor g1[i-1];
      end;
      for i:=0 to len-1 do fn[i]:=tmp2[i] xor g0[i];
      for i:=0 to len-1 do g0[i]:=g1[i];
      for i:=0 to len-1 do g1[i]:=fn[i];
    end;
    for i:=0 to len-1 do fb[i]:=g1[i];
  end;
  for i:=0 to len-1 do begin A[i]:=fa[i];B[i]:=fb[i];end;
  while true do begin
    zeroB:=true;
    for i:=0 to len-1 do if B[i]<>0 then begin zeroB:=false;break;end;
    if zeroB then break;
    for i:=0 to len-1 do R[i]:=A[i];
    db:=-1;
    for i:=len-1 downto 0 do if B[i]<>0 then begin db:=i;break;end;
    if db>=0 then begin
      while true do begin
        da:=-1;
        for i:=len-1 downto 0 do if R[i]<>0 then begin da:=i;break;end;
        if (da<db) or (da<0) then break;
        shift:=da-db;
        for j:=0 to db do if B[j]<>0 then R[j+shift]:=R[j+shift] xor 1;
      end;
    end;
    for i:=0 to len-1 do A[i]:=B[i];
    for i:=0 to len-1 do B[i]:=R[i];
  end;
  resdeg:=-1;
  for i:=len-1 downto 0 do if A[i]<>0 then begin resdeg:=i;break;end;
  if resdeg<0 then resdeg:=0;
  rank:=resdeg;
end;


procedure CalcMat2;
var
  nn:LongInt;

  // Krylov 基: vN[j,i] = (H^j e1)[i]
  vN:array[0..m-1,0..m-1]of Boolean;

  // pN(x): A = pN(H)
  cN,pN,row0,bvec,xvec:array[0..m-1]of Boolean;

  // chiN(x) = χ_n(x)
  prev2,prev1,cura,chiN:array[0..m]of Boolean;

  // gcd 部分
  gr0,gr1,gr2,qpoly,tmpdiv,dpoly:array[0..m]of Boolean;

  // 多项式除法结果
  rem,quot,tmpq:array[0..m]of Boolean;
  pPrime,chiPrime:array[0..m]of Boolean;

  // 扩展欧几里得 #1: 求 vcoef = pPrime^{-1} mod chiPrime
  r0a,r1a,r2a,s0a,s1a,s2a,t0a,t1a,t2a,q2,qs1,qt1,tmp:array[0..m]of Boolean;
  vcoef:array[0..m]of Boolean;

  // 扩展欧几里得 #2: 求 alphacoef = dpoly^{-1} mod chiPrime
  r0b,r1b,r2b,s0b,s1b,s2b,t0b,t1b,t2b,q3,qs1b,qt1b,tmpb:array[0..m]of Boolean;
  alphacoef:array[0..m]of Boolean;

  // g(x) = alphacoef * vcoef mod chiPrime
  mulpoly:array[0..2*m]of Boolean;
  rem2:array[0..2*m]of Boolean;
  gpoly:array[0..m]of Boolean;

  ii,jj,kk:LongInt;
  deg_r1,deg_r2,db,sh,deg_div,deg_rem,deg_chiPrime,highest:LongInt;
  left,right,s:boolean;
begin
  nn:=n;

  // ---------- Step 1. Krylov 基 vN ----------
  for jj:=0 to nn-1 do
    for ii:=0 to nn-1 do
      vN[jj,ii]:=false;
  vN[0,0]:=true; // e1
  for jj:=1 to nn-1 do
    for ii:=0 to nn-1 do
    begin
      left  := (ii>0)    and vN[jj-1,ii-1];
      right := (ii<nn-1) and vN[jj-1,ii+1];
      vN[jj,ii]:= left xor right;
    end;

  // ---------- Step 2. 用 A 的第一列恢复 pN ----------
  for ii:=0 to nn-1 do
  begin
    cN[ii]:=l[ii,0]; // A[:,0]
    pN[ii]:=false;
  end;
  for ii:=nn-1 downto 0 do
  begin
    s:=cN[ii];
    for jj:=ii+1 to nn-1 do
      if vN[jj,ii] and pN[jj] then
        s:=s xor true;
    pN[ii]:=s;
  end;

  // ---------- Step 3. 递推得到 χ_n(x) = chiN ----------
  for ii:=0 to nn do
  begin
    prev2[ii]:=false;
    prev1[ii]:=false;
    chiN[ii]:=false;
  end;
  prev2[0]:=true;
  if nn>0 then prev1[1]:=true;
  if nn=1 then
  begin
    for ii:=0 to nn do chiN[ii]:=prev1[ii];
  end
  else
  begin
    for kk:=2 to nn do
    begin
      for ii:=0 to nn do cura[ii]:=false;
      // cura = x*prev1 + prev2  (GF(2))
      for ii:=0 to nn-1 do
        if prev1[ii] then
          cura[ii+1]:=cura[ii+1] xor true;
      for ii:=0 to nn do
        if prev2[ii] then
          cura[ii]:=cura[ii] xor true;
      for ii:=0 to nn do
      begin
        prev2[ii]:=prev1[ii];
        prev1[ii]:=cura[ii];
      end;
    end;
    for ii:=0 to nn do chiN[ii]:=prev1[ii];
  end;

  // ---------- Step 4. gcd(pN, chiN) -> dpoly ----------
  for ii:=0 to nn do
  begin
    gr0[ii]:=false; gr1[ii]:=false; gr2[ii]:=false;
    qpoly[ii]:=false; tmpdiv[ii]:=false;
    dpoly[ii]:=false;
  end;
  for ii:=0 to nn-1 do gr0[ii]:=pN[ii];
  for ii:=0 to nn   do gr1[ii]:=chiN[ii];

  while true do
  begin
    deg_r1:=-1;
    for ii:=nn downto 0 do
      if gr1[ii] then begin deg_r1:=ii; break; end;
    if deg_r1<0 then break;

    for ii:=0 to nn do
    begin
      gr2[ii]:=gr0[ii];
      qpoly[ii]:=false;
    end;
    db:=deg_r1;
    while true do
    begin
      deg_r2:=-1;
      for ii:=nn downto 0 do
        if gr2[ii] then begin deg_r2:=ii; break; end;
      if (deg_r2<db) or (deg_r2<0) then break;
      sh:=deg_r2-db;
      qpoly[sh]:=qpoly[sh] xor true;
      for ii:=0 to nn do tmpdiv[ii]:=false;
      for ii:=0 to nn-sh do
        if gr1[ii] then
          tmpdiv[ii+sh]:=tmpdiv[ii+sh] xor true;
      for ii:=0 to nn do
        gr2[ii]:=gr2[ii] xor tmpdiv[ii];
    end;

    for ii:=0 to nn do
    begin
      gr0[ii]:=gr1[ii];
      gr1[ii]:=gr2[ii];
    end;
  end;
  for ii:=0 to nn do
    dpoly[ii]:=gr0[ii]; // d(x)=gcd(p,chi)

  // ---------- Step 5. 求 pPrime = pN/dpoly, chiPrime = chiN/dpoly ----------
  // 5a. pPrime
  for ii:=0 to nn do
  begin
    rem[ii]:=false; quot[ii]:=false; tmpq[ii]:=false;
  end;
  for ii:=0 to nn-1 do rem[ii]:=pN[ii];
  deg_div:=-1;
  for ii:=nn downto 0 do
    if dpoly[ii] then begin deg_div:=ii; break; end;
  while true do
  begin
    deg_rem:=-1;
    for ii:=nn downto 0 do
      if rem[ii] then begin deg_rem:=ii; break; end;
    if (deg_rem<deg_div) or (deg_rem<0) then break;
    sh:=deg_rem-deg_div;
    quot[sh]:=quot[sh] xor true;
    for ii:=0 to nn do tmpq[ii]:=false;
    for ii:=0 to nn-sh do
      if dpoly[ii] then
        tmpq[ii+sh]:=tmpq[ii+sh] xor true;
    for ii:=0 to nn do
      rem[ii]:=rem[ii] xor tmpq[ii];
  end;
  for ii:=0 to nn do
    pPrime[ii]:=quot[ii]; // p'(x)

  // 5b. chiPrime
  for ii:=0 to nn do
  begin
    rem[ii]:=chiN[ii];
    quot[ii]:=false;
    tmpq[ii]:=false;
  end;
  while true do
  begin
    deg_rem:=-1;
    for ii:=nn downto 0 do
      if rem[ii] then begin deg_rem:=ii; break; end;
    if (deg_rem<deg_div) or (deg_rem<0) then break;
    sh:=deg_rem-deg_div;
    quot[sh]:=quot[sh] xor true;
    for ii:=0 to nn do tmpq[ii]:=false;
    for ii:=0 to nn-sh do
      if dpoly[ii] then
        tmpq[ii+sh]:=tmpq[ii+sh] xor true;
    for ii:=0 to nn do
      rem[ii]:=rem[ii] xor tmpq[ii];
  end;
  for ii:=0 to nn do
    chiPrime[ii]:=quot[ii]; // χ'(x)=chiPrime

  // ---------- Step 6. vcoef = pPrime^{-1} mod chiPrime ----------
  for ii:=0 to nn do
  begin
    r0a[ii]:=false; r1a[ii]:=false; r2a[ii]:=false;
    s0a[ii]:=false; s1a[ii]:=false; s2a[ii]:=false;
    t0a[ii]:=false; t1a[ii]:=false; t2a[ii]:=false;
    q2[ii]:=false; qs1[ii]:=false; qt1[ii]:=false; tmp[ii]:=false;
    vcoef[ii]:=false;
  end;
  for ii:=0 to nn do r0a[ii]:=pPrime[ii];
  for ii:=0 to nn do r1a[ii]:=chiPrime[ii];
  s0a[0]:=true;   // s0 = 1
  t1a[0]:=true;   // t1 = 1

  while true do
  begin
    deg_r1:=-1;
    for ii:=nn downto 0 do if r1a[ii] then begin deg_r1:=ii; break; end;
    if deg_r1<0 then break;

    for ii:=0 to nn do
    begin
      q2[ii]:=false;
      r2a[ii]:=r0a[ii];
    end;
    db:=deg_r1;
    while true do
    begin
      deg_r2:=-1;
      for ii:=nn downto 0 do if r2a[ii] then begin deg_r2:=ii; break; end;
      if (deg_r2<db) or (deg_r2<0) then break;
      sh:=deg_r2-db;
      q2[sh]:=q2[sh] xor true;
      for ii:=0 to nn do tmp[ii]:=false;
      for ii:=0 to nn-sh do
        if r1a[ii] then
          tmp[ii+sh]:=tmp[ii+sh] xor true;
      for ii:=0 to nn do
        r2a[ii]:=r2a[ii] xor tmp[ii];
    end;

    // s2 = s0 xor q2*s1
    for ii:=0 to nn do qs1[ii]:=false;
    for sh:=0 to nn do
      if q2[sh] then
        for ii:=0 to nn-sh do
          if s1a[ii] then
            qs1[ii+sh]:=qs1[ii+sh] xor true;
    for ii:=0 to nn do
      s2a[ii]:=s0a[ii] xor qs1[ii];

    // t2 = t0 xor q2*t1
    for ii:=0 to nn do qt1[ii]:=false;
    for sh:=0 to nn do
      if q2[sh] then
        for ii:=0 to nn-sh do
          if t1a[ii] then
            qt1[ii+sh]:=qt1[ii+sh] xor true;
    for ii:=0 to nn do
      t2a[ii]:=t0a[ii] xor qt1[ii];

    for ii:=0 to nn do begin r0a[ii]:=r1a[ii]; r1a[ii]:=r2a[ii]; end;
    for ii:=0 to nn do begin s0a[ii]:=s1a[ii]; s1a[ii]:=s2a[ii]; end;
    for ii:=0 to nn do begin t0a[ii]:=t1a[ii]; t1a[ii]:=t2a[ii]; end;
  end;
  for ii:=0 to nn do
    vcoef[ii]:=s0a[ii]; // v(x)

  // ---------- Step 7. alphacoef = dpoly^{-1} mod chiPrime ----------
  for ii:=0 to nn do
  begin
    r0b[ii]:=false; r1b[ii]:=false; r2b[ii]:=false;
    s0b[ii]:=false; s1b[ii]:=false; s2b[ii]:=false;
    t0b[ii]:=false; t1b[ii]:=false; t2b[ii]:=false;
    q3[ii]:=false; qs1b[ii]:=false; qt1b[ii]:=false; tmpb[ii]:=false;
    alphacoef[ii]:=false;
  end;
  for ii:=0 to nn do r0b[ii]:=dpoly[ii];
  for ii:=0 to nn do r1b[ii]:=chiPrime[ii];
  s0b[0]:=true;   // s0 = 1
  t1b[0]:=true;   // t1 = 1

  while true do
  begin
    deg_r1:=-1;
    for ii:=nn downto 0 do if r1b[ii] then begin deg_r1:=ii; break; end;
    if deg_r1<0 then break;

    for ii:=0 to nn do
    begin
      q3[ii]:=false;
      r2b[ii]:=r0b[ii];
    end;
    db:=deg_r1;
    while true do
    begin
      deg_r2:=-1;
      for ii:=nn downto 0 do if r2b[ii] then begin deg_r2:=ii; break; end;
      if (deg_r2<db) or (deg_r2<0) then break;
      sh:=deg_r2-db;
      q3[sh]:=q3[sh] xor true;
      for ii:=0 to nn do tmpb[ii]:=false;
      for ii:=0 to nn-sh do
        if r1b[ii] then
          tmpb[ii+sh]:=tmpb[ii+sh] xor true;
      for ii:=0 to nn do
        r2b[ii]:=r2b[ii] xor tmpb[ii];
    end;

    // s2b = s0b xor q3*s1b
    for ii:=0 to nn do qs1b[ii]:=false;
    for sh:=0 to nn do
      if q3[sh] then
        for ii:=0 to nn-sh do
          if s1b[ii] then
            qs1b[ii+sh]:=qs1b[ii+sh] xor true;
    for ii:=0 to nn do
      s2b[ii]:=s0b[ii] xor qs1b[ii];

    // t2b = t0b xor q3*t1b
    for ii:=0 to nn do qt1b[ii]:=false;
    for sh:=0 to nn do
      if q3[sh] then
        for ii:=0 to nn-sh do
          if t1b[ii] then
            qt1b[ii+sh]:=qt1b[ii+sh] xor true;
    for ii:=0 to nn do
      t2b[ii]:=t0b[ii] xor qt1b[ii];

    for ii:=0 to nn do begin r0b[ii]:=r1b[ii]; r1b[ii]:=r2b[ii]; end;
    for ii:=0 to nn do begin s0b[ii]:=s1b[ii]; s1b[ii]:=s2b[ii]; end;
    for ii:=0 to nn do begin t0b[ii]:=t1b[ii]; t1b[ii]:=t2b[ii]; end;
  end;
  for ii:=0 to nn do
    alphacoef[ii]:=s0b[ii]; // α(x)

  // ---------- Step 8. g(x) = α(x) * v(x) mod chiPrime ----------
  for ii:=0 to 2*nn do
  begin
    mulpoly[ii]:=false;
    rem2[ii]:=false;
  end;
  for ii:=0 to nn do
    for jj:=0 to nn do
      if alphacoef[ii] and vcoef[jj] then
        mulpoly[ii+jj]:=mulpoly[ii+jj] xor true;

  // reduce mod chiPrime
  for ii:=0 to 2*nn do rem2[ii]:=mulpoly[ii];
  deg_chiPrime:=-1;
  for ii:=nn downto 0 do
    if chiPrime[ii] then begin deg_chiPrime:=ii; break; end;
  for highest:=2*nn downto deg_chiPrime do
    if (highest>=0) and rem2[highest] then
    begin
      sh:=highest-deg_chiPrime;
      for ii:=0 to deg_chiPrime do
        if chiPrime[ii] then
          rem2[ii+sh]:=rem2[ii+sh] xor true;
    end;

  for ii:=0 to nn-1 do
    gpoly[ii]:=rem2[ii];

  // ---------- Step 9. R 的第0行 row0 = g(H) e1 = sum_j gpoly[j]*(H^j e1) ----------
  for ii:=0 to nn-1 do
    row0[ii]:=false;
  for jj:=0 to nn-1 do
    if gpoly[jj] then
      for ii:=0 to nn-1 do
        if vN[jj,ii] then
          row0[ii]:=row0[ii] xor true;

  // ---------- Step 10. 用三向递推填满整张 R ----------
  for ii:=0 to nn-1 do
    r[0,ii]:=row0[ii];
  for jj:=1 to nn-1 do
    for ii:=0 to nn-1 do
    begin
      s:=false;
      if (ii>0)    and r[jj-1,ii-1] then s:=s xor true;
      if (ii<nn-1) and r[jj-1,ii+1] then s:=s xor true;
      if (jj>=2)   and r[jj-2,ii]   then s:=s xor true;
      r[jj,ii]:=s;
    end;

  // ---------- Step 11. x = R * bvec，回写到 l[*,-1] ----------
  for ii:=0 to nn-1 do
    bvec[ii]:=l[ii,-1];
  for ii:=0 to nn-1 do
  begin
    s:=false;
    for jj:=0 to nn-1 do
      if r[ii,jj] and bvec[jj] then
        s:=s xor true;
    xvec[ii]:=s;
  end;
  for ii:=0 to nn-1 do
    l[ii,-1]:=xvec[ii];
end;



procedure GeneMat();
begin
for i:=0 to n-1 do
  begin
  t[0,i]:=l[i,-1];
  l[i,-1]:=false;
  end;
for j:=1 to n-1 do
  for i:=0 to n-1 do
    t[j,i]:=not(t[j-1,i-1] xor t[j-1,i] xor t[j-1,i+1] xor t[j-2,i]) xor a[j-1,i];
end;

begin
{$ifdef disp}
CreateWin(m,m);
bb:=CreateBB(GetWin());
b:=CreateBMP(m,m);
{$endif}
for n:=1 to 20 do
  begin
  write(n,#9);
  write('m');MakeMat();{$ifdef disp}write('%');PrintMat('_A',l);{$endif}
  write('c');CalcMat2();{$ifdef disp}write('%');PrintMat('_E',l);write('%');PrintMat('_R',r);{$endif}
  write('g');GeneMat();{$ifdef disp}write('%');PrintMat('_T',t);{$endif}
//  write(#9,s,#9,n*n,#9,s/n/n:0:5);
  {$ifdef disp}if not(iswin()) then halt;{$endif}
  writeln();
  end;
end.
