# Azure ARM Comparer

Azure ARM Comparer is a Python script designed to compare two Azure Resource Manager (ARM) template export files. The script focuses on comparing the configuration attributes of resources, generating a detailed Markdown report that includes both a summary and a full property-by-property comparison for each matched resource.

The report contains clickable anchors in the summary table, allowing you to jump directly to the detailed comparison for any resource.

## Features

- **Resource Pairing by Type and Name:** Automatically pairs resources based on their type and name. You can also provide custom mappings in a YAML configuration file if resource names differ.
- **Wildcard Ignore Rules:** Exclude specific properties from the comparison using wildcard patterns (e.g., `tags.*`).
- **Detailed Markdown Report:** Generates a report with a summary table, detailed comparison tables (including line numbers), and lists of unmatched resources.
- **Clickable Anchors:** The resource names in the summary are clickable links that scroll down to their detailed comparison sections.
- **Fail Column:** In the detailed comparison, any property that fails (i.e. the left and right values differ) is marked with a cross (✗). Properties that are ignored show **Ignored**, while matching properties leave the cell blank for easier review.

## Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/azure-arm-comparer.git
   cd azure-arm-comparer
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

```yaml
ignoreRules:
  - "properties.provisioningState"
  - "tags.*"
resourceMappings:
  - leftResourceType: "Microsoft.Compute/virtualMachines"
    leftResourceName: "myLeftVM"
    rightResourceType: "Microsoft.Compute/virtualMachines"
    rightResourceName: "myRightVM"
```

- **ignoreRules:** A list of property paths to ignore during comparison. Wildcards are supported.
- **resourceMappings:** A list of mappings to manually pair resources if their names differ between the left and right ARM templates.

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

## Sample Markdown Output

Below is an example of the generated Markdown output with the updated **Fail** column.

```markdown
# Summary

## Ignored Properties

The following properties were ignored during comparisons:
- properties.provisioningState
- tags.*

## Compared Resources

| Resource Type                     | Name                                                          | Total Properties | Correct | Incorrect |
| --------------------------------- | ------------------------------------------------------------- | ---------------- | ------- | --------- |
| Microsoft.Compute/virtualMachines | [myLeftVM](#microsoftcompute-virtualmachines-myleftvm)         | 25               | 23      | 2         |
| Microsoft.Storage/storageAccounts | [mystorage](#microsoftstorage-storageaccounts-mystorage)         | 18               | 18      | 0         |

## Unmatched Resources in Left Template

| Resource Type                         | Name        |
| ------------------------------------- | ----------- |
| Microsoft.Network/networkInterfaces   | nicLeft     |

## Unmatched Resources in Right Template

| Resource Type                         | Name        |
| ------------------------------------- | ----------- |
| Microsoft.Network/networkInterfaces   | nicRight    |

---

<a id="microsoftcompute-virtualmachines-myleftvm"></a>
### Comparison for Resource: Microsoft.Compute/virtualMachines / myLeftVM

| Property Path                               | Left Value (Line No.)      | Right Value (Line No.)     | Fail     |
| ------------------------------------------- | -------------------------- | -------------------------- | -------- |
| properties.hardwareProfile.vmSize           | Standard_DS2_v2 (45)       | Standard_DS2_v2 (46)       |          |
| properties.storageProfile.osDisk.name       | osDisk1 (50)               | osDisk1-renamed (51)       | ✗        |
... (additional rows)

<a id="microsoftstorage-storageaccounts-mystorage"></a>
### Comparison for Resource: Microsoft.Storage/storageAccounts / mystorage

| Property Path                | Left Value (Line No.) | Right Value (Line No.) | Fail     |
| ---------------------------- | --------------------- | ---------------------- | -------- |
| properties.accountType       | Standard_LRS (30)     | Standard_LRS (31)      |          |
... (additional rows)
```

## Version / Release History

- **v1.1.0** (2025-02-23)
  - Updated detailed comparison table with a **Fail** column.
  - Properties that match leave the cell empty.
  - Non-matching properties are marked with a cross (✗).
  - Ignored properties display "Ignored" and are listed in the summary.
- **v1.0.0** (2025-02-23)
  - Initial release.
  - Resource pairing by type and name.
  - Detailed Markdown output with clickable summary links.
  - Support for wildcard ignore rules and resource mappings.

## Contributing

Contributions and improvements are welcome! Feel free to fork the repository and submit pull requests for enhancements or bug fixes.

## License

This project is licensed under the MIT License.
