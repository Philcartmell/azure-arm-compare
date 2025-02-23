# ARM Compare

ARM Compare is a Python script designed to compare two Azure Resource Manager (ARM) template export files. The script focuses on comparing the configuration attributes of resources, generating a detailed Markdown report that includes both a summary and a full property-by-property comparison for each matched resource.

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

- **Detailed Markdown Report:**  
  Generates a report with a summary table and detailed comparison tables. The comparison tables list properties side-by-side with a **Fail** column marking differences using a cross (✗).  

- **Clickable Anchors:**  
  The resource names in the summary are clickable links that scroll down to their detailed comparison sections.

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Philcartmell/azure-arm-compare.git
   cd azure-arm-compare
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

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

## How to Use It

Run the script using the command line with the following arguments:

- `--left`: Path to the left ARM template JSON file.
- `--right`: Path to the right ARM template JSON file.
- `--config`: (Optional) Path to a YAML configuration file.
- `--output`: Path to the Markdown file where the comparison result will be saved.

### Example Execution

```bash
python arm-compare.py --left samples/left.json --right samples/right.json --config config.yaml --output sample_output.md
```

## Contributing

Contributions and improvements are welcome! Feel free to fork the repository and submit pull requests for enhancements or bug fixes.

## License

This project is licensed under the MIT License.
