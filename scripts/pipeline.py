#!/usr/bin/env python3
"""Deterministic, provenance-first pipeline for Milestones 3–5."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "corpus" / "config.json"
CACHE = ROOT / "corpus" / "cache"
SOURCES = ROOT / "corpus" / "sources.jsonl"
CLAIMS = ROOT / "claims" / "claims.jsonl"
LEDGER = ROOT / "corpus" / "retrieval-ledger.jsonl"
CANDIDATES = ROOT / "opportunities" / "candidates.jsonl"
DOSSIERS = ROOT / "opportunities" / "dossiers.jsonl"
RANKINGS = ROOT / "opportunities" / "rankings.json"
SATURATION = ROOT / "verification" / "saturation-audit.json"
NOVELTY_SEARCHES = ROOT / "verification" / "novelty-searches.jsonl"
DATASET_AUDITS = ROOT / "verification" / "dataset-audits.jsonl"
NOVELTY_CHALLENGES = ROOT / "verification" / "novelty-challenges.jsonl"
CANDIDATE_ADMISSIONS = ROOT / "verification" / "candidate-admissions.jsonl"
GAUNTLET_REPLAYS = ROOT / "verification" / "gauntlet-replays.jsonl"
CANDIDATE_PRIORITY = ROOT / "opportunities" / "candidate-priority-list.jsonl"
TARGET_REVIEWS = ROOT / "verification" / "target-reviews.jsonl"
CYCLE_RESULT = ROOT / "verification" / "cycle-result.json"

GAP_PATTERNS = re.compile(r"\b(remain(?:s|ed)? unknown|not (?:well )?understood|future (?:work|research)|knowledge gap|lack(?:s|ing)?|challenge|uncertain|unresolved|poorly understood)\b", re.I)
LIMIT_PATTERNS = re.compile(r"\b(limitation|however|despite|uncertaint|bias|confound|caveat|difficult|inconsistent)\b", re.I)
MECHANISM_PATTERNS = re.compile(r"\b(caus|driv|influenc|mechanism|lead(?:s|ing)? to|result(?:s|ing)? in|associated with|due to|effect of)\b", re.I)
NEGATIVE_PATTERNS = re.compile(r"\b(no |not |without |little |weak |decreas\w*|reduc\w*|loss|fail\w*|slower|lower)\b", re.I)
MIXED_PATTERNS = re.compile(r"\b(mixed|varied|inconsistent|context-dependent|trade-off|whereas)\b", re.I)

CONCEPT_TERMS = {
    "recovery-time": ["recovery", "relaxation", "return time", "cooling time", "cooling rate", "recover"],
    "memory-path-dependence": ["memory", "path dependence", "history dependence", "history-dependent"],
    "hysteresis": ["hysteresis", "lagged response", "irreversibility"],
    "resilience-stability": ["resilience", "stability", "resistant", "resistance"],
    "accumulated-stress": ["cumulative", "accumulated", "repeated", "cycle aging", "fatigue damage", "fatigue", "disturbance history"],
    "early-warning-slowing": ["critical slowing", "slower recovery", "early warning", "loss of resilience"],
    "temperature-state": ["surface temperature", "thermal", "temperature", "heat"],
    "degradation-state": ["degradation", "state of health", "capacity fade", "aging"],
}
CORE_DISCOVERY_CONCEPTS = {
    "recovery-time", "memory-path-dependence", "hysteresis",
    "resilience-stability", "accumulated-stress", "early-warning-slowing",
}
TRIO_SIZE = 3
MINIMUM_INTERVIEW_SURVIVORS = 2


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path):
    return json.loads(path.read_text())


def read_jsonl(path: Path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))


def reconstruct_abstract(index):
    if not index:
        return ""
    size = max(position for positions in index.values() for position in positions) + 1
    words = [""] * size
    for word, positions in index.items():
        for position in positions:
            words[position] = word
    return " ".join(words)


def normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def source_id_for(work):
    doi = (work.get("doi") or "").lower().replace("https://doi.org/", "")
    if doi:
        return "doi-" + re.sub(r"[^a-z0-9._-]+", "-", doi).strip("-")
    return "oa-" + work["id"].rsplit("/", 1)[-1].lower()


def infer_source_type(title: str) -> str:
    if re.search(r"\b(review|overview|synthesis|meta-analysis|perspective)\b", title, re.I):
        return "review"
    return "primary-study"


def relevance_score(title: str, abstract: str, keywords) -> float:
    title_l = title.lower()
    abstract_l = abstract.lower()
    score = sum(3 for keyword in keywords if keyword in title_l)
    score += sum(1 for keyword in keywords if keyword in abstract_l)
    return score


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "NeglectedScience/0.1 (local research pilot)"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def crossref_verify(doi: str, title: str):
    if not doi:
        return False, None
    encoded = urllib.parse.quote(doi.replace("https://doi.org/", ""), safe="")
    try:
        data = fetch_json(f"https://api.crossref.org/v1/works/{encoded}")["message"]
    except Exception:
        return False, None
    registered = " ".join(data.get("title") or [])
    match = SequenceMatcher(None, normalize_title(title), normalize_title(registered)).ratio() >= 0.88
    return True, match


def fetch_corpus():
    config = read_json(CONFIG)
    CACHE.mkdir(parents=True, exist_ok=True)
    selected = []
    ledger = []
    for domain, spec in config["domains"].items():
        pool = {}
        for query in spec["queries"]:
            params = {
                "search": query,
                "filter": f"from_publication_date:{config['from_year']}-01-01,type:article|review",
                "per-page": config["max_results_per_query"],
            }
            url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
            try:
                results = fetch_json(url).get("results", [])
                status, uncertainty = "success", None
            except Exception as exc:
                results = []
                status, uncertainty = "failed", type(exc).__name__
            added = 0
            for work in results:
                abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
                title = work.get("display_name") or ""
                if not title or not abstract or not work.get("doi"):
                    continue
                score = relevance_score(title, abstract, spec["keywords"])
                if score < 5:
                    continue
                sid = source_id_for(work)
                candidate = {
                    "work": work,
                    "abstract": abstract,
                    "score": score + math.log1p(work.get("cited_by_count") or 0),
                }
                if sid not in pool or candidate["score"] > pool[sid]["score"]:
                    pool[sid] = candidate
                    added += 1
            ledger.append({
                "retrieved_at": utc_now(), "provider": "OpenAlex", "query": query,
                "domain": domain, "result_count": len(results), "selected_count": added,
                "status": status, "uncertainty": uncertainty,
            })
            time.sleep(0.1)
        ranked = sorted(pool.values(), key=lambda item: item["score"], reverse=True)
        reviews = [item for item in ranked if infer_source_type(item["work"].get("display_name") or "") == "review"]
        primary = [item for item in ranked if item not in reviews]
        chosen = reviews[:3] + primary[: max(0, config["sources_per_domain"] - min(3, len(reviews)))]
        if len(chosen) < config["sources_per_domain"]:
            used = {source_id_for(item["work"]) for item in chosen}
            chosen += [item for item in ranked if source_id_for(item["work"]) not in used][: config["sources_per_domain"] - len(chosen)]
        for item in chosen[: config["sources_per_domain"]]:
            work, abstract = item["work"], item["abstract"]
            sid = source_id_for(work)
            doi = (work.get("doi") or "").replace("https://doi.org/", "") or None
            verified, title_match = crossref_verify(doi, work.get("display_name") or "")
            cache_path = CACHE / f"{sid}.json"
            cache_path.write_text(json.dumps({"abstract": abstract, "openalex_id": work.get("id"), "retrieved_at": utc_now()}))
            authors = [entry.get("author", {}).get("display_name") for entry in (work.get("authorships") or [])[:8]]
            selected.append({
                "source_id": sid, "domain": domain, "title": work.get("display_name"),
                "year": work.get("publication_year"), "source_type": infer_source_type(work.get("display_name") or ""),
                "doi": doi, "openalex_id": work.get("id"), "url": work.get("doi") or work.get("id"),
                "publisher": ((work.get("primary_location") or {}).get("source") or {}).get("display_name"),
                "authors": [a for a in authors if a], "cited_by_count": work.get("cited_by_count") or 0,
                "abstract_available": True, "abstract_sha256": hashlib.sha256(abstract.encode()).hexdigest(),
                "crossref_verified": verified, "title_match": title_match, "retrieved_at": utc_now(),
                "provenance": "OpenAlex works search; DOI checked against Crossref when available",
                "review_status": "mechanically-screened",
                "uncertainties": ([] if title_match else ["Crossref title match unavailable or below threshold"]),
                "conventional_use": None, "measures": [],
            })
    for dataset in config["datasets"]:
        selected.append({
            **dataset, "year": None, "source_type": "dataset-documentation", "doi": None,
            "openalex_id": None, "authors": [], "cited_by_count": 0, "abstract_available": False,
            "abstract_sha256": None, "crossref_verified": False, "title_match": None,
            "retrieved_at": utc_now(), "provenance": "Curated official dataset landing page",
            "review_status": "human-reviewed", "uncertainties": ["Dataset suitability requires variable-level review"],
        })
        ledger.append({
            "retrieved_at": utc_now(), "provider": "curated-official", "query": dataset["url"],
            "domain": dataset["domain"], "result_count": 1, "selected_count": 1,
            "status": "success", "uncertainty": "Variable-level suitability not yet established",
        })
    selected.sort(key=lambda row: (row["domain"], row["source_type"], -(row["year"] or 0), row["title"]))
    write_jsonl(SOURCES, selected)
    write_jsonl(LEDGER, ledger)
    print(json.dumps({"sources": len(selected), "papers": sum(s["source_type"] != "dataset-documentation" for s in selected), "datasets": sum(s["source_type"] == "dataset-documentation" for s in selected)}, indent=2))


def sentence_split(text: str):
    return [part.strip() for part in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if len(part.split()) >= 6]


def concepts_for(text: str):
    lower = text.lower()
    return sorted({concept for concept, terms in CONCEPT_TERMS.items() if any(term in lower for term in terms)})


def classify_sentence(text: str):
    if GAP_PATTERNS.search(text):
        return "explicit-gap"
    if LIMIT_PATTERNS.search(text):
        return "limitation"
    if MECHANISM_PATTERNS.search(text):
        return "reported-mechanism"
    if re.search(r"\b(recover|recovery|relaxation|resilien|cooling|hysteresis|memory)\b", text, re.I):
        return "recovery-observation"
    return "reported-association"


def polarity_for(text: str):
    if MIXED_PATTERNS.search(text):
        return "mixed"
    if NEGATIVE_PATTERNS.search(text):
        return "negative"
    if re.search(r"\b(associated|increas\w*|improv\w*|enhanc\w*|faster|higher|positive)\b", text, re.I):
        return "positive"
    return "uncertain"


def bounded_excerpt(sentence: str):
    words = sentence.split()
    return " ".join(words[:22]) + (" …" if len(words) > 22 else "")


def extract_claims():
    rows = []
    for source in read_jsonl(SOURCES):
        if source["source_type"] == "dataset-documentation":
            evidence = source["conventional_use"]
            rows.append({
                "claim_id": source["source_id"] + "-use", "source_id": source["source_id"],
                "domain": source["domain"], "location": "official dataset landing page: documented purpose",
                "claim_kind": "dataset-use", "concepts": ["dataset-conventional-use"],
                "evidence_excerpt": bounded_excerpt(evidence), "evidence_sha256": hashlib.sha256(evidence.encode()).hexdigest(),
                "polarity": "not-applicable", "extraction_method": "curated-dataset-record-v1",
                "review_status": "human-reviewed", "uncertainty": "medium",
            })
            continue
        title_concepts = concepts_for(source["title"])
        title_polarity = polarity_for(source["title"])
        if title_concepts and (title_polarity != "uncertain" or "memory-path-dependence" in title_concepts):
            rows.append({
                "claim_id": f"{source['source_id']}-title", "source_id": source["source_id"],
                "domain": source["domain"], "location": "title",
                "claim_kind": "reported-association", "concepts": title_concepts,
                "evidence_excerpt": bounded_excerpt(source["title"]),
                "evidence_sha256": hashlib.sha256(source["title"].encode()).hexdigest(),
                "polarity": title_polarity, "extraction_method": "deterministic-abstract-v1",
                "review_status": "pending", "uncertainty": "high",
            })
        cache = read_json(CACHE / f"{source['source_id']}.json")
        sentences = sentence_split(cache["abstract"])
        scored = []
        for index, sentence in enumerate(sentences, 1):
            concepts = concepts_for(sentence)
            score = len(concepts) * 2 + bool(GAP_PATTERNS.search(sentence)) * 3 + bool(LIMIT_PATTERNS.search(sentence)) * 2 + bool(MECHANISM_PATTERNS.search(sentence))
            if set(concepts) & CORE_DISCOVERY_CONCEPTS and score >= 3:
                scored.append((score, index, sentence, concepts))
        for _, index, sentence, concepts in sorted(scored, reverse=True)[:4]:
            rows.append({
                "claim_id": f"{source['source_id']}-a{index}", "source_id": source["source_id"],
                "domain": source["domain"], "location": f"abstract sentence {index}",
                "claim_kind": classify_sentence(sentence), "concepts": concepts,
                "evidence_excerpt": bounded_excerpt(sentence), "evidence_sha256": hashlib.sha256(sentence.encode()).hexdigest(),
                "polarity": polarity_for(sentence), "extraction_method": "deterministic-abstract-v1",
                "review_status": "pending", "uncertainty": "high",
            })
    rows.sort(key=lambda row: (row["domain"], row["source_id"], row["location"]))
    overrides_path = ROOT / "verification" / "extraction-overrides.json"
    if overrides_path.exists():
        overrides = read_json(overrides_path)
        for row in rows:
            if row["claim_id"] in overrides:
                row.update(overrides[row["claim_id"]])
                row["review_status"] = "human-reviewed"
    write_jsonl(CLAIMS, rows)
    sample = [row for i, row in enumerate(rows) if row["extraction_method"] == "deterministic-abstract-v1" and i % 5 == 0]
    write_jsonl(ROOT / "verification" / "extraction-review-sample.jsonl", sample)
    print(json.dumps({"claims": len(rows), "review_sample": len(sample)}, indent=2))


def candidate_id(prefix: str, value: str):
    digest = hashlib.sha1(value.encode()).hexdigest()[:10]
    return f"{prefix}-{digest}"


def discover():
    claims = read_jsonl(CLAIMS)
    sources = {row["source_id"]: row for row in read_jsonl(SOURCES)}
    candidates = []
    for domain in sorted({row["domain"] for row in claims}):
        gaps = [row for row in claims if row["domain"] == domain and row["claim_kind"] in {"explicit-gap", "limitation"}]
        for row in gaps[:3]:
            question = f"Does the limitation reported for {domain.replace('_', ' ')} conceal a testable recovery or path-dependence question?"
            candidates.append({"candidate_id": candidate_id("explicit", row["claim_id"]), "gap_type": "explicit", "question": question, "domains": [domain], "claim_ids": [row["claim_id"]], "dataset_source_ids": [], "mechanical_status": "needs-scientific-review", "risk_flags": ["explicit gaps may be stale or rhetorical"]})
    by_domain_concept = defaultdict(list)
    for row in claims:
        for concept in row["concepts"]:
            by_domain_concept[(row["domain"], concept)].append(row)
    for (domain, concept), rows in by_domain_concept.items():
        # In the pilot corpus, title/abstract polarity is not reliable enough to
        # compare performance claims across battery or materials test regimes.
        # Keep the contradiction engine bounded to environmental domains where
        # the candidate question explicitly asks for measurement alignment.
        if domain not in {"earth_heat", "ecological_recovery"}:
            continue
        positive = [r for r in rows if r["polarity"] == "positive"]
        negative = [r for r in rows if r["polarity"] in {"negative", "mixed"}]
        if positive and negative:
            pair = [positive[0], negative[0]]
            question = f"Which measurement conditions explain the apparent tension in {concept} findings within {domain.replace('_', ' ')}?"
            candidates.append({"candidate_id": candidate_id("contradiction", domain + concept), "gap_type": "contradiction", "question": question, "domains": [domain], "claim_ids": [r["claim_id"] for r in pair], "dataset_source_ids": [], "mechanical_status": "apparent-tension-only", "risk_flags": ["polarity classifier does not establish a scientific contradiction"]})
    concept_domains = defaultdict(lambda: defaultdict(list))
    for row in claims:
        for concept in row["concepts"]:
            concept_domains[concept][row["domain"]].append(row)
    for concept, domains in concept_domains.items():
        if concept in {"temperature-state", "degradation-state", "dataset-conventional-use"} or len(domains) < 2:
            continue
        chosen_domains = sorted(domains)[:4]
        evidence = [domains[domain][0]["claim_id"] for domain in chosen_domains]
        question = f"Do {concept.replace('-', ' ')} measurements share a transferable dynamical structure across {' and '.join(d.replace('_', ' ') for d in chosen_domains)}?"
        candidates.append({"candidate_id": candidate_id("translation", concept + ":" + ",".join(chosen_domains)), "gap_type": "translation", "question": question, "domains": chosen_domains, "claim_ids": evidence, "dataset_source_ids": [], "mechanical_status": "structural-equivalence-unproven", "risk_flags": ["shared terminology may not imply shared mechanism"]})
    datasets = [source for source in sources.values() if source["source_type"] == "dataset-documentation"]
    for dataset in datasets:
        relevant = [row for row in claims if row["domain"] == dataset["domain"] and row["claim_kind"] != "dataset-use"]
        concepts = sorted({concept for row in relevant for concept in row["concepts"] if concept not in {"temperature-state", "degradation-state"}})
        if not concepts:
            continue
        concept = concepts[0]
        evidence = [row["claim_id"] for row in relevant if concept in row["concepts"]][:2]
        question = f"Can {dataset['title']} support a falsifiable analysis of {concept.replace('-', ' ')} beyond its conventional use?"
        candidates.append({"candidate_id": candidate_id("datause", dataset["source_id"] + concept), "gap_type": "data-use", "question": question, "domains": [dataset["domain"]], "claim_ids": evidence, "dataset_source_ids": [dataset["source_id"]], "mechanical_status": "variable-audit-required", "risk_flags": ["landing-page metadata does not prove variable adequacy"]})
    unique = {row["candidate_id"]: row for row in candidates}
    rows = sorted(unique.values(), key=lambda row: (row["gap_type"], row["candidate_id"]))
    write_jsonl(CANDIDATES, rows)
    counts = defaultdict(int)
    for row in rows:
        counts[row["gap_type"]] += 1
    print(json.dumps({"candidates": len(rows), "by_type": counts}, indent=2, default=dict))


SCORE_KEYS = ["importance", "unresolved_evidence", "data_adequacy", "testability", "falsification", "feasibility", "negative_result_value", "cross_domain_leverage", "impact"]
PROFILES = {
    "balanced": {key: 1.0 for key in SCORE_KEYS},
    "rigor_first": {**{key: 0.7 for key in SCORE_KEYS}, "unresolved_evidence": 1.5, "data_adequacy": 1.5, "testability": 1.5, "falsification": 1.7},
    "impact_first": {**{key: 0.8 for key in SCORE_KEYS}, "importance": 1.6, "impact": 1.6, "negative_result_value": 1.2},
}

SATURATION_QUERIES = {
    "earth_heat": ["urban thermal lag nighttime heat persistence", "surface urban heat island diurnal hysteresis recovery"],
    "ecological_recovery": ["ecosystem recovery debt disturbance legacy", "ecological hysteresis resilience recovery time"],
    "battery_memory": ["battery relaxation path dependent aging history", "battery degradation recovery memory hysteresis"],
    "materials_fatigue": ["cyclic material memory relaxation fatigue damage", "material hysteresis recovery accumulated loading"],
}


def saturation_audit():
    existing_concepts = {concept for row in read_jsonl(CLAIMS) for concept in row["concepts"]}
    output = {"retrieved_at": utc_now(), "existing_concepts": sorted(existing_concepts), "domains": {}}
    for domain, queries in SATURATION_QUERIES.items():
        passes = []
        for query in queries:
            params = {"search": query, "filter": "from_publication_date:2016-01-01,type:article|review", "per-page": 10}
            data = fetch_json("https://api.openalex.org/works?" + urllib.parse.urlencode(params))
            works = []
            mapped = set()
            for work in data.get("results", []):
                abstract = reconstruct_abstract(work.get("abstract_inverted_index"))
                concepts = concepts_for((work.get("display_name") or "") + " " + abstract)
                mapped.update(concepts)
                works.append({"title": work.get("display_name"), "year": work.get("publication_year"), "doi": work.get("doi"), "mapped_concepts": concepts})
            passes.append({"query": query, "result_count": len(works), "mapped_concepts": sorted(mapped), "new_taxonomy_concepts": sorted(mapped - existing_concepts), "works": works})
        output["domains"][domain] = passes
    SATURATION.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({domain: [entry["new_taxonomy_concepts"] for entry in passes] for domain, passes in output["domains"].items()}, indent=2))


def build_dossiers():
    candidates = read_jsonl(CANDIDATES)
    claims = {row["claim_id"]: row for row in read_jsonl(CLAIMS)}
    sources = {row["source_id"]: row for row in read_jsonl(SOURCES)}
    dossiers = []
    for candidate in candidates:
        evidence_claims = [claims[cid] for cid in candidate["claim_ids"] if cid in claims]
        source_ids = sorted({row["source_id"] for row in evidence_claims} | set(candidate["dataset_source_ids"]))
        domain_count = len(candidate["domains"])
        evidence_count = len(evidence_claims)
        has_dataset = bool(candidate["dataset_source_ids"])
        gap = candidate["gap_type"]
        scores = {
            "importance": 3 if "earth_heat" in candidate["domains"] or "ecological_recovery" in candidate["domains"] else 2,
            "unresolved_evidence": 2 if gap in {"explicit", "contradiction"} else 1,
            "data_adequacy": 3 if has_dataset else 2,
            "testability": 3 if has_dataset or gap == "contradiction" else 2,
            "falsification": 3 if gap in {"contradiction", "translation"} else 2,
            "feasibility": 3 if domain_count == 1 else 2,
            "negative_result_value": 3 if gap == "translation" else 2,
            "cross_domain_leverage": min(4, domain_count + (1 if gap == "translation" else 0)),
            "impact": 3 if "earth_heat" in candidate["domains"] or "ecological_recovery" in candidate["domains"] else 2,
        }
        if evidence_count < 2:
            scores["unresolved_evidence"] = min(scores["unresolved_evidence"], 1)
        dossier = {
            "id": candidate["candidate_id"], "question": candidate["question"], "gap_types": [gap],
            "importance": "Potential value is provisional and must be assessed against domain-specific consequences and existing work.",
            "known": f"The bounded corpus contains {evidence_count} mechanically linked claim records across {domain_count} domain(s).",
            "unresolved": "The relationship, contradiction, or data-use opportunity has not been established as unresolved; Milestone 6 must challenge it.",
            "public_evidence": [sources[sid]["url"] for sid in source_ids if sid in sources],
            "competing_hypotheses": [
                "The candidate reflects a reproducible relationship or transferable dynamical structure.",
                "The candidate disappears after aligning definitions, boundary conditions, sampling, and measurement error."
            ],
            "experiment": "Align definitions and variables, preregister discriminating predictions, reproduce a baseline, and test on held-out conditions.",
            "falsification": ["The proposed relationship fails within source domains.", "Aligned measurements support a simpler domain-specific explanation."],
            "confounders": ["Different temporal and spatial scales", "Measurement and sampling differences", "Unobserved state variables"],
            "evidence_against_novelty": ["Adjacent disciplines may already describe the same question using different terminology.", *candidate["risk_flags"]],
            "neglect_explanation": "Possible disciplinary separation or conventional dataset use; this is a hypothesis, not an established explanation.",
            "scores": scores,
            "uncertainties": ["Abstract-level extraction only", "No adversarial prior-art search yet", "No external specialist review"],
            "sources": [{"source_id": sid, "location": next((claim["location"] for claim in evidence_claims if claim["source_id"] == sid), "official dataset landing page")} for sid in source_ids],
            "status": "candidate"
        }
        overrides_path = ROOT / "opportunities" / "dossier-overrides.json"
        if overrides_path.exists():
            dossier.update(read_json(overrides_path).get(dossier["id"], {}))
        dossiers.append(dossier)
    minimum = [d for d in dossiers if d["scores"]["testability"] > 0 and d["scores"]["data_adequacy"] > 0 and d["scores"]["falsification"] > 0]
    preliminary = sorted(minimum, key=lambda d: sum(d["scores"].values()), reverse=True)[:20]
    write_jsonl(DOSSIERS, preliminary)
    ranking = {"profiles": {}, "rank_stability": {}}
    positions = defaultdict(list)
    for profile, weights in PROFILES.items():
        ranked = sorted(preliminary, key=lambda d: sum(d["scores"][key] * weights[key] for key in SCORE_KEYS), reverse=True)
        ranking["profiles"][profile] = [{"id": d["id"], "score": round(sum(d["scores"][key] * weights[key] for key in SCORE_KEYS), 2)} for d in ranked]
        for position, dossier in enumerate(ranked, 1):
            positions[dossier["id"]].append(position)
    ranking["rank_stability"] = {identifier: {"best": min(pos), "worst": max(pos), "spread": max(pos) - min(pos)} for identifier, pos in positions.items()}
    stable = sorted(preliminary, key=lambda d: (max(positions[d["id"]]), sum(positions[d["id"]])))[:3]
    ranking["mechanical_finalist_suggestions"] = [d["id"] for d in stable]
    ranking["scientific_review_finalists"] = [d["id"] for d in preliminary if d["status"] == "finalist"]
    RANKINGS.write_text(json.dumps(ranking, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"dossiers": len(preliminary), "mechanical_finalist_suggestions": ranking["mechanical_finalist_suggestions"], "scientific_review_finalists": ranking["scientific_review_finalists"]}, indent=2))


def validate_all():
    targets = [
        (SOURCES, ROOT / "schemas" / "source-record.schema.json"),
        (CLAIMS, ROOT / "schemas" / "claim-record.schema.json"),
        (LEDGER, ROOT / "schemas" / "retrieval-ledger.schema.json"),
        (ROOT / "terminology" / "concepts.jsonl", ROOT / "schemas" / "terminology-record.schema.json"),
        (DOSSIERS, ROOT / "schemas" / "opportunity-dossier.schema.json"),
        (NOVELTY_SEARCHES, ROOT / "schemas" / "novelty-search-record.schema.json"),
        (DATASET_AUDITS, ROOT / "schemas" / "dataset-audit.schema.json"),
        (NOVELTY_CHALLENGES, ROOT / "schemas" / "novelty-challenge.schema.json"),
        (CANDIDATE_ADMISSIONS, ROOT / "schemas" / "candidate-admission.schema.json"),
        (GAUNTLET_REPLAYS, ROOT / "schemas" / "gauntlet-replay.schema.json"),
        (CANDIDATE_PRIORITY, ROOT / "schemas" / "candidate-priority.schema.json"),
        (TARGET_REVIEWS, ROOT / "schemas" / "target-review.schema.json"),
        (ROOT / "corpus" / "structural-cases.jsonl", ROOT / "schemas" / "structural-case.schema.json"),
        (ROOT / "corpus" / "research-cells.jsonl", ROOT / "schemas" / "research-cell.schema.json"),
        (ROOT / "corpus" / "source-feasibility-intake.jsonl", ROOT / "schemas" / "source-feasibility.schema.json"),
    ]
    failures = []
    for data_path, schema_path in targets:
        schema = read_json(schema_path)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for number, row in enumerate(read_jsonl(data_path), 1):
            for error in validator.iter_errors(row):
                failures.append(f"{data_path.relative_to(ROOT)}:{number}: {error.message}")
    source_ids = {row["source_id"] for row in read_jsonl(SOURCES)}
    for number, claim in enumerate(read_jsonl(CLAIMS), 1):
        if claim["source_id"] not in source_ids:
            failures.append(f"claims/claims.jsonl:{number}: missing source {claim['source_id']}")
    dossier_rows = read_jsonl(DOSSIERS)
    dossier_ids = {row["id"] for row in dossier_rows}
    finalist_ids = {row["id"] for row in dossier_rows if row["status"] == "finalist"}
    search_rows = read_jsonl(NOVELTY_SEARCHES)
    search_by_id = {row["search_id"]: row for row in search_rows}
    audit_rows = read_jsonl(DATASET_AUDITS)
    audit_by_id = {row["audit_id"]: row for row in audit_rows}
    challenge_rows = read_jsonl(NOVELTY_CHALLENGES)
    evidence_record_ids = set(search_by_id) | set(audit_by_id) | {row["challenge_id"] for row in challenge_rows}
    admission_rows = read_jsonl(CANDIDATE_ADMISSIONS)
    admission_by_id = {row["admission_id"]: row for row in admission_rows}
    replay_rows = read_jsonl(GAUNTLET_REPLAYS)
    priority_rows = read_jsonl(CANDIDATE_PRIORITY)
    priority_by_id = {row["lead_id"]: row for row in priority_rows}
    target_rows = read_jsonl(TARGET_REVIEWS)
    target_by_id = {row["target_id"]: row for row in target_rows}
    cycle_result = read_json(CYCLE_RESULT)
    if len(search_by_id) != len(search_rows):
        failures.append("verification/novelty-searches.jsonl: duplicate search_id")
    if len(audit_by_id) != len(audit_rows):
        failures.append("verification/dataset-audits.jsonl: duplicate audit_id")
    if len({row["challenge_id"] for row in challenge_rows}) != len(challenge_rows):
        failures.append("verification/novelty-challenges.jsonl: duplicate challenge_id")
    if len(admission_by_id) != len(admission_rows):
        failures.append("verification/candidate-admissions.jsonl: duplicate admission_id")
    if len({row["replay_id"] for row in replay_rows}) != len(replay_rows):
        failures.append("verification/gauntlet-replays.jsonl: duplicate replay_id")
    if len(priority_by_id) != len(priority_rows):
        failures.append("opportunities/candidate-priority-list.jsonl: duplicate lead_id")
    if sorted(row["rank"] for row in priority_rows) != list(range(1, len(priority_rows) + 1)):
        failures.append("opportunities/candidate-priority-list.jsonl: ranks must be unique and contiguous")
    if len(target_by_id) != len(target_rows):
        failures.append("verification/target-reviews.jsonl: duplicate target_id")
    if {row["finalist_id"] for row in challenge_rows} != finalist_ids:
        failures.append("verification/novelty-challenges.jsonl: challenge coverage must equal finalist set")
    for finalist_id in finalist_ids:
        attacks = {row["attack_type"] for row in search_rows if row["finalist_id"] == finalist_id}
        if not {"citation-backward", "citation-forward"} <= attacks:
            failures.append(f"verification/novelty-searches.jsonl: incomplete citation trace for {finalist_id}")
        if not attacks & {"alternative-terminology", "adjacent-discipline"}:
            failures.append(f"verification/novelty-searches.jsonl: missing terminology expansion for {finalist_id}")
    for number, search in enumerate(search_rows, 1):
        if search["finalist_id"] not in dossier_ids:
            failures.append(f"verification/novelty-searches.jsonl:{number}: missing finalist {search['finalist_id']}")
    for number, audit in enumerate(audit_rows, 1):
        for finalist_id in audit["finalist_ids"]:
            if finalist_id not in dossier_ids:
                failures.append(f"verification/dataset-audits.jsonl:{number}: missing finalist {finalist_id}")
    for number, challenge in enumerate(challenge_rows, 1):
        finalist_id = challenge["finalist_id"]
        for search_id in challenge["search_ids"]:
            if search_id not in search_by_id:
                failures.append(f"verification/novelty-challenges.jsonl:{number}: missing search {search_id}")
            elif search_by_id[search_id]["finalist_id"] != finalist_id:
                failures.append(f"verification/novelty-challenges.jsonl:{number}: search {search_id} belongs to another finalist")
        for audit_id in challenge["dataset_audit_ids"]:
            if audit_id not in audit_by_id:
                failures.append(f"verification/novelty-challenges.jsonl:{number}: missing audit {audit_id}")
            elif finalist_id not in audit_by_id[audit_id]["finalist_ids"]:
                failures.append(f"verification/novelty-challenges.jsonl:{number}: audit {audit_id} does not cover finalist")
    for number, admission in enumerate(admission_rows, 1):
        if admission["source_candidate_id"] not in dossier_ids:
            failures.append(f"verification/candidate-admissions.jsonl:{number}: missing source candidate {admission['source_candidate_id']}")
        checks_pass = all(check["status"] == "pass" for check in admission["construction_checks"].values())
        if (admission["emission_verdict"] == "interview-ready") != checks_pass:
            failures.append(f"verification/candidate-admissions.jsonl:{number}: interview-ready requires every construction check to pass")
        for check in admission["construction_checks"].values():
            missing_refs = set(check["evidence_refs"]) - evidence_record_ids
            if missing_refs:
                failures.append(f"verification/candidate-admissions.jsonl:{number}: missing evidence records {sorted(missing_refs)}")
    for number, replay in enumerate(replay_rows, 1):
        missing = set(replay["admission_ids"]) - set(admission_by_id)
        if missing:
            failures.append(f"verification/gauntlet-replays.jsonl:{number}: missing admissions {sorted(missing)}")
            continue
        ready = [identifier for identifier in replay["admission_ids"] if admission_by_id[identifier]["emission_verdict"] == "interview-ready"]
        if replay["interview_ready_ids"] != ready:
            failures.append(f"verification/gauntlet-replays.jsonl:{number}: interview_ready_ids do not match admission verdicts")
        trio_created = len(ready) == 3
        if replay["trio_created"] != trio_created:
            failures.append(f"verification/gauntlet-replays.jsonl:{number}: trio_created requires exactly three interview-ready targets")
        if not trio_created and (replay["broad_pipeline_authorized"] or replay["would_reach_confirmation_milestone_6"]):
            failures.append(f"verification/gauntlet-replays.jsonl:{number}: failed construction batch cannot advance")
    selected_leads = {row["lead_id"] for row in priority_rows if row["selection_status"] == "selected"}
    if len(selected_leads) != TRIO_SIZE:
        failures.append("opportunities/candidate-priority-list.jsonl: exactly three leads must be selected")
    if {row["lead_id"] for row in target_rows} != selected_leads:
        failures.append("verification/target-reviews.jsonl: reviews must cover exactly the selected leads")
    if len(target_rows) != TRIO_SIZE:
        failures.append("verification/target-reviews.jsonl: exactly three targets are required")
    for number, target in enumerate(target_rows, 1):
        if not all(check["status"] == "pass" for check in target["construction_checks"].values()):
            failures.append(f"verification/target-reviews.jsonl:{number}: selected target failed a construction check")
        if target["first_interview"]["verdict"] != "admitted":
            failures.append(f"verification/target-reviews.jsonl:{number}: selected trio must record an admitted first-interview verdict")
    cycle_schema = read_json(ROOT / "schemas" / "cycle-result.schema.json")
    cycle_validator = Draft202012Validator(cycle_schema, format_checker=FormatChecker())
    for error in cycle_validator.iter_errors(cycle_result):
        failures.append(f"verification/cycle-result.json: {error.message}")
    cycle_target_ids = cycle_result.get("target_ids", [])
    if set(cycle_target_ids) != set(target_by_id):
        failures.append("verification/cycle-result.json: target_ids must match target reviews")
    admitted_ids = {row["target_id"] for row in target_rows if row["first_interview"]["verdict"] == "admitted"}
    if set(cycle_result.get("first_interview_survivors", [])) != admitted_ids:
        failures.append("verification/cycle-result.json: first-interview survivors must match target reviews")
    dispositions = {row["target_id"]: row["confirmation_challenge"]["disposition"] for row in target_rows}
    if cycle_result.get("confirmation_dispositions") != dispositions:
        failures.append("verification/cycle-result.json: confirmation dispositions must match target reviews")
    eligible = {identifier for identifier, disposition in dispositions.items() if disposition == "surviving"}
    if set(cycle_result.get("milestone_7_eligible_ids", [])) != eligible:
        failures.append("verification/cycle-result.json: eligible IDs must be confirmation survivors")
    if cycle_result.get("primary_id") not in eligible or cycle_result.get("reserve_id") not in eligible:
        failures.append("verification/cycle-result.json: primary and reserve must be confirmation survivors")
    if cycle_result.get("milestone_6_complete") != (len(dispositions) == TRIO_SIZE and bool(eligible)):
        failures.append("verification/cycle-result.json: Milestone 6 completion must require three dispositions and a survivor")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps({"validated_records": sum(len(read_jsonl(path)) for path, _ in targets), "referential_integrity": "pass"}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["fetch", "extract", "discover", "rank", "saturation", "validate", "all"])
    args = parser.parse_args()
    if args.command in {"fetch", "all"}:
        fetch_corpus()
    if args.command in {"extract", "all"}:
        extract_claims()
    if args.command in {"discover", "all"}:
        discover()
    if args.command in {"rank", "all"}:
        build_dossiers()
    if args.command in {"saturation", "all"}:
        saturation_audit()
    if args.command in {"validate", "all"}:
        validate_all()


if __name__ == "__main__":
    main()
