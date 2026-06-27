import heapq
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    m = int(data[idx]); idx += 1

    gtmp  = [[] for _ in range(n + 1)]
    rgtmp = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        w = int(data[idx]); idx += 1
        gtmp[u].append((v, w))
        rgtmp[v].append((u, w))
    # tuple быстрее list при итерации (меньше накладных расходов FOR_ITER)
    graph  = [tuple(x) for x in gtmp]
    rgraph = [tuple(x) for x in rgtmp]
    del gtmp, rgtmp

    k = int(data[idx]); idx += 1

    INF   = 10 ** 18
    _push = heapq.heappush
    _pop  = heapq.heappop

    fdist = [INF] * (n + 1)
    bdist = [INF] * (n + 1)
    fmod  = []
    bmod  = []

    # default-аргументы → LOAD_FAST вместо LOAD_DEREF (~60 нс на каждое обращение)
    def bidir(s, t,
              fd=fdist, bd=bdist, fm=fmod, bm=bmod,
              g=graph,  rg=rgraph,
              push=_push, pop=_pop, INF=INF):

        for v in fm: fd[v] = INF
        for v in bm: bd[v] = INF
        fm.clear(); bm.clear()

        if s == t: return 0

        fd[s] = 0; fm.append(s)
        bd[t] = 0; bm.append(t)
        fh = [(0, s)]; bh = [(0, t)]
        mu = INF

        while fh and bh:
            # кешируем fh[0][0] и bh[0][0] — иначе каждый доступ = 2 BINARY_SUBSCR
            fmin = fh[0][0]; bmin = bh[0][0]
            if fmin + bmin >= mu: break

            if fmin <= bmin:
                dd, u = pop(fh)
                if fd[u] != dd: continue
                bdu = bd[u]                   # кешируем bd[u]
                if dd + bdu < mu: mu = dd + bdu
                for v, w in g[u]:
                    nd = dd + w
                    fv = fd[v]                # кешируем fd[v]
                    if nd < fv:
                        if fv == INF: fm.append(v)
                        fd[v] = nd
                        push(fh, (nd, v))
                        c = nd + bd[v]
                        if c < mu: mu = c
            else:
                dd, u = pop(bh)
                if bd[u] != dd: continue
                fdu = fd[u]                   # кешируем fd[u]
                if fdu + dd < mu: mu = fdu + dd
                for v, w in rg[u]:
                    nd = dd + w
                    bv = bd[v]                # кешируем bd[v]
                    if nd < bv:
                        if bv == INF: bm.append(v)
                        bd[v] = nd
                        push(bh, (nd, v))
                        c = fd[v] + nd
                        if c < mu: mu = c

        return -1 if mu == INF else mu

    out = []
    for _ in range(k):
        s = int(data[idx]); idx += 1
        t = int(data[idx]); idx += 1
        out.append(bidir(s, t))

    sys.stdout.buffer.write(('\n'.join(map(str, out)) + '\n').encode())

solve()
