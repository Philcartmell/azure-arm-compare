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

def generate_anchor(resource_type, resource_name):
    """
    Generates a sanitized anchor string based on resource type and name.
    """
    combined = f"{resource_type}-{resource_name}"
    anchor = re.sub(r'[^a-zA-Z0-9-]', '', combined.replace(' ', '-')).lower()
    return anchor

def generate_markdown_table(resource_key_display, left_flat, right_flat, ignore_rules, ignored_set):
    """
    Given two flattened dicts for a resource (left and right), generate a Markdown table comparing the property values.
    If a property key matches an ignore rule, its fail result is set to "Ignored" (and added to ignored_set);
    if it doesn't match and the left/right values differ, a cross (✗) is printed;
    if they match, the cell is left empty.
    """
    md_lines = []
    md_lines.append(f"### Comparison for Resource: {resource_key_display}\n")
    md_lines.append("| Property Path | Left Value | Right Value | Fail |")
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
        md_lines.append(f"| {key} | {left_val} | {right_val} | {fail_cell} |")
    return "\n".join(md_lines)

def main():
    args = parse_arguments()

    if not os.path.exists(args.left):
        exit_with_error(f"Error: Left file '{args.left}' does not exist.")
    if not os.path.exists(args.right):
        exit_with_error(f"Error: Right file '{args.right}' does not exist.")
    if args.config and not os.path.exists(args.config):
        exit_with_error(f"Error: Config file '{args.config}' does not exist.")

    left_template = load_json_file(args.left)
    right_template = load_json_file(args.right)

    config = {}
    ignore_rules = []
    resource_mappings = []
    if args.config:
        config = load_yaml_file(args.config)
        ignore_rules = config.get('ignoreRules', [])
        resource_mappings = config.get('resourceMappings', [])
    
    if "dependsOn" not in ignore_rules:
        ignore_rules.append("dependsOn")

    ignored_properties = set()

    left_resources = left_template.get("resources", [])
    right_resources = right_template.get("resources", [])

    def get_key(resource):
        return (resource.get("type"), resource.get("name"))
    
    left_dict = {get_key(res): res for res in left_resources if res.get("type") and res.get("name")}
    right_dict = {get_key(res): res for res in right_resources if res.get("type") and res.get("name")}

    resource_pairs = []
    summary_entries = []

    # Enhanced partial mapping based on prefixes
    for mapping in resource_mappings:
        left_prefix_type = mapping.get("leftResourceType")
        left_prefix_name = mapping.get("leftResourceName")
        right_prefix_type = mapping.get("rightResourceType")
        right_prefix_name = mapping.get("rightResourceName")
        
        for key in list(left_dict.keys()):
            ltype, lname = key
            if ltype.startswith(left_prefix_type) and lname.startswith(left_prefix_name):
                type_remainder = ltype[len(left_prefix_type):]
                name_remainder = lname[len(left_prefix_name):]
                candidate_right_type = right_prefix_type + type_remainder
                candidate_right_name = right_prefix_name + name_remainder
                candidate_key = (candidate_right_type, candidate_right_name)
                if candidate_key in right_dict:
                    resource_pairs.append((left_dict[key], right_dict[candidate_key]))
                    del left_dict[key]
                    del right_dict[candidate_key]

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
        
        total = correct = incorrect = 0
        all_keys = set(left_flat.keys()).union(set(right_flat.keys()))
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
        detailed_section += generate_markdown_table(resource_key_display, left_flat, right_flat, ignore_rules, ignored_properties)
        detailed_sections.append(detailed_section)
        detailed_sections.append("\n")

    summary_lines = []
    summary_lines.append("# Summary\n")
    if ignored_properties:
        summary_lines.append("## Ignored Properties\n")
        summary_lines.append("The following properties were ignored during comparisons:")
        for prop in sorted(ignored_properties):
            summary_lines.append(f"- {prop}")
        summary_lines.append("")

    summary_lines.append("## Compared Resources\n")
    summary_lines.append("| Resource Type | Name | Total Properties | Correct | Incorrect |")
    summary_lines.append("| --- | --- | --- | --- | --- |")
    for entry in summary_entries:
        rtype, rname, total, correct, incorrect, anchor = entry
        summary_lines.append(f"| {rtype} | [{rname}](#{anchor}) | {total} | {correct} | {incorrect} |")
    
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
