program diandeng;
uses display;

const m=100;
var i,j,k,n,l,t:longint;
var b:boolean;

type TMat=packed array[0..m-1,0..m-1]of boolean;
type TVet=packed array[0..m-1]of boolean;

const MatC:array[boolean]of longword=(black,white);

procedure MPrint(Mat:TMat);
var i,j:longint;
begin
for j:=0 to n-1 do
  for i:=0 to n-1 do
    SetPixel(j,i,MatC[Mat[i,j]]);
while IsNextMsg do ;
freshwin();
end;

procedure MPrintPNG(Mat:TMat);
var b:pbitmap;
begin
b:=CreateBMP(n,n);
for j:=0 to n-1 do
  for i:=0 to n-1 do
    Bar(b,j,i,1,1,MatC[Mat[i,j]]);
SaveBMP(b,'png/'+i2s(n)+'.png');
ReleaseBMP(b);
end;

procedure VPrint(Vet:TVet);
var i,j:longint;
begin
j:=n;
  for i:=0 to n-1 do
    SetPixel(j,i,MatC[Vet[i]]);
while IsNextMsg do ;
freshwin();
end;

procedure MInit(var Mat:TMat;b:boolean);
begin
for i:=0 to n-1 do
  for j:=0 to n-1 do
    Mat[i,j]:=b;
end;

procedure MInit(var Mat:TMat);
begin
MInit(Mat,false);
end;

procedure MInitE(var Mat:TMat);
begin
MInit(Mat);
for i:=0 to n-1 do
  Mat[i,i]:=true;
end;

procedure MInitH(var Mat:TMat);
begin
MInit(Mat);
for i:=0 to n-1 do
  begin
  if i-1>=0 then Mat[i,i-1]:=true;
  Mat[i,i]:=true;
  if i+1<=n-1 then Mat[i,i+1]:=true;
  end;
end;

procedure MMulV(var VetO:TVet;Mat:TMat;Vet:TVet);
begin
for i:=0 to n-1 do
  begin
  b:=false;
  for j:=0 to n-1 do
    b:=b xor (Mat[i,j] and Vet[j]);
  VetO[i]:=b;
  end;
end;

procedure MMulH(var MatO:TMat;Mat:TMat);
begin
for i:=0 to n-1 do
  for j:=0 to n-1 do
    begin
    b:=Mat[i,j];
    if i-1>=0 then b:=b xor Mat[i-1,j];
    if i+1<=n-1 then b:=b xor Mat[i+1,j];
    MatO[i,j]:=b;
    end;
end;

procedure MSum(var MatO:TMat;Mat:TMat);
begin
for i:=0 to n-1 do
  for j:=0 to n-1 do
    MatO[i,j]:=MatO[i,j] xor Mat[i,j];
end;

procedure MCpy(var MatO:TMat;Mat:TMat);
begin
for i:=0 to n-1 do
  for j:=0 to n-1 do
    MatO[i,j]:=Mat[i,j];
end;

procedure VSum(Var VetO:TVet;Vet:TVet);
begin
for i:=0 to n-1 do
  VetO[i]:=VetO[i] xor Vet[i];
end;

procedure Solve(Mat:TMat;var Vet:TVet);
begin
for j:=0 to n-1 do
  begin
  if Mat[j,j]=false then
    begin
    t:=0;
    for i:=j+1 to n-1 do
      if Mat[i,j]=true then t:=i;
    if t<>0 then
      begin
      for l:=j to n-1 do
        Mat[j,l]:=Mat[t,l] xor Mat[j,l];
      Vet[j]:=Vet[t] xor Vet[j];
      end;
    end;
  for i:=j+1 to n-1 do
    if Mat[i,j]=true then
      begin
      for l:=j to n-1 do
        Mat[i,l]:=Mat[j,l] xor Mat[i,l];
      Vet[i]:=Vet[j] xor Vet[i];
      end;
  MPrint(Mat);VPrint(Vet);
  end;
for j:=n-1 downto 0 do
  begin
  for i:=j-1 downto 0 do
    if Mat[i,j]=true then
      begin
      for l:=j to n-1 do
        Mat[i,l]:=Mat[j,l] xor Mat[i,l];
      Vet[i]:=Vet[j] xor Vet[i];
      end;
  MPrint(Mat);VPrint(Vet);
  end;
end;

procedure SolveV2M(Var Mat:TMat;Vet:TVet);
var M1:TMat;
begin
MInit(M1,true);
MInit(Mat,false);
for j:=n-1 downto 0 do
  for i:=0 to n-1 do
    begin
    if j=n-1 then b:=Vet[i]
    else b:=M1[i,j+1];
    if b then
      begin
      Mat[j,i]:=not(Mat[j,i]);
      M1[i,j]:=not(M1[i,j]);
      if j-1>=0 then M1[i,j-1]:=not(M1[i,j-1]);
      if i-1>=0 then M1[i-1,j]:=not(M1[i-1,j]);
      if i+1<=n-1 then M1[i+1,j]:=not(M1[i+1,j]);
      end;
    end;
end;

var MP0,MP1,MTP,MINI,MR:TMat;
var VME,VTP:TVet;

begin
CreateWin(m,m);
for n:=1 to m do
begin
write(n);
MInit(MINI,true);
MInitE(MP0);
MInitH(MP1);
MMulV(VME,MP0,MINI[0]);
MMulV(VTP,MP1,MINI[1]);
VSum(VME,VTP);
for k:=2 to n do
  begin
  MMulH(MTP,MP1);
  MSum(MTP,MP0);
  MCpy(MP0,MP1);
  MCpy(MP1,MTP);
  if(k<n) then
    begin
    MMulV(VTP,MP1,MINI[i]);
    VSum(VME,VTP);
    end;
  end;
Solve(MP1,VME);
//waitkey();
SolveV2M(MR,VME);
//MPrintPNG(MR);
MPrint(MR);
//waitkey();
writeln('!');
end;
end.
