#!/usr/bin/env python3
import argparse
import json
import yaml
import re
import fnmatch
import os
import sys

def exit_with_error(message):
    sys.stderr.write(message + "\n")
    sys.stderr.flush()
    sys.exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Compare two ARM templates by type and name')
    parser.add_argument('--left', required=True, help='Left ARM template JSON file')
    parser.add_argument('--right', required=True, help='Right ARM template JSON file')
    parser.add_argument('--config', help='Configuration YAML file (optional)')
    parser.add_argument('--output', required=True, help='Output Markdown file')
    return parser.parse_args()

def load_json_file(filepath):
    if not os.path.exists(filepath):
        exit_with_error(f"Error: JSON file '{filepath}' does not exist.")
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        exit_with_error(f"Error: Failed to read JSON file '{filepath}': {e}")

def load_yaml_file(filepath):
    if not os.path.exists(filepath):
        exit_with_error(f"Error: YAML config file '{filepath}' does not exist.")
    try:
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        exit_with_error(f"Error: Failed to read YAML config file '{filepath}': {e}")

def flatten_json(data, parent_key=''):
    """
    Recursively flattens JSON into a dict mapping full property paths to values.
    Lists are indexed.
    """
    items = {}
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(flatten_json(v, new_key))
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    list_key = f"{new_key}[{i}]"
                    if isinstance(item, (dict, list)):
                        items.update(flatten_json(item, list_key))
                    else:
                        items[list_key] = item
            else:
                items[new_key] = v
    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_key = f"{parent_key}[{i}]"
            if isinstance(item, (dict, list)):
                items.update(flatten_json(item, new_key))
            else:
                items[new_key] = item
    else:
        items[parent_key] = data
    return items

def find_line_number(resource_key, prop_key, raw_lines, start_line=0):
    """
    Naively searches for the resource key (e.g. type and name) in the raw JSON lines to determine a starting line.
    Then, from that point, searches for the given property key (wrapped in quotes).
    Returns a 1-indexed line number or an empty string if not found.
    """
    resource_start = None
    for idx, line in enumerate(raw_lines):
        if resource_key in line:
            resource_start = idx
            break
    if resource_start is None:
        resource_start = start_line
    for idx in range(resource_start, len(raw_lines)):
        if f'"{prop_key}"' in raw_lines[idx] or f"'{prop_key}'" in raw_lines[idx]:
            return idx + 1  # convert to 1-indexed
    return ''

def get_resource_line_numbers(resource, raw_lines):
    """
    For a given resource (a dict) and the raw JSON lines (as a list),
    returns a mapping from each flattened property path to the line number
    where its last key segment is found.
    """
    line_numbers = {}
    resource_key = f'{resource.get("type", "")} {resource.get("name", "")}'
    flat = flatten_json(resource)
    for key in flat.keys():
        last_segment = key.split('.')[-1]
        line_numbers[key] = find_line_number(resource_key, last_segment, raw_lines)
    return line_numbers

def generate_anchor(resource_type, resource_name):
    """
    Generates a sanitized anchor string based on resource type and name.
    """
    combined = f"{resource_type}-{resource_name}"
    anchor = re.sub(r'[^a-zA-Z0-9-]', '', combined.replace(' ', '-')).lower()
    return anchor

def generate_markdown_table(resource_key_display, left_flat, right_flat, left_lines, right_lines, ignore_rules, ignored_set):
    """
    Given two flattened dicts for a resource (left and right), along with mappings of property keys to their detected
    line numbers, generate a Markdown table comparing the property values.
    If a property key matches an ignore rule, its fail result is set to "Ignored" (and added to ignored_set);
    if it doesn't match and the left/right values differ, a cross (✗) is printed;
    if they match, the cell is left empty.
    """
    md_lines = []
    md_lines.append(f"### Comparison for Resource: {resource_key_display}\n")
    md_lines.append("| Property Path | Left Value (Line No.) | Right Value (Line No.) | Fail |")
    md_lines.append("| --- | --- | --- | --- |")
    all_keys = set(left_flat.keys()).union(set(right_flat.keys()))
    for key in sorted(all_keys):
        is_ignored = ignore_rules and any(fnmatch.fnmatch(key, pattern) for pattern in ignore_rules)
        if is_ignored:
            fail_cell = "Ignored"
            ignored_set.add(key)
        else:
            fail_cell = "" if left_flat.get(key, '') == right_flat.get(key, '') else "✗"
        left_val = left_flat.get(key, '')
        right_val = right_flat.get(key, '')
        left_line = left_lines.get(key, '')
        right_line = right_lines.get(key, '')
        left_val_with_line = f"{left_val} ({left_line})" if left_line else f"{left_val}"
        right_val_with_line = f"{right_val} ({right_line})" if right_line else f"{right_val}"
        md_lines.append(f"| {key} | {left_val_with_line} | {right_val_with_line} | {fail_cell} |")
    return "\n".join(md_lines)

def main():
    args = parse_arguments()

    # Check if left and right files exist (config is optional)
    if not os.path.exists(args.left):
        exit_with_error(f"Error: Left file '{args.left}' does not exist.")
    if not os.path.exists(args.right):
        exit_with_error(f"Error: Right file '{args.right}' does not exist.")
    if args.config and not os.path.exists(args.config):
        exit_with_error(f"Error: Config file '{args.config}' does not exist.")

    # Load JSON templates and raw lines for line number detection.
    left_template = load_json_file(args.left)
    right_template = load_json_file(args.right)
    try:
        with open(args.left, 'r') as f:
            left_raw_lines = f.readlines()
    except Exception as e:
        exit_with_error(f"Error: Failed to read left file raw lines: {e}")
    try:
        with open(args.right, 'r') as f:
            right_raw_lines = f.readlines()
    except Exception as e:
        exit_with_error(f"Error: Failed to read right file raw lines: {e}")

    # Load YAML configuration if provided.
    config = {}
    ignore_rules = []
    resource_mappings = []
    if args.config:
        config = load_yaml_file(args.config)
        ignore_rules = config.get('ignoreRules', [])
        resource_mappings = config.get('resourceMappings', [])
    
    # Always add "dependsOn" to the ignore rules.
    if "dependsOn" not in ignore_rules:
        ignore_rules.append("dependsOn")

    # Global set to accumulate all ignored property keys.
    ignored_properties = set()

    # Extract resources (assumed under "resources") and pair by (type, name).
    left_resources = left_template.get("resources", [])
    right_resources = right_template.get("resources", [])

    def get_key(resource):
        return (resource.get("type"), resource.get("name"))
    
    left_dict = {get_key(res): res for res in left_resources if res.get("type") and res.get("name")}
    right_dict = {get_key(res): res for res in right_resources if res.get("type") and res.get("name")}

    resource_pairs = []
    summary_entries = []  # Each entry: (resource_type, resource_name, total, correct, incorrect, anchor)

    # Use resourceMappings from config if provided.
    for mapping in resource_mappings:
        left_key = (mapping.get("leftResourceType"), mapping.get("leftResourceName"))
        right_key = (mapping.get("rightResourceType"), mapping.get("rightResourceName"))
        if left_key in left_dict and right_key in right_dict:
            resource_pairs.append((left_dict[left_key], right_dict[right_key]))
            del left_dict[left_key]
            del right_dict[right_key]

    # Pair any remaining resources by (type, name).
    for key in list(left_dict.keys()):
        if key in right_dict:
            resource_pairs.append((left_dict[key], right_dict[key]))
            del left_dict[key]
            del right_dict[key]

    detailed_sections = []
    for left_res, right_res in resource_pairs:
        resource_type = left_res.get("type", "Unknown type")
        resource_name = left_res.get("name", "Unknown name")
        resource_key_display = f"{resource_type} / {resource_name}"
        anchor = generate_anchor(resource_type, resource_name)

        if ignore_rules and any(fnmatch.fnmatch(resource_type, pattern) for pattern in ignore_rules):
            continue

        left_flat = flatten_json(left_res)
        right_flat = flatten_json(right_res)
        left_line_numbers = get_resource_line_numbers(left_res, left_raw_lines)
        right_line_numbers = get_resource_line_numbers(right_res, right_raw_lines)
        
        all_keys = set(left_flat.keys()).union(set(right_flat.keys()))
        total = correct = incorrect = 0
        for key in sorted(all_keys):
            is_ignored = ignore_rules and any(fnmatch.fnmatch(key, pattern) for pattern in ignore_rules)
            total += 1
            if not is_ignored:
                if left_flat.get(key, '') == right_flat.get(key, ''):
                    correct += 1
                else:
                    incorrect += 1

        summary_entries.append((resource_type, resource_name, total, correct, incorrect, anchor))
        detailed_section = f'<a id="{anchor}"></a>\n'
        detailed_section += generate_markdown_table(resource_key_display, left_flat, right_flat, left_line_numbers, right_line_numbers, ignore_rules, ignored_properties)
        detailed_sections.append(detailed_section)
        detailed_sections.append("\n")

    # Build summary section.
    summary_lines = []
    summary_lines.append("# Summary\n")
    # Add a section for Ignored Properties if any were found.
    if ignored_properties:
        summary_lines.append("## Ignored Properties\n")
        summary_lines.append("The following properties were ignored during comparisons:")
        for prop in sorted(ignored_properties):
            summary_lines.append(f"- {prop}")
        summary_lines.append("")  # Blank line

    summary_lines.append("## Compared Resources\n")
    summary_lines.append("| Resource Type | Name | Total Properties | Correct | Incorrect |")
    summary_lines.append("| --- | --- | --- | --- | --- |")
    for entry in summary_entries:
        rtype, rname, total, correct, incorrect, anchor = entry
        summary_lines.append(f"| {rtype} | [{rname}](#{anchor}) | {total} | {correct} | {incorrect} |")
    
    # Build unmatched resources summary as tables.
    if left_dict:
        summary_lines.append("\n## Unmatched Resources in Left Template\n")
        summary_lines.append("| Resource Type | Name |")
        summary_lines.append("| --- | --- |")
        for res in left_dict.values():
            rtype = res.get("type", "Unknown type")
            rname = res.get("name", "Unknown name")
            summary_lines.append(f"| {rtype} | {rname} |")
    if right_dict:
        summary_lines.append("\n## Unmatched Resources in Right Template\n")
        summary_lines.append("| Resource Type | Name |")
        summary_lines.append("| --- | --- |")
        for res in right_dict.values():
            rtype = res.get("type", "Unknown type")
            rname = res.get("name", "Unknown name")
            summary_lines.append(f"| {rtype} | {rname} |")

    output_sections = []
    output_sections.extend(summary_lines)
    output_sections.append("\n---\n")
    output_sections.extend(detailed_sections)

    try:
        with open(args.output, 'w') as f:
            f.write("\n".join(output_sections))
    except Exception as e:
        exit_with_error(f"Error: Failed to write output file '{args.output}': {e}")

if __name__ == '__main__':
    main()
