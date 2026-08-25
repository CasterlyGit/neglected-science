from __future__ import annotations

FUNCTIONS = {
    "F1": "Planning and task decomposition",
    "F2": "Role specialization and coordination",
    "F3": "Tool selection and execution",
    "F4": "Workflow-state and trace capture",
    "F5": "Self-evaluation and repair",
    "F6": "Verification and escalation",
}

EVIDENCE = {
    "E1": "Scientific literature",
    "E2": "Structured biological knowledge",
    "E3": "Biological data",
    "E4": "Software and statistical outputs",
    "E5": "Scientific-model outputs",
    "E6": "Experimental or clinical observations",
}

STAGES = {
    "V0": "Illustrative output",
    "V1": "Demonstrated execution",
    "V2": "Replayable computation",
    "V3": "Scientifically evaluated computation",
    "V4": "Prospective empirical evaluation",
}
STAGE_ORDER = {stage: index for index, stage in enumerate(STAGES)}

QUALIFIERS = {
    "B": "Benchmark or baseline",
    "H": "Human or expert checkpoint",
    "S": "Statistics or uncertainty",
    "R": "Robustness or failure analysis",
    "X": "External or independent evaluation",
    "P": "Prospective testing",
    "C": "Closed-loop refinement",
}

SUPPORT_RELATIONS = {
    "supports", "calculated_from", "observed_in", "derived_from",
    "contradicted_by", "qualified_by",
}

TEXT_EXTENSIONS = {
    ".txt", ".md", ".json", ".jsonl", ".csv", ".tsv", ".yaml", ".yml",
    ".py", ".r", ".js", ".ts", ".toml", ".ini", ".cfg", ".xml",
}

SECRET_PATTERNS = {
    "private-key": "-----BEGIN PRIVATE KEY-----",
    "aws-access-key": "AKIA",
    "github-token": "ghp_",
    "openai-key": "sk-",
}
