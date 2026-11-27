d=ValueError
e=sorted
X=any
W=enumerate
V=sum
Q=next
O=chr
N=ord
M=bytes
J=range
H=max
I=abs
R=[A for A in J(128)if A&136==0]
a=-33,-31,-18,-14,14,18,31,33
S=-17,-16,-15,-1,1,15,16,17
g=[(),(),a,(-17,-15,15,17),(-16,-1,1,16),S,S]
C=0,100,320,335,500,950,0
P=0,0,1,1,2,4,0
h=M([A if A in(1,9)else 0 for A in J(256)])
E=[15]*128
E[0]=13
E[4]=12
E[7]=14
E[112]=7
E[116]=3
E[119]=11
safe_sq=M(0 not in(A//8,A%15,A%16,A%17)for A in(min(A,256-A)for A in J(256)))
F,G=([[0]*128 for A in J(16)]for A in(0,1))
for T in(0,8):
	b=1 if not T else-1
	for K in R:
		U,A=K&7,K>>4
		if T:A=7-A
		L=I(2*U-7);B=L+I(2*A-7);i=0,7*A-2*L+18*(U in(3,4)and A in(2,3)),45-5*B+2*A,28-2*B+3*A,3*A+18*(A==6),12-B,-18*A-4*(7-L)+35*(A==0 and U in(2,6));j=0,3*A*A+5*A-L,35-4*B,28-2*B,18-2*B,16-B,55-6*B
		for D in J(1,7):c=T|D;F[c][K]=b*(C[D]+i[D]);G[c][K]=b*(C[D]+j[D])
def parse(t):A,B,C,D=map(N,t[:4]);return 16*B+A-881,16*D+C-881,'__nbrq'.index(t[4])if len(t)==5 else 0
def uci(m):return''.join(O(97+(A&7))+O(49+(A>>4))for A in m[:2])+('__nbrq'[m[2]]if m[2]else'')
class Position:
	def __init__(A,fen):
		J,B,K,H,*I=fen.split();A.b=bytearray(128);A.s=8*(B!='w');A.c=V((B in K)<<A for A,B in W('KQkq'));A.ep=128 if H=='-'else parse(H*2)[0];A.h=int((I or[0])[0]);A.k=[-1]*2;A.pc={};A.mg=A.eg=A.ph=0
		C=112
		for ch in J:
			if ch=='/':C=(C&112)-16
			elif ch.isdigit():C+=int(ch)
			else:
				D=' PNBRQK  pnbrqk'.index(ch)
				A.b[C]=D
				A.mg+=F[D][C]
				A.eg+=G[D][C]
				A.ph+=P[D&7]
				if D&7==6:A.k[D>>3]=C
				C+=1
	def evaluate(A):
		B=min(24,A.ph)
		D=A.b
		C=(A.mg*B+A.eg*(24-B))//24
		C+=30*((D.count(3)>1)-(D.count(11)>1))
		if B:
			for(E,G)in W((16,-16)):
				f=A.k[E]+G
				if not f&136:C+=(1-2*E)*(3*B*D.count(1|E<<3,H(f-1,0),f+2)//4)
		C+=A.pawn_score(B)
		return C*(1 if A.s==0 else-1)+12
	def pawn_score(B,phase):
		C=M(B.b).translate(h),phase
		if C in B.pc:return B.pc[C]
		D=[[0]*9,[0]*9]
		for A,N in W((1,9)):
			K=-1
			while(K:=B.b.find(N,K+1))>=0:D[A][K&7]|=1<<((K>>4)^7*A)
		O=0
		for A,T in W(D):
			U=D[A^1];G=0
			for j,F in W(T[:8]):
				if not F:continue
				G-=12*(F.bit_count()*(1+int(not(T[j-1]or T[j+1])))-1)
				K=128|U[j-1]|U[j]|U[j+1]
				for S in J(8-(K&-K).bit_length(),8):
					if F>>S&1:G+=S*S*5*(32-phase)//24
			O+=(1-2*A)*G
		B.pc[C]=O
		return O
	def play(A,m,safe=False):
		C,D,Q=m
		B=A.b;O=A.s
		K=B[C]&7;M=B[D]
		edits=[(C,0),(D,Q|O if Q else B[C])]
		if K==1 and D==A.ep and M==0:
			D2=A.ep+4*O-16
			M=B[D2]
			edits.append((D2,0))
		if K==6 and abs(C-D)==2:
			R=(C&112)+7*(D>C)
			edits+=((R,0),((C+D)//2,B[R]))
		changes=[]
		R=[A.c,A.ep,A.h,A.mg,A.eg,A.ph,A.k[O>>3],changes]
		for i,p in edits:
			x=B[i]
			changes.append((i,x))
			B[i]=p
			A.mg+=F[p][i]-F[x][i]
			A.eg+=G[p][i]-G[x][i]
			A.ph+=P[p&7]-P[x&7]
		if K==6:
			A.k[O>>3]=D
		A.c&=E[C]&E[D];A.ep=(C+D)//2 if K==1 and I(D-C)==32 else 128;A.h=0 if K==1 or M else A.h+1;A.s^=8
		if not safe and A.attacked(A.k[O>>3],A.s):A.undo(R);return
		return R
	def undo(self,u):
		self.c,self.ep,self.h,self.mg,self.eg,self.ph,ks,changes=u
		self.s^=8
		self.k[self.s>>3]=ks
		for sq,old in changes:
			self.b[sq]=old
	def key(A):
		C=128;B=A.ep
		if B!=C:
			E=B-16+4*A.s
			for D in(E-1,E+1):
				if not D&136 and A.b[D]==A.s|1:
					F=A.play((D,B,0))
					if F is not None:A.undo(F);C=B;break
		return M(A.b)+M((A.s,A.c,C))
	def castles(A,a):
		C,B=A.s,A.b;G,H=(0,1)if C==0 else(112,4);D=C^8
		if a==G+4 and not A.attacked(a,D):
			for(E,J,K)in((1,7,H),(-1,0,H*2)):
				I,F=a+E,a+2*E
				if A.c&K and B[G+J]==C|4 and not B[I]and not B[F]and(E==1 or not B[a-3])and not A.attacked(I,D)and not A.attacked(F,D):yield(a,F,0)
	def attacked(G,q,s):
		B=G.b;E=q-16+4*s
		for A in(E-1,E+1):
			if not A&136 and B[A]==s|1:return True
		for D in a:
			A=q+D
			if not A&136 and B[A]==s|2:return True
		for D in S:
			A=q+D
			while not A&136 and not(W:=B[A]):A+=D
			if not A&136:
				W^=s
				if W in(5,3 if D&1 and I(D)!=1 else 4)or W==6 and A==q+D:return True
		return False
	def pawn_moves(C,a,captures=False):
		D,E=C.b,C.s;F=16 if E==0 else-16;A=a+F
		if not A&136 and not D[A]:
			if A>>4 in(0,7):
				for G in(5,2,4,3):yield(a,A,G)
			elif not captures:
				yield(a,A,0)
				if a>>4==(1 if E==0 else 6)and not D[A+F]:yield(a,A+F,0)
		for B in(A-1,A+1):
			if B&136:continue
			H=D[B]
			if H and H&8!=E or B==C.ep:
				for G in(5,2,4,3)if B>>4 in(0,7)else(0,):yield(a,B,G)
	def moves(B,captures=False):
		F=captures;H,I=B.b,B.s
		for A in R:
			C=H[A]^I
			if not 0<C<8:continue
			if C==1:yield from B.pawn_moves(A,F);continue
			for J in g[C]:
				D=A+J
				while not D&136:
					E=H[D]
					if 0<E^I<8:break
					if E or not F:yield(A,D,0)
					if E or C&3==2:break
					D+=J
			if C==6 and not F:yield from B.castles(A)
	def legal(self,check=None):
		king=self.k[self.s>>3]
		in_check=self.attacked(king,self.s^8) if check is None else check
		for m in self.moves():
			if not in_check and safe_sq[m[0]-king] and m[1]!=self.ep:
				yield m
			else:
				u=self.play(m)
				if u is not None:
					self.undo(u)
					yield m
from collections import Counter as k
class Halt(Exception):0
class Search:
	def __init__(A,p,limit,history):A.p=p;A.limit=limit;A.nodes=0;A.tt={};A.path=k(history);A.killers={};A.hist={}
	def run(s,d,a,b,y=1,n=True):
		s.nodes+=1
		if s.nodes>=s.limit:raise Halt
		p=s.p;o=p.k[p.s>>3];h=p.h
		if h>=100:return y-30000 if p.attacked(o,p.s^8)and Q(p.legal(True),None)is None else 0
		k=p.key();r=s.path[k]
		if r>=2:return 0
		if y>=72:return p.evaluate()
		k_tt=k+M((h,))if h>=28 else k
		l=a;t=s.tt.get(k_tt);f=None;v=-31000
		if t:
			i,x,j,f=t;x-=y*((x>29000)-(x<-29000))
			if not r and i>=H(0,d)and(not j or j==1 and x>=b or j==2 and x<=a):return x
		c=p.attacked(o,p.s^8);q=d<=0 and not c
		w=p.b
		if not c and(q or b<29000):
			x=p.evaluate()
			if x>=b:
				if Q(p.legal(c),None)is None:return 0
				if q or d<=2 and x>=b+110*d:return x
				if n and d>=3 and X(w.count(p.s|i)for i in(2,3,4,5)):
					z=p.ep;p.ep=128;p.s^=8
					try:x=-s.run(d-3-(d>6),-b,1-b,y+1,False)
					finally:p.s^=8;p.ep=z
					if x>=b:return x
			if q:v=x;a=H(a,x)
		h=s.killers.get(y,())
		def order(m):
			if m==f:return 10000000
			i,j,z=m
			t=w[i]&7;x=w[j]&7
			if t==1 and j==p.ep:x=1
			if x or z:return 100000+10*C[x]-C[t]+C[z]
			return 80000 if m in h else s.hist.get((p.s,m),0)
		s.path[k]=r+1
		i=0
		g=None
		try:
			for m in e(p.moves(q),key=order,reverse=True):
				j,z,t=m
				cap=w[z] or w[j]&7==1 and z==p.ep
				u=p.play(m,not c and safe_sq[j-o] and z!=p.ep)
				if u is None:continue
				i+=1
				try:
					if i==1:x=-s.run(d-1,-b,-a,y+1)
					else:
						red=d>=3 and i>4 and not c and not cap and not t and not p.attacked(p.k[p.s>>3],p.s^8)
						x=-s.run(d-1-red,-a-1,-a,y+1)
						if red and x>a:x=-s.run(d-1,-a-1,-a,y+1)
						if a<x<b:x=-s.run(d-1,-b,-a,y+1)
				finally:p.undo(u)
				if x>v:v,g=x,m
				a=H(a,x)
				if a>=b:
					if not cap and not t and d>0:
						s.killers[y]=(m,)+(h[:1] if m not in h else ())
						j=p.s,m
						s.hist[j]=s.hist.get(j,0)+d*d
					break
		finally:
			if r:s.path[k]=r
			else:del s.path[k]
		if not i:
			if not q:return y-30000 if c else 0
			if Q(p.legal(c),None) is None:return 0
		if not r:
			s.tt[k_tt]=H(0,d),v+y*((v>29000)-(v<-29000)),2 if v<=l else 1 if v>=b else 0,g
		return v
f='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
Z=75000
def choose(fen,legal,history=(),nodes=Z):
	B=Position(fen);E=[]
	if history:
		F=Position(f)
		for N in history:
			E.append(F.key())
			if F.play(parse(N))is None:raise d
	G=Search(B,nodes,E);G.path[B.key()]+=1;A=[parse(A)for A in e(legal)]
	if not A:return''
	I=A[0]
	try:
		for O in J(64):
			C=-31000;D=[]
			for K in A:
				L=B.play(K)
				if L is None:continue
				try:M=-G.run(O,-31000,-C)
				finally:B.undo(L)
				D.append((M,K));C=H(C,M)
			if not D:raise d
			D.sort(key=lambda v:-v[0]);A=[A for(B,A)in D];I=A[0]
			if C>29000:break
	except Halt:0
	return uci(I)
import json as Y,os,urllib.request
def main():
	C=os.environ['MAKEFUN_ENV_URL']
	P={}
	while True:
		route='/move' if P else '/game'
		R=urllib.request.urlopen(urllib.request.Request(C+route,Y.dumps(P).encode(),{'Content-Type':'application/json'})).read()
		R=Y.loads(R)
		P={}
		if R['status']=='done':
			return
		if R['status']=='your_move':
			D=125000 if R['opponent']in('nodes-1M','nodes-2M')else Z
			E=choose(R['fen'],R['legal_moves'],R['moves'],nodes=D)
			P={'game':R['game'],'move':E}
if __name__=='__main__':main()
