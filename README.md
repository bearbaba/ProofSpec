# ProofSpec

**Consensus-verifiable obligations for real-world deliverables.**

ProofSpec is a reusable GenLayer Intelligent Contract primitive for determining whether an agreed specification has been satisfied by verifiable evidence.

## Core idea

A contract should not ask AI whether something is "good."

It should ask whether an explicit specification has been satisfied by verifiable evidence.

ProofSpec follows four principles:

1. **Spec-first, not prompt-first**
2. **Evidence over opinion**
3. **Unverifiable is not failure**
4. **Semantic equivalence, not identical prose**

## Intended outcomes

- PASS
- PARTIAL
- FAIL
- UNVERIFIABLE

## Use cases

- AI agent agreements
- Freelance deliverables
- DAO grant milestones
- Hackathon bounties
- Service-level agreements
- Bug bounty verification

## Status

Early development.

## Live GenLayer Deployment

ProofSpec V2 is deployed and running on GenLayer Studio.

**Contract:** `0x1423CaEFCB857942C3b0cD63D2CA745D2cB93AEc`

**Studio:** https://studio.genlayer.com/?import-contract=0x1423CaEFCB857942C3b0cD63D2CA745D2cB93AEc

## Live Evaluation Evidence

### Case #1 — PASS

- Status: FINALIZED
- Verdict: PASS
- Score: 100
- Reason: SPEC_SATISFIED

The submitted webpage was successfully fetched and verified as publicly reachable with visible content.

### Case #2 — UNVERIFIABLE is not FAIL

- Status: FINALIZED
- Verdict: UNVERIFIABLE
- Score: 0
- Mandatory failed: 0
- Mandatory unverifiable: 1
- Reason: MANDATORY_EVIDENCE_UNVERIFIABLE

The evidence could not be fetched. ProofSpec correctly treated missing evidence as unverifiable rather than failed.

### Case #3 — Dependency blocking

The website itself was verifiable, but its prerequisite manifest was unavailable.

- Status: FINALIZED
- Verdict: UNVERIFIABLE
- Score: 0
- Mandatory failed: 0
- Mandatory unverifiable: 1
- Reason: MANDATORY_EVIDENCE_UNVERIFIABLE

This demonstrates deterministic dependency blocking: a downstream obligation cannot receive credit when its prerequisite is not satisfied.

## Design Boundary

Validators handle evidence interpretation and obligation classification.

The contract deterministically derives dependency blocking, weighted score, mandatory gates, and final verdict.
