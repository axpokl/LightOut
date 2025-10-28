program LightsOutAnyN;
type
  PByteMat = array of array of Byte;
  PByteVec = array of Byte;

function Idx(N,r,c:Integer):Integer; begin Idx:=r*N+c end;

procedure SetSizeMat(var A:PByteMat; n,m:Integer);
var i:Integer;
begin
  SetLength(A,n); for i:=0 to n-1 do SetLength(A[i],m);
end;

procedure SetSizeVec(var v:PByteVec; n:Integer);
begin
  SetLength(v,n);
end;

procedure ClearMat(var A:PByteMat);
var i,j:Integer;
begin
  for i:=0 to High(A) do for j:=0 to High(A[i]) do A[i][j]:=0;
end;

procedure ClearVec(var v:PByteVec);
var i:Integer;
begin
  for i:=0 to High(v) do v[i]:=0;
end;

procedure BuildM(N:Integer; var M:PByteMat);
var S,r,c,col,rowi:Integer;
begin
  S:=N*N; SetSizeMat(M,S,S); ClearMat(M);
  for r:=0 to N-1 do
    for c:=0 to N-1 do begin
      col:=Idx(N,r,c);
      rowi:=Idx(N,r,c); M[rowi][col]:=1;
      if r>0 then begin rowi:=Idx(N,r-1,c); M[rowi][col]:=1 end;
      if r<N-1 then begin rowi:=Idx(N,r+1,c); M[rowi][col]:=1 end;
      if c>0 then begin rowi:=Idx(N,r,c-1); M[rowi][col]:=1 end;
      if c<N-1 then begin rowi:=Idx(N,r,c+1); M[rowi][col]:=1 end;
    end;
end;

procedure BuildT(N:Integer; var Tm:PByteMat);
var S,r,c,rowi,col:Integer;
begin
  S:=N*N; SetSizeMat(Tm,S,S); ClearMat(Tm);
  for r:=0 to N-1 do
    for c:=0 to N-1 do begin
      rowi:=Idx(N,r,c);
      col:=Idx(N,r,c); Tm[rowi][col]:=1;
      if r>0 then begin col:=Idx(N,r-1,c); Tm[rowi][col]:=1 end;
      if r<N-1 then begin col:=Idx(N,r+1,c); Tm[rowi][col]:=1 end;
      if c>0 then begin col:=Idx(N,r,c-1); Tm[rowi][col]:=1 end;
      if c<N-1 then begin col:=Idx(N,r,c+1); Tm[rowi][col]:=1 end;
    end;
end;

procedure MatMulMod2(const A,B:PByteMat; var C:PByteMat);
var i,j,k,ni,nk,nj:Integer; s:Byte;
begin
  ni:=Length(A); nk:=Length(A[0]); nj:=Length(B[0]);
  SetSizeMat(C,ni,nj);
  for i:=0 to ni-1 do
    for j:=0 to nj-1 do begin
      s:=0;
      for k:=0 to nk-1 do if (A[i][k]<>0) and (B[k][j]<>0) then s:=s xor 1;
      C[i][j]:=s;
    end;
end;

procedure MatVecMulMod2(const A:PByteMat; const v:PByteVec; var outv:PByteVec);
var i,j,ni,nj:Integer; s:Byte;
begin
  ni:=Length(A); nj:=Length(A[0]); SetSizeVec(outv,ni);
  for i:=0 to ni-1 do begin
    s:=0; for j:=0 to nj-1 do if (A[i][j]<>0) and (v[j]<>0) then s:=s xor 1;
    outv[i]:=s;
  end;
end;

procedure BuildGoalAllOn(n:Integer; var v:PByteVec);
var i:Integer;
begin
  SetSizeVec(v,n); for i:=0 to n-1 do v[i]:=1;
end;

procedure BuildPermutation(N:Integer; var Perm,InvPerm:PByteVec; var GStart,GSize:PByteVec);
var S,i,r,c,idxCur,g:Integer; pr,pc:array[0..3] of Integer;
begin
  S:=N*N; SetSizeVec(Perm,S); SetSizeVec(InvPerm,S); SetSizeVec(GStart,4); SetSizeVec(GSize,4);
  pr[0]:=0;pc[0]:=0; pr[1]:=0;pc[1]:=1; pr[2]:=1;pc[2]:=0; pr[3]:=1;pc[3]:=1;
  idxCur:=0;
  for g:=0 to 3 do begin
    GStart[g]:=idxCur;
    for r:=0 to N-1 do for c:=0 to N-1 do
      if ((r and 1)=pr[g]) and ((c and 1)=pc[g]) then begin Perm[idxCur]:=Idx(N,r,c); inc(idxCur) end;
    GSize[g]:=idxCur-GStart[g];
  end;
  for i:=0 to S-1 do InvPerm[ Perm[i] ]:=i;
end;

procedure ExtractBlock(const A:PByteMat; starti,sz:Integer; var B:PByteMat);
var i,j:Integer;
begin
  SetSizeMat(B,sz,sz);
  for i:=0 to sz-1 do for j:=0 to sz-1 do B[i][j]:=A[starti+i][starti+j];
end;

procedure SolveLinearGF2(var A:PByteMat; var b:PByteVec; var x:PByteVec);
var k,i,j,row,col,pivot:Integer; tmp:Byte; pivcol:PByteVec; T: PByteMat; tb:PByteVec;
begin
  k:=Length(b); SetSizeVec(pivcol,k); for i:=0 to k-1 do pivcol[i]:=255;
  SetSizeMat(T,k,k); for i:=0 to k-1 do for j:=0 to k-1 do T[i][j]:=A[i][j];
  SetSizeVec(tb,k); for i:=0 to k-1 do tb[i]:=b[i];
  row:=0;
  for col:=0 to k-1 do begin
    pivot:=-1; for i:=row to k-1 do if T[i][col]<>0 then begin pivot:=i; break end;
    if pivot=-1 then continue;
    if pivot<>row then begin
      for j:=0 to k-1 do begin tmp:=T[pivot][j]; T[pivot][j]:=T[row][j]; T[row][j]:=tmp end;
      tmp:=tb[pivot]; tb[pivot]:=tb[row]; tb[row]:=tmp;
    end;
    pivcol[row]:=col;
    for i:=0 to k-1 do if (i<>row) and (T[i][col]<>0) then begin
      for j:=0 to k-1 do T[i][j]:=T[i][j] xor T[row][j];
      tb[i]:=tb[i] xor tb[row];
    end;
    inc(row); if row=k then break;
  end;
  SetSizeVec(x,k); for i:=0 to k-1 do x[i]:=0;
  for i:=k-1 downto 0 do if pivcol[i]<>255 then begin
    col:=pivcol[i]; tmp:=tb[i];
    for j:=col+1 to k-1 do if (T[i][j]<>0) and (x[j]<>0) then tmp:=tmp xor 1;
    x[col]:=tmp;
  end;
end;

procedure SolveBlocks(N:Integer; const Mprime:PByteMat; const RHSperm,Perm,GStart,GSize:PByteVec; var PressPerm:PByteVec);
var g,i,S,starti,sz:Integer; BlockA:PByteMat; BlockB,BlockX:PByteVec;
begin
  S:=N*N; SetSizeVec(PressPerm,S); for i:=0 to S-1 do PressPerm[i]:=0;
  for g:=0 to 3 do begin
    starti:=GStart[g]; sz:=GSize[g];
    if sz=0 then continue;
    ExtractBlock(Mprime,starti,sz,BlockA);
    SetSizeVec(BlockB,sz); for i:=0 to sz-1 do BlockB[i]:=RHSperm[starti+i];
    SolveLinearGF2(BlockA,BlockB,BlockX);
    for i:=0 to sz-1 do PressPerm[starti+i]:=BlockX[i];
  end;
end;

procedure PermuteMatVec(const A:PByteMat; const Perm:PByteVec; var AP:PByteMat);
var i,j,S:Integer;
begin
  S:=Length(Perm); SetSizeMat(AP,S,S);
  for i:=0 to S-1 do for j:=0 to S-1 do AP[i][j]:=A[Perm[i]][Perm[j]];
end;

procedure PermuteVec(const v,Perm:PByteVec; var vp:PByteVec);
var i,S:Integer;
begin
  S:=Length(Perm); SetSizeVec(vp,S); for i:=0 to S-1 do vp[i]:=v[Perm[i]];
end;

procedure UnpermutePress(const PressPerm,Perm:PByteVec; var Press:PByteVec);
var i,S:Integer;
begin
  S:=Length(Perm); SetSizeVec(Press,S);
  for i:=0 to S-1 do Press[ Perm[i] ]:=PressPerm[i];
end;

procedure VecXor(const A,B:PByteVec; var C:PByteVec);
var i:Integer;
begin
  SetSizeVec(C,Length(A)); for i:=0 to High(A) do C[i]:=A[i] xor B[i];
end;

function SolveFullLinear(const M:PByteMat; const b:PByteVec; var x:PByteVec):Boolean;
var A:PByteMat; bb:PByteVec; i,j,S,row,col,pivot:Integer; tmp:Byte; pivcol:PByteVec;
begin
  S:=Length(b); SetSizeMat(A,S,S); for i:=0 to S-1 do for j:=0 to S-1 do A[i][j]:=M[i][j];
  SetSizeVec(bb,S); for i:=0 to S-1 do bb[i]:=b[i];
  SetSizeVec(pivcol,S); for i:=0 to S-1 do pivcol[i]:=255;
  row:=0;
  for col:=0 to S-1 do begin
    pivot:=-1; for i:=row to S-1 do if A[i][col]<>0 then begin pivot:=i; break end;
    if pivot=-1 then continue;
    if pivot<>row then begin
      for j:=0 to S-1 do begin tmp:=A[pivot][j]; A[pivot][j]:=A[row][j]; A[row][j]:=tmp end;
      tmp:=bb[pivot]; bb[pivot]:=bb[row]; bb[row]:=tmp;
    end;
    pivcol[row]:=col;
    for i:=0 to S-1 do if (i<>row) and (A[i][col]<>0) then begin
      for j:=0 to S-1 do A[i][j]:=A[i][j] xor A[row][j];
      bb[i]:=bb[i] xor bb[row];
    end;
    inc(row);
  end;
  for i:=row to S-1 do if (bb[i]<>0) then begin SolveFullLinear:=False; exit end;
  SetSizeVec(x,S); for i:=0 to S-1 do x[i]:=0;
  for i:=row-1 downto 0 do if pivcol[i]<>255 then begin
    col:=pivcol[i]; tmp:=bb[i];
    for j:=col+1 to S-1 do if (A[i][j]<>0) and (x[j]<>0) then tmp:=tmp xor 1;
    x[col]:=tmp;
  end;
  SolveFullLinear:=True;
end;

procedure SolveLightsOut(N:Integer);
var S,i,j:Integer;
  M,Tm,Mprime,AP:PByteMat;
  Goal,RHS,RHSperm,Perm,InvPerm,GStart,GSize,PressPerm,Press,Ach,Residual,Fix,FinalPress:PByteVec;
begin
  S:=N*N;
  BuildM(N,M);
  BuildT(N,Tm);
  MatMulMod2(Tm,M,Mprime);
  BuildGoalAllOn(S,Goal);
  MatVecMulMod2(Tm,Goal,RHS);
  BuildPermutation(N,Perm,InvPerm,GStart,GSize);
  PermuteMatVec(Mprime,Perm,AP);
  PermuteVec(RHS,Perm,RHSperm);
  SolveBlocks(N,AP,RHSperm,Perm,GStart,GSize,PressPerm);
  UnpermutePress(PressPerm,Perm,Press);
  MatVecMulMod2(M,Press,Ach);
  VecXor(Goal,Ach,Residual);
  if not SolveFullLinear(M,Residual,Fix) then begin
    writeln('No solution');
    exit;
  end;
  VecXor(Press,Fix,FinalPress);
  writeln('Press matrix (1=press):');
  for i:=0 to N-1 do begin
    for j:=0 to N-1 do begin
      write(FinalPress[Idx(N,i,j)]);
      if j<N-1 then write(' ');
    end;
    writeln;
  end;
end;

var N:Integer;
begin
  if ParamCount>=1 then Val(ParamStr(1),N) else readln(N);
  if N<=0 then begin writeln('N must be >=1'); halt(1) end;
  SolveLightsOut(N);
end.
