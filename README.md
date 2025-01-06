# lsdll
List windows dll resources 

## Requirements
- Windows environment
- Python 3
- pywin32

## Usage 

### List resources 
```bash 
python3 lsdll.py --list <dll_path>
``` 
### Extract resource 
```bash 
python3 lsdll.py --extract --type 3 --name VIEWS.html
``` 
### Other usages
```bash
usage: lsdll.py [-h] [--list] [--extract] [--type TYPE] [--name NAME] [--output OUTPUT] dll_path

List and extract resources from a DLL.

positional arguments:
  dll_path              Path to the DLL file.

options:
  -h, --help            show this help message and exit
  --list, -l            List resources in the DLL.
  --extract, -x         Extract resources in the DLL.
  --type TYPE, -t TYPE  Resource type (name or integer).
  --name NAME, -n NAME  Resource name or ID.
  --output OUTPUT, -o OUTPUT
                        Output file or folder path.
```
