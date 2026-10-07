import sys
import pytest

pytestmark = pytest.mark.skipif(
    sys.platform.startswith("win"),
    reason="genlayer-test Direct Mode currently hits Windows temp-file locking (WinError 32)"
)

import json


VALID_OBLIGATIONS = json.dumps([
    {
        "id": "api",
        "description": "API must be publicly reachable",
        "mandatory": True,
        "weight": 60
    },
    {
        "id": "docs",
        "description": "Documentation must be available",
        "mandatory": False,
        "weight": 40
    }
])

VALID_EVIDENCE = json.dumps([
    "https://proofspec.test/api",
    "https://proofspec.test/docs"
])


def deploy(direct_vm, direct_deploy):
    direct_vm.check_pickling = True
    direct_vm.strict_mocks = True
    return direct_deploy("contracts/ProofSpec.py")


def test_create_case_runtime(
    direct_vm,
    direct_deploy,
    direct_alice,
):
    contract = deploy(direct_vm, direct_deploy)
    direct_vm.sender = direct_alice

    case_id = contract.create_case(
        "API Delivery",
        "Deliver a working public API according to the agreed specification.",
        VALID_OBLIGATIONS,
        VALID_EVIDENCE,
        80,
    )

    assert case_id == 1
    assert contract.get_case_count() == 1

    case = json.loads(contract.get_case(1))

    assert case["title"] == "API Delivery"
    assert case["status"] == "OPEN"
    assert case["required_score"] == 80
    assert case["score"] == 0
    assert case["verdict"] == ""


def test_case_ids_increment(
    direct_vm,
    direct_deploy,
    direct_alice,
):
    contract = deploy(direct_vm, direct_deploy)
    direct_vm.sender = direct_alice

    first = contract.create_case(
        "Delivery One",
        "Deliver the first agreed implementation according to requirements.",
        VALID_OBLIGATIONS,
        VALID_EVIDENCE,
        80,
    )

    second = contract.create_case(
        "Delivery Two",
        "Deliver the second agreed implementation according to requirements.",
        VALID_OBLIGATIONS,
        VALID_EVIDENCE,
        80,
    )

    assert first == 1
    assert second == 2
    assert contract.get_case_count() == 2


def test_consensus_pass_runtime(
    direct_vm,
    direct_deploy,
    direct_alice,
):
    contract = deploy(direct_vm, direct_deploy)
    direct_vm.sender = direct_alice

    case_id = contract.create_case(
        "API Delivery",
        "Deliver a working public API according to the agreed specification.",
        VALID_OBLIGATIONS,
        VALID_EVIDENCE,
        80,
    )

    direct_vm.mock_web(
        r"https://proofspec\.test/api",
        "API is online and responds correctly."
    )

    direct_vm.mock_web(
        r"https://proofspec\.test/docs",
        "Complete public API documentation."
    )

    direct_vm.mock_llm(
        r".*",
        json.dumps({
            "score": 100,
            "mandatory_failed": 0,
            "mandatory_unverifiable": 0,
            "summary": "All requirements are supported by evidence."
        })
    )

    verdict = contract.evaluate_case(case_id)

    assert verdict == "PASS"

    case = json.loads(contract.get_case(case_id))

    assert case["status"] == "FINALIZED"
    assert case["verdict"] == "PASS"
    assert case["score"] == 100
    assert case["reason_code"] == "SPEC_SATISFIED"


def test_unverifiable_is_not_failure_runtime(
    direct_vm,
    direct_deploy,
    direct_alice,
):
    contract = deploy(direct_vm, direct_deploy)
    direct_vm.sender = direct_alice

    case_id = contract.create_case(
        "API Delivery",
        "Deliver a working public API according to the agreed specification.",
        VALID_OBLIGATIONS,
        VALID_EVIDENCE,
        80,
    )

    direct_vm.mock_web(
        r"https://proofspec\.test/api",
        "Evidence could not establish whether the API satisfies the requirement."
    )

    direct_vm.mock_web(
        r"https://proofspec\.test/docs",
        "Documentation exists."
    )

    direct_vm.mock_llm(
        r".*",
        json.dumps({
            "score": 40,
            "mandatory_failed": 0,
            "mandatory_unverifiable": 1,
            "summary": "The mandatory API requirement cannot be reliably verified."
        })
    )

    verdict = contract.evaluate_case(case_id)

    assert verdict == "UNVERIFIABLE"

    case = json.loads(contract.get_case(case_id))

    assert case["verdict"] == "UNVERIFIABLE"
    assert case["mandatory_failed"] == 0
    assert case["mandatory_unverifiable"] == 1
    assert case["reason_code"] == "MANDATORY_EVIDENCE_UNVERIFIABLE"


def test_validator_accepts_semantically_equivalent_score(
    direct_vm,
    direct_deploy,
    direct_alice,
):
    contract = deploy(direct_vm, direct_deploy)
    direct_vm.sender = direct_alice

    case_id = contract.create_case(
        "API Delivery",
        "Deliver a working public API according to the agreed specification.",
        VALID_OBLIGATIONS,
        VALID_EVIDENCE,
        80,
    )

    direct_vm.mock_web(
        r"https://proofspec\.test/.*",
        "The submitted evidence supports the stated requirements."
    )

    direct_vm.mock_llm(
        r".*",
        json.dumps({
            "score": 92,
            "mandatory_failed": 0,
            "mandatory_unverifiable": 0,
            "summary": "Evidence supports completion."
        })
    )

    assert contract.evaluate_case(case_id) == "PASS"

    direct_vm.clear_mocks()

    direct_vm.mock_web(
        r"https://proofspec\.test/.*",
        "The submitted evidence supports the stated requirements."
    )

    direct_vm.mock_llm(
        r".*",
        json.dumps({
            "score": 89,
            "mandatory_failed": 0,
            "mandatory_unverifiable": 0,
            "summary": "Requirements independently verified."
        })
    )

    # Same verdict, same mandatory gates, score delta <= 5.
    assert direct_vm.run_validator() is True


def test_validator_rejects_different_semantic_verdict(
    direct_vm,
    direct_deploy,
    direct_alice,
):
    contract = deploy(direct_vm, direct_deploy)
    direct_vm.sender = direct_alice

    case_id = contract.create_case(
        "API Delivery",
        "Deliver a working public API according to the agreed specification.",
        VALID_OBLIGATIONS,
        VALID_EVIDENCE,
        80,
    )

    direct_vm.mock_web(
        r"https://proofspec\.test/.*",
        "The submitted evidence supports the requirements."
    )

    direct_vm.mock_llm(
        r".*",
        json.dumps({
            "score": 90,
            "mandatory_failed": 0,
            "mandatory_unverifiable": 0,
            "summary": "Requirements satisfied."
        })
    )

    assert contract.evaluate_case(case_id) == "PASS"

    direct_vm.clear_mocks()

    direct_vm.mock_web(
        r"https://proofspec\.test/.*",
        "The validator sees contrary evidence."
    )

    direct_vm.mock_llm(
        r".*",
        json.dumps({
            "score": 30,
            "mandatory_failed": 1,
            "mandatory_unverifiable": 0,
            "summary": "A mandatory requirement is not satisfied."
        })
    )

    assert direct_vm.run_validator() is False
