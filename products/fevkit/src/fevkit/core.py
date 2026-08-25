from __future__ import annotations

import hashlib, json, os, re, shutil, subprocess, tempfile
from dataclasses import asdict, dataclass
from datetime import datetime
from importlib.resources import files
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

FUNCTIONS={"F1":"Planning and task decomposition","F2":"Role specialization and coordination","F3":"Tool selection and execution","F4":"Workflow-state and trace capture","F5":"Self-evaluation and repair","F6":"Verification and escalation"}
EVIDENCE={"E1":"Scientific literature","E2":"Structured biological knowledge","E3":"Biological data","E4":"Software and statistical outputs","E5":"Scientific-model outputs","E6":"Experimental or clinical observations"}
STAGES={"V0":"Illustrative output","V1":"Demonstrated execution","V2":"Replayable computation","V3":"Scientifically evaluated computation","V4":"Prospective empirical evaluation"}
STAGE_RANK={x:i for i,x in enumerate(STAGES)}
HASH_RE=re.compile(r"^[0-9a-f]{64}$")
RELATIONS={"supports","calculated_from","observed_in","derived_from","contradicted_by","qualified_by"}
DEFAULT_EXECUTABLES={"python","python3","node","Rscript"}

@dataclass(frozen=True)
class Finding:
    code:str; severity:str; message:str; path:str="$"; remediation:str|None=None; dimension:str|None=None
    def as_dict(self): return {k:v for k,v in asdict(self).items() if v is not None}

@dataclass(frozen=True)
class AuditResult:
    status:str; run_id:str|None; profile:str; claimed_stage:str|None; computed_stage:str; computed_stage_name:str; qualifiers:tuple[str,...]; functions:dict[str,dict[str,Any]]; evidence:dict[str,dict[str,Any]]; findings:tuple[Finding,...]; integrity:dict[str,Any]; metrics:dict[str,Any]; manifest:str
    def as_dict(self):
        v=asdict(self); v["findings"]=[x.as_dict() for x in self.findings]; v["qualifiers"]=list(self.qualifiers); v["counts"]={"errors":sum(x.severity=="error" for x in self.findings),"warnings":sum(x.severity=="warning" for x in self.findings),"info":sum(x.severity=="info" for x in self.findings)}; return v

class FEVKitError(RuntimeError): pass

def _d(v): return v if isinstance(v,dict) else {}
def _l(v): return v if isinstance(v,list) else []
def _s(v): return isinstance(v,str) and bool(v.strip())
def _time(v):
    try: datetime.fromisoformat(str(v).replace("Z","+00:00")); return _s(v)
    except ValueError: return False
def _sha(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for c in iter(lambda:f.read(1024*1024),b""): h.update(c)
    return h.hexdigest()
def _safe(root,rel):
    if not _s(rel): return None
    p=Path(rel)
    if p.is_absolute() or ".." in p.parts:return None
    r=(root/p).resolve()
    try:r.relative_to(root.resolve());return r
    except ValueError:return None
def _add(fs,code,severity,message,path="$",remediation=None,dimension=None):fs.append(Finding(code,severity,message,path,remediation,dimension))
def _profiles():return json.loads(files("fevkit").joinpath("profiles.json").read_text())
def _declared(run):
    out=[]
    for c in ("inputs","artifacts"):
        for i,x in enumerate(_l(run.get(c))):out.append((f"$.run.{c}[{i}]",_d(x),c[:-1]))
    for i,x in enumerate(_l(_d(run.get("environment")).get("lockfiles"))):out.append((f"$.run.environment.lockfiles[{i}]",_d(x),"lockfile"))
    return out
def _states(vocab,counts,findings):
    return {i:{"id":i,"name":n,"count":counts.get(i,0),"present":counts.get(i,0)>0,"complete":counts.get(i,0)>0 and not any(x.severity=="error" and x.dimension==i for x in findings),"finding_codes":sorted({x.code for x in findings if x.severity=="error" and x.dimension==i})} for i,n in vocab.items()}

def audit_bundle(bundle,profile=None):
    source=Path(bundle).expanduser().resolve(); manifest=source/"run.json" if source.is_dir() else source; root=manifest.parent
    if not manifest.is_file():raise FEVKitError(f"run manifest not found: {manifest}")
    try:doc=json.loads(manifest.read_text())
    except (OSError,json.JSONDecodeError) as e:raise FEVKitError(str(e)) from e
    fs=[]; run=_d(doc.get("run"))
    if doc.get("spec_version")!="0.1":_add(fs,"STRUCTURE.SPEC_VERSION","error","spec_version must be '0.1'.","$.spec_version")
    for k in ("id","title","objective","domain","started_at","completed_at","status"):
        if not _s(run.get(k)):_add(fs,"STRUCTURE."+k.upper(),"error",f"run.{k} is required.",f"$.run.{k}")
    for k in ("started_at","completed_at"):
        if run.get(k) is not None and not _time(run.get(k)):_add(fs,"STRUCTURE."+k.upper()+"_FORMAT","error",f"run.{k} must be ISO-8601.",f"$.run.{k}")
    if _time(run.get("started_at")) and _time(run.get("completed_at")) and datetime.fromisoformat(run["completed_at"].replace("Z","+00:00"))<datetime.fromisoformat(run["started_at"].replace("Z","+00:00")):_add(fs,"STRUCTURE.TIME_ORDER","error","completed_at precedes started_at.","$.run.completed_at")
    system=_d(run.get("system"))
    if not _s(system.get("name")):_add(fs,"STRUCTURE.SYSTEM_NAME","error","system.name is required.","$.run.system.name")
    if not _s(system.get("version")):_add(fs,"STRUCTURE.SYSTEM_VERSION","error","system.version is required.","$.run.system.version")
    inputs,arts,steps,evs,claims,checks=map(_l,[run.get("inputs"),run.get("artifacts"),run.get("steps"),run.get("evidence"),run.get("claims"),run.get("human_checkpoints")])
    input_ids={_d(x).get("id") for x in inputs}; art_ids={_d(x).get("id") for x in arts}; step_ids={_d(x).get("id") for x in steps}; ev_ids={_d(x).get("id") for x in evs}
    fc={x:0 for x in FUNCTIONS}; ec={x:0 for x in EVIDENCE}
    for i,raw in enumerate(steps):
        x=_d(raw); b=f"$.run.steps[{i}]"; fn=x.get("function")
        if fn not in FUNCTIONS:_add(fs,"FUNCTION.UNKNOWN","error",f"Unknown function class '{fn}'.",b+".function")
        else:fc[fn]+=1
        if not _s(x.get("action")):_add(fs,"STEP.ACTION","error","Step action is required.",b+".action",dimension=fn if fn in FUNCTIONS else None)
        if x.get("status") not in {"completed","failed","skipped","running"}:_add(fs,"STEP.STATUS","error","Step status is invalid.",b+".status",dimension=fn if fn in FUNCTIONS else None)
        for j,r in enumerate(_l(x.get("inputs"))):
            if r not in input_ids and r not in art_ids:_add(fs,"REF.STEP_INPUT","error",f"Step input '{r}' does not resolve.",f"{b}.inputs[{j}]",dimension=fn if fn in FUNCTIONS else None)
        for j,r in enumerate(_l(x.get("outputs"))):
            if r not in art_ids:_add(fs,"REF.STEP_OUTPUT","error",f"Step output '{r}' does not resolve.",f"{b}.outputs[{j}]",dimension=fn if fn in FUNCTIONS else None)
        if fn=="F3":
            tool=_d(x.get("tool"))
            if not _s(tool.get("name")):_add(fs,"TOOL.NAME","error","Tool name is required.",b+".tool.name",dimension="F3")
            if not _s(tool.get("version")):_add(fs,"TOOL.VERSION","error","Tool version must be pinned.",b+".tool.version",dimension="F3")
            if not isinstance(tool.get("parameters"),dict):_add(fs,"TOOL.PARAMETERS","error","Tool parameters must be an object.",b+".tool.parameters",dimension="F3")
    req={"E1":("title",),"E2":("title","database","version"),"E3":("title","dataset_id","version","selection"),"E4":("title","software","version","parameters"),"E5":("title","model","version","input_signature"),"E6":("title","protocol_id","observed_at")}
    for i,raw in enumerate(evs):
        x=_d(raw); b=f"$.run.evidence[{i}]"; c=x.get("class")
        if c not in EVIDENCE:_add(fs,"EVIDENCE.UNKNOWN_CLASS","error",f"Unknown evidence class '{c}'.",b+".class");continue
        ec[c]+=1
        if not _time(x.get("retrieved_at")):_add(fs,"EVIDENCE.RETRIEVED_AT","error","Evidence requires an ISO-8601 retrieval timestamp.",b+".retrieved_at",dimension=c)
        src=_d(x.get("source"))
        for k in req[c]:
            ok=isinstance(src.get(k),dict) if k=="parameters" else _s(src.get(k))
            if not ok:_add(fs,f"{c}.{k.upper()}","error",f"{EVIDENCE[c]} requires source.{k}.",f"{b}.source.{k}",dimension=c)
        if c=="E1" and not any(_s(src.get(k)) for k in ("doi","pmid","url")):_add(fs,"E1.LOCATOR","error","Literature evidence requires DOI, PMID, or URL.",b+".source",dimension="E1")
        for j,r in enumerate(_l(x.get("artifact_ids"))):
            if r not in input_ids and r not in art_ids:_add(fs,"REF.EVIDENCE_ARTIFACT","error",f"Evidence artifact '{r}' does not resolve.",f"{b}.artifact_ids[{j}]",dimension=c)
    supported=qualified=high=0; rels={}
    for i,raw in enumerate(claims):
        x=_d(raw); b=f"$.run.claims[{i}]"; risk=x.get("risk"); sup=_l(x.get("support")); valid=0
        if not sup:_add(fs,"CLAIM.UNSUPPORTED","error","Claim has no evidence support edges.",b+".support")
        for j,e in enumerate(sup):
            e=_d(e); r=e.get("relation"); eid=e.get("evidence_id")
            if r not in RELATIONS:_add(fs,"CLAIM.RELATION","error",f"Unsupported relation '{r}'.",f"{b}.support[{j}].relation")
            else:rels[r]=rels.get(r,0)+1
            if eid not in ev_ids:_add(fs,"REF.CLAIM_EVIDENCE","error",f"Claim evidence '{eid}' does not resolve.",f"{b}.support[{j}].evidence_id")
            elif r!="contradicted_by":valid+=1
        if valid:supported+=1
        if not _s(x.get("uncertainty")):_add(fs,"CLAIM.UNCERTAINTY","warning" if risk=="low" else "error","Claim requires uncertainty.",b+".uncertainty")
        if not _s(x.get("limitations")):_add(fs,"CLAIM.LIMITATIONS","warning" if risk=="low" else "error","Claim requires limitations.",b+".limitations")
        if x.get("kind") in {"inference","causal_hypothesis","speculation"} and not _s(x.get("rationale")):_add(fs,"CLAIM.RATIONALE","error","Inferential claims require a rationale.",b+".rationale")
        if _s(x.get("uncertainty")) and _s(x.get("limitations")):qualified+=1
        if risk in {"high","clinical"}:high+=1;_add(fs,"CLAIM.CLINICAL_BOUNDARY","warning","High- or clinical-risk claim detected. FEVKit does not establish medical validity or safety.",b)
        for j,r in enumerate(_l(x.get("step_ids"))):
            if r not in step_ids:_add(fs,"REF.CLAIM_STEP","error",f"Claim step '{r}' does not resolve.",f"{b}.step_ids[{j}]")
    dec=_declared(run); verified=checked=missing=mismatch=unhashed=unsafe=0
    for b,x,k in dec:
        p=_safe(root,x.get("path"))
        if p is None:unsafe+=1;_add(fs,"ARTIFACT.UNSAFE_PATH","error",f"{k} path escapes the bundle.",b+".path");continue
        if not p.is_file():missing+=1;_add(fs,"ARTIFACT.MISSING_FILE","error",f"Declared file does not exist: {x.get('path')}",b+".path");continue
        expected=x.get("sha256")
        if not isinstance(expected,str) or not HASH_RE.fullmatch(expected):unhashed+=1;_add(fs,"ARTIFACT.HASH","error",f"{k} requires SHA-256.",b+".sha256");continue
        checked+=1
        if _sha(p)!=expected:mismatch+=1;_add(fs,"ARTIFACT.HASH_MISMATCH","error",f"Hash mismatch for {x.get('path')}.",b+".sha256")
        else:verified+=1
    privacy=_d(run.get("privacy")); personal=privacy.get("contains_personal_data"); sensitive=sum(_d(x).get("sensitive") is True for x in inputs)
    if not isinstance(personal,bool):_add(fs,"PRIVACY.ATTESTATION","error","Declare contains_personal_data.","$.run.privacy.contains_personal_data")
    if sensitive and personal is not True:_add(fs,"PRIVACY.CONTRADICTION","error","Sensitive input conflicts with privacy declaration.","$.run.privacy")
    env=_d(run.get("environment")); runtimes=_d(env.get("runtimes")); runtime=bool(runtimes) and all(_s(v) for v in runtimes.values()); locks=_l(env.get("lockfiles")); lock=bool(locks) and all(HASH_RE.fullmatch(str(_d(x).get("sha256",""))) for x in locks); container="@sha256:" in str(_d(env.get("container")).get("image",""))
    if not runtime:_add(fs,"ENV.RUNTIME","error","Declare exact runtime versions.","$.run.environment.runtimes")
    if not lock and not container:_add(fs,"ENV.NO_LOCK_OR_CONTAINER","error","Require hashed lockfile or digest-pinned container.","$.run.environment")
    replay=_d(run.get("replay")); command=replay.get("command"); command_ok=isinstance(command,list) and bool(command) and all(_s(x) for x in command); expected=_l(replay.get("expected_artifacts"))
    if not command_ok:_add(fs,"REPLAY.COMMAND","error","Declare replay.command as an argument array.","$.run.replay.command")
    if not expected:_add(fs,"REPLAY.EXPECTED_ARTIFACTS","error","Declare expected replay artifacts.","$.run.replay.expected_artifacts")
    val=_d(run.get("validation")); name=profile or val.get("profile") or "generic"; profiles=_profiles(); policy=profiles.get(name)
    if policy is None:_add(fs,"PROFILE.UNKNOWN","error",f"Unknown profile '{name}'.","$.run.validation.profile");name="generic";policy=profiles[name]
    evals=[_d(x) for x in _l(val.get("evaluations"))]; baseline=any(x.get("baseline") or x.get("control") for x in evals); stats=any(_l(x.get("metrics")) for x in evals); uncertainty=any(_d(x.get("uncertainty")) for x in evals); robustness=any(_d(x.get("robustness")) or _d(x.get("failure_analysis")) for x in evals); external=any(x.get("independent") is True or _s(x.get("external_site")) for x in evals); prospective=val.get("prospective") is True or any(x.get("prospective") is True for x in evals); closed=val.get("closed_loop") is True or any(x.get("closed_loop") is True for x in evals); human=any(_d(x).get("status")=="approved" for x in checks)
    for x in policy.get("required_functions",[]):
        if not fc[x]:_add(fs,"PROFILE.FUNCTION","error",f"Profile '{name}' requires {x}.","$.run.steps",dimension=x)
    for x in policy.get("required_evidence",[]):
        if not ec[x]:_add(fs,"PROFILE.EVIDENCE","error",f"Profile '{name}' requires {x}.","$.run.evidence",dimension=x)
    if policy.get("human_review") and not human:_add(fs,"PROFILE.HUMAN_REVIEW","error","Profile requires approved human checkpoint.","$.run.human_checkpoints")
    if policy.get("statistics") and not stats:_add(fs,"PROFILE.STATISTICS","error","Profile requires statistics.","$.run.validation.evaluations")
    if policy.get("uncertainty") and not uncertainty:_add(fs,"PROFILE.UNCERTAINTY","error","Profile requires uncertainty.","$.run.validation.evaluations")
    if policy.get("robustness") and not robustness:_add(fs,"PROFILE.ROBUSTNESS","error","Profile requires robustness.","$.run.validation.evaluations")
    all_verified=bool(dec) and verified==len(dec) and not (missing or mismatch or unhashed or unsafe); structural=any(x.severity=="error" and (x.code.startswith(("STEP.","TOOL.")) or x.code in {"REF.STEP_INPUT","REF.STEP_OUTPUT","FUNCTION.UNKNOWN"}) for x in fs); demonstrated=bool(steps) and bool(arts) and all(_d(x).get("status")=="completed" for x in steps) and not structural; replayable=demonstrated and all_verified and runtime and (lock or container) and command_ok and bool(expected); evaluated=replayable and bool(evals) and baseline and stats and uncertainty and robustness and human; empirical=evaluated and prospective and external and ec["E6"]>0; stage="V4" if empirical else "V3" if evaluated else "V2" if replayable else "V1" if demonstrated else "V0"; claimed=val.get("claimed_stage")
    if claimed not in STAGES:_add(fs,"VALIDATION.CLAIMED_STAGE","error","claimed_stage must be V0-V4.","$.run.validation.claimed_stage");claimed=None
    elif STAGE_RANK[claimed]>STAGE_RANK[stage]:_add(fs,"VALIDATION.OVERCLAIM","error",f"Run claims {claimed}, but supports at most {stage}.","$.run.validation.claimed_stage")
    if STAGE_RANK[stage]<STAGE_RANK.get(policy.get("minimum_stage","V1"),1):_add(fs,"PROFILE.MINIMUM_STAGE","error",f"Profile '{name}' requires at least {policy.get('minimum_stage')}; this bundle supports {stage}.","$.run.validation")
    quals=[]
    if baseline:quals.append("B")
    if human:quals.append("H")
    if stats and uncertainty:quals.append("S")
    if robustness:quals.append("R")
    if external:quals.append("X")
    if prospective:quals.append("P")
    if closed:quals.append("C")
    fstates=_states(FUNCTIONS,fc,fs);estates=_states(EVIDENCE,ec,fs);errors=sum(x.severity=="error" for x in fs);warnings=sum(x.severity=="warning" for x in fs);status="FAIL" if errors else "WARN" if warnings else "PASS";integrity={"declared_files":len(dec),"checked_files":checked,"verified_files":verified,"missing_files":missing,"hash_mismatches":mismatch,"unhashed_files":unhashed,"unsafe_paths":unsafe,"all_declared_files_verified":all_verified};metrics={"steps_total":len(steps),"artifacts_total":len(arts),"evidence_total":len(evs),"claims_total":len(claims),"claims_with_support":supported,"claims_fully_qualified":qualified,"high_or_clinical_risk_claims":high,"support_relations":rels,"function_coverage":round(sum(x["present"] for x in fstates.values())/6,4),"evidence_class_coverage":round(sum(x["present"] for x in estates.values())/6,4),"next_stage_blockers":[] if stage=="V4" else ["Capture evidence required for the next cumulative assurance stage."]}
    return AuditResult(status,run.get("id"),name,claimed,stage,STAGES[stage],tuple(quals),fstates,estates,tuple(fs),integrity,metrics,str(manifest))

def replay_bundle(bundle,*,execute=False,timeout=None,allowed_executables=None):
    source=Path(bundle).expanduser().resolve();manifest=source/"run.json" if source.is_dir() else source;root=manifest.parent;run=_d(json.loads(manifest.read_text()).get("run"));rp=_d(run.get("replay"));cmd=rp.get("command")
    if not isinstance(cmd,list) or not cmd or not all(_s(x) for x in cmd):raise FEVKitError("replay.command must be an argument array")
    exe=Path(cmd[0]).name;allow=set(allowed_executables or DEFAULT_EXECUTABLES)
    if exe not in allow:raise FEVKitError(f"replay executable '{exe}' is not allowed")
    arts={str(_d(x).get("id")):_d(x) for x in _l(run.get("artifacts"))};ids=_l(rp.get("expected_artifacts"));plan={"bundle":str(root),"command":cmd,"executable":exe,"timeout_seconds":int(timeout or rp.get("timeout_seconds") or 300),"network_declaration":rp.get("network","unspecified"),"expected_artifacts":ids,"executed":False,"matched":None,"notice":"Not a security sandbox."}
    if not execute:return plan
    with tempfile.TemporaryDirectory(prefix="fevkit-replay-") as td:
        work=Path(td)/"bundle";shutil.copytree(root,work);env={k:v for k,v in os.environ.items() if k in {"PATH","HOME","USER","TMPDIR","LANG","LC_ALL","SYSTEMROOT","WINDIR"}};done=subprocess.run(cmd,cwd=work,env=env,shell=False,capture_output=True,text=True,timeout=plan["timeout_seconds"],check=False);comparisons=[];matched=done.returncode==0
        for i in ids:
            x=arts.get(i,{}) ;p=_safe(work,x.get("path"));actual=_sha(p) if p and p.is_file() else None;ok=actual==x.get("sha256");matched=matched and ok;comparisons.append({"artifact_id":i,"path":x.get("path"),"expected_sha256":x.get("sha256"),"actual_sha256":actual,"matched":ok})
        plan.update({"executed":True,"returncode":done.returncode,"stdout":done.stdout[-20000:],"stderr":done.stderr[-20000:],"comparisons":comparisons,"matched":matched});return plan

def sarif_document(result):
    return {"$schema":"https://json.schemastore.org/sarif-2.1.0.json","version":"2.1.0","runs":[{"tool":{"driver":{"name":"FEVKit","version":"0.1.0"}},"results":[{"ruleId":x.code,"level":{"error":"error","warning":"warning","info":"note"}.get(x.severity,"note"),"message":{"text":x.message},"locations":[{"physicalLocation":{"artifactLocation":{"uri":result.manifest},"region":{"snippet":{"text":x.path}}}}]} for x in result.findings]}]}

def export_ro_crate(bundle):
    source=Path(bundle).expanduser().resolve();manifest=source/"run.json" if source.is_dir() else source;run=_d(json.loads(manifest.read_text()).get("run"));graph=[{"@id":"ro-crate-metadata.json","@type":"CreativeWork","about":{"@id":"./"},"conformsTo":{"@id":"https://w3id.org/ro/crate/1.1"}},{"@id":"./","@type":"Dataset","name":run.get("title","FEVKit run"),"description":run.get("objective",""),"conformsTo":[{"@id":"https://w3id.org/ro/wfrun/process/0.5"},{"@id":"https://fevkit.dev/spec/0.1"}],"hasPart":[{"@id":x.get("path")} for _,x,_ in _declared(run) if _s(x.get("path"))],"mentions":{"@id":"#run-"+str(run.get("id","unknown"))}},{"@id":"#run-"+str(run.get("id","unknown")),"@type":"CreateAction","name":run.get("title"),"description":run.get("objective"),"startTime":run.get("started_at"),"endTime":run.get("completed_at"),"instrument":{"@id":"#software"}},{"@id":"#software","@type":"SoftwareApplication","name":_d(run.get("system")).get("name"),"softwareVersion":_d(run.get("system")).get("version")}]
    for _,x,k in _declared(run):
        if _s(x.get("path")):graph.append({"@id":x["path"],"@type":"File","name":x.get("id",x["path"]),"encodingFormat":x.get("media_type","application/octet-stream"),"sha256":x.get("sha256"),"additionalType":"https://fevkit.dev/types/"+k})
    return {"@context":["https://w3id.org/ro/crate/1.1/context",{"fevkit":"https://fevkit.dev/terms/"}],"@graph":graph}
