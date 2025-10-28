program rcalc2;
const MAXN=4096;
function ROfN(n:LongInt):LongInt;
var len,i,k,da,db,shift,j,resdeg:LongInt;
    f0,f1,fn,tmp,fa:array[0..MAXN-1] of Byte;
    g0,g1,tmp2,fb:array[0..MAXN-1] of Byte;
    A,B,R:array[0..MAXN-1] of Byte;
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
  ROfN:=resdeg;
end;
var i:LongInt;
begin
  for i:=0 to 1000 do
    writeln('n=',i,' r(n)=',ROfN(i));
end.
