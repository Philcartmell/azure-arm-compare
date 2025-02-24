# ARM Compare

ARM Compare is a Python script designed to compare two Azure Resource Manager (ARM) template export files. The script focuses on comparing the configuration attributes of resources, generating a detailed report that includes both a summary and a full property-by-property comparison for each matched resource.

The report contains clickable anchors in the summary table, allowing you to jump directly to the detailed comparison for any resource.

## Features

- **Resource Pairing by Type and Name:**  
  Automatically pairs resources based on their type and name. You can also provide custom mappings in a YAML configuration file if resource names differ.

- **Enhanced Prefix-Based Resource Mapping:**  
  When you provide a mapping with a base resource type and name, child resources are automatically paired by appending any additional segments. For example, a mapping defined for  
  `Microsoft.Storage/storageAccounts` with name `storage001` will automatically map a resource such as  
  `Microsoft.Storage/storageAccounts/blobServices` with name `storage001/default` to the corresponding target by appending `/blobServices` and `/default` to the right-side mapping.

- **Wildcard Ignore Rules:**  
  Exclude specific properties from the comparison using wildcard patterns (e.g., `tags.*` or `dependsOn*`).

- **Detailed Report Generation:**  
  Generates a report with a summary table and detailed comparison tables. For Markdown output, the tables list properties side-by-side with a **Fail** column marking differences using a cross (✗).

- **Clickable Anchors:**  
  The resource names in the summary are clickable links that scroll down to their detailed comparison sections.

## Download or Install

### PyPI

```bash
pip install azure-arm-compare
```

Once installed, you can use the command-line tool by running:

```bash
arm-compare --help
```

Or, if you prefer to use it programmatically in your Python code:

```python
import arm_compare

# For example, to invoke the main function:
arm_compare.main()
```

### GitHub clone

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Philcartmell/azure-arm-compare.git
   cd azure-arm-compare
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## How to Use It

See `samples` folder.

Run the script using the command line with the following arguments:

- `--left`: Path to the left ARM template JSON file.
- `--right`: Path to the right ARM template JSON file.
- `--config`: (Optional) Path to a YAML configuration file.
- `--output`: Path to the output file where the comparison result will be saved.
- `--format`: (Optional) Output format: either `markdown` or `html` (default).

## Exporting ARM Templates

When exporting ARM templates from Azure, ensure that you exclude parameters. This ensures that resource names remain fixed in the output, which is critical for accurate comparisons.

## Configuration

A YAML configuration file is optional but recommended if your ARM templates use different resource names for corresponding resources. Use the configuration file to define additional ignore rules and resource mappings.

### Sample YAML Configuration (`config.yaml`)

The config.yaml file is optional, but unless the resource names are identical you'll probably want to provide it.

```yaml
ignoreRules:
  - "name"
  - "dependsOn*"
resourceMappings:
  - leftResourceType: "Microsoft.Storage/storageAccounts"
    leftResourceName: "storage001"
    rightResourceType: "Microsoft.Storage/storageAccounts"
    rightResourceName: "storage002"
```

- **ignoreRules:** A list of property paths to ignore during comparison. Wildcards are supported.
- **resourceMappings:**  
  A list of mappings to manually pair resources if their names differ between the left and right ARM templates. The enhanced mapping logic supports prefix-based matching so that if a resource’s type and name start with the specified mapping values, any additional segments (child resources) are automatically appended to the right-side mapping.

### Example Execution

```bash
python arm-compare.py --left samples/left.json --right samples/right.json --config config.yaml --output sample_output.md
```

## Release History

### Version 0.0.3

No functional changes - Fix to PyPI release.

### Version 0.0.2
- **HTML as Default Output:** HTML output is now the default output format.
- **Expandable Value Cells:**  
  For HTML output, if a left or right value exceeds 64 characters, the script truncates it and provides a `[more]` link. Clicking the link expands the full value and toggles to `[less]` to collapse it again.
- **Row Highlight on Click:**  
  In HTML output, clicking on a cell in the Property Path column highlights the entire row in yellow, making it easier to compare properties across the row.
- **Enhanced Summary:**  
  The summary table now includes an additional "Ignored" column. The summary aggregates the counts so that the sum of Ignored, Correct, and Incorrect equals the Total Properties compared.

### Version 0.0.1 (Initial Release)
- **Markdown Report Generation:**  
  Initially generated a Markdown report with a summary table and detailed property-by-property comparisons.
- **Resource Pairing by Type and Name:**  
  Automatic pairing of resources by type and name with clickable anchors in the summary.
- **Enhanced Prefix-Based Resource Mapping:**  
  Support for prefix-based matching in resource mappings.
- **Wildcard Ignore Rules:**  
  Ability to ignore properties using wildcard patterns.

## Contributing

Contributions and improvements are welcome! Feel free to fork the repository and submit pull requests for enhancements or bug fixes.

## License

This project is licensed under the MIT License.