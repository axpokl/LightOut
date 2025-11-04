program rcalc4;
const
  m = 10000;
type
  TBits    = array of QWord;
  TBoolDyn = array of Boolean;
var
  f, g: array[-2..0, -1..m] of boolean;
  inited: boolean = false;
  curN: longint = 0;

procedure ensure_row(n: longint);
var ni,k: longint;
begin
  if not inited then
  begin
    FillChar(f, SizeOf(f), 0);
    FillChar(g, SizeOf(g), 0);
    f[0,0]:=true; g[0,0]:=true;
    inited:=true; curN:=0;
  end;
  if n<=curN then exit;
  for ni:=curN+1 to n do
  begin
    f[-2]:=f[-1]; f[-1]:=f[0];
    g[-2]:=g[-1]; g[-1]:=g[0];
    for k:=0 to ni do
    begin
      f[0,k]:=f[-1,k-1] xor f[-2,k];
      g[0,k]:=g[-1,k-1] xor g[-1,k] xor g[-2,k];
    end;
  end;
  curN:=n;
end;

procedure pack_bool_to_bits_dyn(const src: TBoolDyn; n: longint; var bits: TBits);
var words,i: longint;
begin
  words := (n+64) shr 6;
  SetLength(bits, words);
  for i:=0 to words-1 do bits[i]:=0;
  for i:=0 to n do
    if src[i] then bits[i shr 6] := bits[i shr 6] or (QWord(1) shl (i and 63));
end;

function deg_bits(const a: TBits): longint;
var i,b: longint; w: QWord;
begin
  for i:=High(a) downto 0 do
    if a[i]<>0 then
    begin
      w:=a[i];
      for b:=63 downto 0 do
        if (w and (QWord(1) shl b))<>0 then
        begin deg_bits := (i shl 6) + b; exit; end;
    end;
  deg_bits := -1;
end;

procedure xor_shift_bits(var A: TBits; const B: TBits; sh: longint);
var ws,bs,j,si: longint; lo,hi: QWord;
begin
  if sh<0 then exit;
  ws := sh shr 6; bs := sh and 63;
  for j:=High(A) downto 0 do
  begin
    lo := 0; hi := 0;
    si := j - ws;
    if (si>=0) and (si<=High(B)) then lo := B[si] shl bs;
    if (bs<>0) and (si-1>=0) and (si-1<=High(B)) then hi := B[si-1] shr (64-bs);
    A[j] := A[j] xor (lo or hi);
  end;
end;

function gcd_deg_bits(var A,B: TBits): longint;
var da,db,sh: longint; tmp: TBits;
begin
  while true do
  begin
    da := deg_bits(A);
    if da<0 then begin gcd_deg_bits:=deg_bits(B); exit; end;
    db := deg_bits(B);
    if db<0 then begin gcd_deg_bits:=da; exit; end;
    if da<db then begin tmp:=A; A:=B; B:=tmp; da:=db; db:=deg_bits(B); end;
    sh := da - db;
    xor_shift_bits(A, B, sh);
  end;
end;

function rank3(n: longint): longint;
var A,B: TBits; fa,ga: array[-1..m] of boolean; ad,bd: TBoolDyn; i: longint;
begin
  ensure_row(n);
  fa:=f[0]; ga:=g[0];
  SetLength(ad, n+1); SetLength(bd, n+1);
  for i:=0 to n do begin ad[i]:=fa[i]; bd[i]:=ga[i]; end;
  pack_bool_to_bits_dyn(ad, n, A);
  pack_bool_to_bits_dyn(bd, n, B);
  rank3 := gcd_deg_bits(A,B);
end;

function rank(n: longint): longint;
var fn,gn,cn: array[-1..m] of boolean; kg,kf,kt,k: longint;
begin
  ensure_row(n);
  fn:=f[0]; gn:=g[0]; kg:=n; kf:=n;
  repeat
    kt:=-1;
    for k:=0 to kf do
    begin
      if k>=(kf-kg) then fn[k]:=fn[k] xor gn[k-(kf-kg)];
      if fn[k] then kt:=k;
    end;
    if kt=-1 then begin rank:=kg; exit; end;
    if kt<kg then begin cn:=fn; fn:=gn; gn:=cn; kf:=kg; kg:=kt; end else kf:=kt;
  until false;
end;

var i: longint;
begin
  for i:=1 to m do
    writeln(i,#9,rank3(i));  // 如需对比： writeln(i,#9,rank(i),#9,rank3(i));
end.
