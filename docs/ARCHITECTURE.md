# ProofSpec Architecture

## Thesis

ProofSpec turns agreed specifications into consensus-verifiable obligations.

## Evaluation model

Specification
    ↓
Obligations
    ↓
Deterministic checks
    ↓
Evidence evaluation
    ↓
GenLayer consensus
    ↓
Structured decision
    ↓
Finalized on-chain state

## Obligation model

Each obligation may define:

- id
- description
- mandatory
- weight
- depends_on
- evidence requirements

Mandatory obligations can block PASS even if the weighted score is otherwise high.

## Verdicts

### PASS
All mandatory obligations are satisfied and the required score is reached.

### PARTIAL
Evidence proves meaningful completion, but one or more non-critical requirements remain incomplete.

### FAIL
Verifiable evidence shows that mandatory requirements were not satisfied.

### UNVERIFIABLE
Available evidence is insufficient, unavailable, inaccessible, or contradictory enough that a reliable decision cannot be made.

Important:

> Absence of verifiable evidence is not proof of failure.
