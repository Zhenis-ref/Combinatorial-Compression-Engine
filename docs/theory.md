\# Law → Engine → Backends



\## Core Law (ΔN–ΔD)



dS/dt = α(ΔN,ΔD)·ΔN + β·ΔD + ε·ξ(t)



α(ΔN,ΔD) = A / \[(1 + exp(-k(ΔN - ΔNcrit)))·(ΔD^p + eps\_floor)]



\- ΔN: external gradient / mismatch (normalized \[0,1])

\- ΔD: internal duality / structural tension (normalized \[0,1])

\- ε·ξ(t): minimal fluctuation (anti-stagnation)

\- bifurcation: regime switch near critical conditions (high ΔN, low ΔD)



\## Engine outputs (universal controls)



Engine returns:

\- explore ∈ \[0,1]

\- exploit ∈ \[0,1]

\- mode: normal/bifurcation



Backends map these controls to:

\- search branching width

\- pruning aggressiveness

\- decoding beam width / temperature

etc.



