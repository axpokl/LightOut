program LightsOutParityRec;
const
  N = 5;
type
  Mat = array[0..N-1,0..N-1] of Byte;

procedure Transform(const Goal:Mat; H,W:Integer; var Bout:Mat);
var r,c:Integer;
begin
  for r:=0 to H-1 do
    for c:=0 to W-1 do begin
      Bout[r,c]:=Goal[r,c];
      if r>0 then Bout[r,c]:=Bout[r,c] xor Goal[r-1,c];
      if r+1<H then Bout[r,c]:=Bout[r,c] xor Goal[r+1,c];
      if c>0 then Bout[r,c]:=Bout[r,c] xor Goal[r,c-1];
      if c+1<W then Bout[r,c]:=Bout[r,c] xor Goal[r,c+1];
    end;
end;

function RowsOfParity(H,par:Integer):Integer;
begin
  if par=0 then RowsOfParity:=(H+1) div 2 else RowsOfParity:=H div 2;
end;

function ColsOfParity(W,par:Integer):Integer;
begin
  if par=0 then ColsOfParity:=(W+1) div 2 else ColsOfParity:=W div 2;
end;

function TrySolve1D(len:Integer; const goalArr:array of Byte; var pressArr:array of Byte; firstVal:Byte):Boolean;
var i:Integer;
begin
  if len=1 then begin
    pressArr[0]:=firstVal;
    TrySolve1D := (pressArr[0]=goalArr[0]);
    exit;
  end;
  pressArr[0]:=firstVal;
  pressArr[1]:=goalArr[0] xor pressArr[0];
  for i:=1 to len-2 do
    pressArr[i+1]:=goalArr[i] xor pressArr[i] xor pressArr[i-1];
  TrySolve1D := ((pressArr[len-2] xor pressArr[len-1])=goalArr[len-1]);
end;

procedure Solve1DRow(W:Integer; const GoalMat:Mat; var PressMat:Mat);
var g0:array[0..N-1] of Byte;
    p0,p1:array[0..N-1] of Byte;
    j:Integer; ok0,ok1:Boolean;
begin
  for j:=0 to W-1 do g0[j]:=GoalMat[0,j];
  ok0:=TrySolve1D(W,g0,p0,0);
  ok1:=TrySolve1D(W,g0,p1,1);
  if ok0 then for j:=0 to W-1 do PressMat[0,j]:=p0[j]
  else if ok1 then for j:=0 to W-1 do PressMat[0,j]:=p1[j]
  else for j:=0 to W-1 do PressMat[0,j]:=0;
end;

procedure Solve1DCol(H:Integer; const GoalMat:Mat; var PressMat:Mat);
var g0:array[0..N-1] of Byte;
    p0,p1:array[0..N-1] of Byte;
    i:Integer; ok0,ok1:Boolean;
begin
  for i:=0 to H-1 do g0[i]:=GoalMat[i,0];
  ok0:=TrySolve1D(H,g0,p0,0);
  ok1:=TrySolve1D(H,g0,p1,1);
  if ok0 then for i:=0 to H-1 do PressMat[i,0]:=p0[i]
  else if ok1 then for i:=0 to H-1 do PressMat[i,0]:=p1[i]
  else for i:=0 to H-1 do PressMat[i,0]:=0;
end;

procedure SolveGrid(H,W:Integer; const GoalMat:Mat; var PressMat:Mat);
var
  Bmat:Mat;
  pr,pc,i,j,hr,wc:Integer;
  SubGoal,SubPress:Mat;
begin
  for i:=0 to H-1 do
    for j:=0 to W-1 do
      PressMat[i,j]:=0;

  if (H=0) or (W=0) then exit;

  if (H=1) and (W=1) then begin
    PressMat[0,0]:=GoalMat[0,0];
    exit;
  end;

  if (H=1) then begin
    Solve1DRow(W,GoalMat,PressMat);
    exit;
  end;

  if (W=1) then begin
    Solve1DCol(H,GoalMat,PressMat);
    exit;
  end;

  Transform(GoalMat,H,W,Bmat);

  for pr:=0 to 1 do
    for pc:=0 to 1 do begin
      hr:=RowsOfParity(H,pr);
      wc:=ColsOfParity(W,pc);
      for i:=0 to hr-1 do
        for j:=0 to wc-1 do begin
          SubGoal[i,j]:=Bmat[2*i+pr,2*j+pc];
          SubPress[i,j]:=0;
        end;
      SolveGrid(hr,wc,SubGoal,SubPress);
      for i:=0 to hr-1 do
        for j:=0 to wc-1 do
          PressMat[2*i+pr,2*j+pc]:=SubPress[i,j];
    end;
end;

var
  GoalAllOn:Mat;
  PressAns:Mat;
  r,c:Integer;
begin
  for r:=0 to N-1 do
    for c:=0 to N-1 do begin
      GoalAllOn[r,c]:=1;
      PressAns[r,c]:=0;
    end;
  SolveGrid(N,N,GoalAllOn,PressAns);
  writeln('Press matrix (1=press):');
  for r:=0 to N-1 do begin
    for c:=0 to N-1 do begin
      write(PressAns[r,c]);
      if c<N-1 then write(' ');
    end;
    writeln;
  end;
end.
