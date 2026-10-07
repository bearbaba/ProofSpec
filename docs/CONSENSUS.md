# Consensus Design

ProofSpec does not require validators to produce identical prose.

Validators independently evaluate:

1. The agreed specification
2. Individual obligations
3. Submitted evidence
4. Mandatory failures
5. Overall verdict
6. Confidence and reason codes

Consensus should focus on decision-critical fields.

Example:

Leader:
PASS / score 92

Validator A:
PASS / score 89

Validator B:
PASS / score 94

These results may be considered equivalent when:

- verdict matches
- mandatory obligation results match
- score difference stays within tolerance
- independent evidence supports the decision

The goal is semantic equivalence, not text equality.
