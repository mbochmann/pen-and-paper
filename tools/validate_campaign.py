#!/usr/bin/env python3
"""Validate saved campaigns and their references. Python 3.10+, standard library only."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def schema_check(value, schema, path="$", *, check_keywords=True):
    supported = {
        "$schema", "title", "type", "enum", "anyOf", "properties", "required",
        "additionalProperties", "items", "minItems", "maxItems", "uniqueItems",
        "minimum", "maximum", "minLength", "pattern", "format",
    }
    if check_keywords:
        require(not set(schema) - supported, f"{path}: unsupported schema keyword")
    if "anyOf" in schema:
        for choice in schema["anyOf"]:
            try:
                schema_check(value, choice, path)
                break
            except ValueError:
                pass
        else:
            raise ValueError(f"{path}: no anyOf variant matches")
    types = {
        "null": value is None,
        "boolean": type(value) is bool,
        "integer": type(value) is int,
        "number": type(value) in (int, float),
        "string": isinstance(value, str),
        "array": isinstance(value, list),
        "object": isinstance(value, dict),
    }
    if "type" in schema:
        expected = schema["type"]
        expected = expected if isinstance(expected, list) else [expected]
        require(any(types.get(t, False) for t in expected), f"{path}: invalid type")
    if "enum" in schema:
        require(any(type(value) is type(v) and value == v for v in schema["enum"]),
                f"{path}: not in enum")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        require(set(schema.get("required", [])) <= set(value), f"{path}: missing fields")
        if schema.get("additionalProperties") is False:
            require(set(value) <= set(props), f"{path}: unexpected fields {set(value) - set(props)}")
        for key, sub in props.items():
            if key in value:
                schema_check(value[key], sub, f"{path}.{key}")
    if isinstance(value, list):
        require(len(value) >= schema.get("minItems", 0), f"{path}: too few items")
        require(len(value) <= schema.get("maxItems", float("inf")), f"{path}: too many items")
        if schema.get("uniqueItems"):
            encoded = [json.dumps(v, sort_keys=True) for v in value]
            require(len(encoded) == len(set(encoded)), f"{path}: duplicate items")
        if "items" in schema:
            for i, v in enumerate(value):
                schema_check(v, schema["items"], f"{path}[{i}]")
    if isinstance(value, str):
        require(len(value) >= schema.get("minLength", 0), f"{path}: empty string")
        if "pattern" in schema:
            require(re.search(schema["pattern"], value) is not None, f"{path}: invalid pattern")
        if schema.get("format") == "date-time":
            stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
            require(stamp.tzinfo is not None, f"{path}: timestamp needs timezone")
    if type(value) in (int, float):
        require(value >= schema.get("minimum", -float("inf")), f"{path}: below minimum")
        require(value <= schema.get("maximum", float("inf")), f"{path}: above maximum")


def unique(records, key, label):
    ids = [r[key] for r in records]
    require(len(ids) == len(set(ids)), f"{label}: duplicate {key}")
    return set(ids)


def validate_campaign(root, entry):
    base = root / entry["path"]
    state = read(base / entry["state"])
    schema_check(state, read(root / "structure/state.schema.json"))
    canon = read(base / "gm/canon.json")
    require(canon["schema_version"] == 1, "Unsupported canon version")
    require(canon["campaign_id"] == state["campaign_id"] == entry["id"], "Campaign mismatch")
    ids = unique(canon["entities"], "id", "canon")
    kinds = {e["id"]: e["kind"] for e in canon["entities"]}
    unique(canon["facts"], "id", "facts")

    def ref(value, kind=None):
        require(value in ids, f"Unknown reference: {value}")
        if kind:
            require(kinds[value] == kind, f"{value}: expected {kind}")

    for entity in canon["entities"]:
        require((base / entity["source"]).is_file(), f"Missing source: {entity['source']}")
    require((base / entry["entrypoint"]).is_file(), "Missing entrypoint")
    events = []
    event_schema = read(root / "structure/event.schema.json")
    for event_file in entry["events"]:
        lines = (base / event_file).read_text(encoding="utf-8").splitlines()
        require(all(line.strip() for line in lines), "Blank JSONL line")
        events.extend(json.loads(line) for line in lines)
    require(events, "Missing setup event")
    event_ids = unique(events, "id", "events")
    roll_ids = set()
    for revision, event in enumerate(events):
        schema_check(event, event_schema, f"events[{revision}]")
        require(event["campaign_id"] == entry["id"], "Event campaign mismatch")
        require(event["revision"] == revision, "Non-contiguous revision sequence")
        require(event["id"] == f"event-{revision:06d}", "Event ID/revision mismatch")
        require(event["type"] == "setup" if revision == 0 else event["type"] != "setup",
                "Setup must occur exactly once at revision zero")
        ref(event["scene_before"], "scene")
        ref(event["scene_after"], "scene")
        if revision:
            require(event["scene_before"] == events[revision - 1]["scene_after"],
                    "Broken event scene continuity")
        for entity_id in event["entity_ids"]:
            ref(entity_id)
        for clue_id in event["revealed_clue_ids"]:
            ref(clue_id, "clue")
        for older in event["supersedes_event_ids"]:
            require(older in {e["id"] for e in events[:revision]}, "Invalid correction target")
        for roll in event["rolls"]:
            require(roll["roll_id"] not in roll_ids, "Roll resolved twice")
            roll_ids.add(roll["roll_id"])
            ref(roll["actor_id"], "pc")
            original, final = roll["original_dice"], roll["final_dice"]
            index = roll["rerolled_index"]
            require(original == final if index is None else original[1-index] == final[1-index],
                    "Illegal dice replacement")
            total = sum(final) + roll["attribute_value"] + roll["bonus"]
            require(roll["total"] == total, "Incorrect roll total")
            delta = roll["target"] - total
            outcome = "success" if delta <= 0 else "cost_or_decline" if delta <= 2 else "setback"
            require(roll["outcome"] == outcome, "Incorrect roll outcome")
    last = events[-1]
    require(state["revision"] == last["revision"], "State/log revision mismatch")
    require(state["last_event_id"] == last["id"], "State/log event mismatch")
    require(state["scene_id"] == last["scene_after"], "State/log scene mismatch")
    require(state["pending_prompt"] == last["pending_prompt"], "State/log prompt mismatch")
    require(state["updated_at"] == last["at"], "State/log timestamp mismatch")
    for entity in canon["entities"]:
        if entity["origin"] == "improvised":
            require(entity["introduced_by_event_id"] in event_ids, "Untraced improvised entity")
    ref(state["scene_id"], "scene")
    if state["location_id"] is not None:
        ref(state["location_id"], "location")
    roles = read(base / "gm/roles.json")["roles"]
    role_ids = unique(roles, "id", "roles")
    for role in roles:
        require(sorted(role["attributes"].values()) == [0, 1, 1, 2], "Unbalanced starting role")
        require(len(role["starting_equipment"]) == 4, "Invalid starting equipment")
    require(unique(state["characters"], "id", "characters") == {"pc-1", "pc-2"}, "Missing PC")
    require(unique(state["characters"], "player_id", "players") == {"player-1", "player-2"}, "Missing player")
    held_items = list(state["party"]["item_ids"])
    for char in state["characters"]:
        require(char["player_id"] == char["id"].replace("pc-", "player-"), "Changed player mapping")
        if char["role_id"] is not None:
            require(char["role_id"] in role_ids, "Unknown role")
            require(all(char[f] is not None for f in ("attributes", "courage", "luck")), "Incomplete chosen role")
        else:
            require(all(char[f] is None for f in ("attributes", "courage", "luck")), "Unchosen role has stats")
            require(not char["equipment"], "Unchosen role has equipment")
        require(sum(e["slots"] for e in char["equipment"]) <= 6, "Equipment capacity exceeded")
        held_items.extend(e["item_id"] for e in char["equipment"] if e["item_id"] is not None)
    require(len(held_items) == len(set(held_items)), "Unique item has multiple owners")
    for item in held_items:
        ref(item, "item")
    if state["phase"] in ("playing", "completed") or state["party"]["starting_resources_granted"]:
        require(all(p["name"] and p["role_id"] for p in state["characters"]), "Play began before character selection")
        require(state["settings"]["dice_mode"] != "unselected", "Play began without dice mode")
        require(bool(state["party"]["bond"]), "Play began before bond confirmation")
        require(state["party"]["starting_resources_granted"], "Missing starting resources marker")
    if not state["party"]["starting_resources_granted"]:
        require(state["party"]["coins"] == 0, "Premature coins")
    unique(state["known_clues"], "clue_id", "known clues")
    for clue in state["known_clues"]:
        ref(clue["clue_id"], "clue")
        require(clue["discovered_event_id"] in event_ids, "Missing clue discovery event")
        discovery = next(e for e in events if e["id"] == clue["discovered_event_id"])
        require(clue["clue_id"] in discovery["revealed_clue_ids"], "Clue absent from discovery event")
    for field in ("world_changes", "party_hypotheses"):
        unique(state[field], "id", field)
        for change in state[field]:
            require(change["source_event_id"] in event_ids, f"{field}: missing event")
    unique(state["open_threads"], "id", "threads")
    unique(state["npc_states"], "npc_id", "NPC state")
    npc_locations = {}
    for npc in state["npc_states"]:
        ref(npc["npc_id"], "npc")
        if npc["location_id"] is not None:
            ref(npc["location_id"], "location")
        npc_locations[npc["npc_id"]] = npc["location_id"]
    for npc in state["present_npc_ids"]:
        ref(npc, "npc")
        require(state["location_id"] is not None and npc_locations.get(npc) == state["location_id"],
                "Present NPC is in a different location")
    unique(state["quests"], "quest_id", "quests")
    for quest in state["quests"]:
        ref(quest["quest_id"], "quest")
        require(not quest["reward_granted"] or quest["status"] == "completed", "Premature quest reward")
    unique(state["clocks"], "clock_id", "clocks")
    for clock in state["clocks"]:
        ref(clock["clock_id"], "clock")
        require(clock["value"] <= clock["max"], "Clock overflow")
        if clock["last_trigger_event_id"] is not None:
            require(clock["last_trigger_event_id"] in event_ids, "Clock trigger event missing")
    world = {change["key"]: change["value"] for change in state["world_changes"]}
    if world.get("water-restored"):
        require(not next(c for c in state["clocks"] if c["clock_id"] == "clock-shortage")["active"],
                "Shortage clock still active after restoration")
    pending = state["pending_roll"]
    if pending is not None:
        require(state["settings"]["dice_mode"] in ("physical", "tool"), "Roll in non-dice mode")
        require(state["pending_action"] is not None, "Pending roll without intention")
        require(pending["roll_id"] not in roll_ids, "Resolved roll is still pending")
        actor = next(p for p in state["characters"] if p["id"] == pending["actor_id"])
        require(actor["attributes"] is not None, "Roll for unchosen character")
        require(actor["attributes"][pending["attribute"]] == pending["attribute_value"], "Wrong pending attribute")
        if pending["reroll_index"] is not None:
            require(len(pending["raw_dice"]) == 2, "Reroll without original dice")
    if state["challenge"] is not None:
        require(state["challenge"]["progress"] <= state["challenge"]["target"], "Challenge overflow")
    resume = (base / "state/resume.md").read_text(encoding="utf-8")
    require(f"Revision {state['revision']}" in resume, "Stale resume revision")
    require(state["last_event_id"] in resume, "Stale resume event")
    require(state["pending_prompt"] in resume, "Stale resume prompt")
    journal = (base / "players/journal.md").read_text(encoding="utf-8")
    require(f"Speicherpunkt {state['revision']}" in journal, "Stale player journal")
    return len(events), len(ids)


def main():
    index = read(ROOT / "campaigns/index.json")
    require(index["schema_version"] == 1, "Unsupported index version")
    campaign_ids = unique(index["campaigns"], "id", "campaign index")
    require(index["active_campaign_id"] in campaign_ids, "Active campaign missing")
    for entry in index["campaigns"]:
        events, entities = validate_campaign(ROOT, entry)
        print(f"OK {entry['id']}: {events} events, {entities} registered entities")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        sys.exit(1)
