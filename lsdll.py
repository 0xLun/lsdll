import win32api
import win32con
import argparse
import os

# Map resource types to human-readable names
RESOURCE_TYPE_MAP = {
    win32con.RT_CURSOR: "Cursor [RT_CURSOR]",
    win32con.RT_ANICURSOR: "Animated Cursor [RT_ANICURSOR]",
    win32con.RT_BITMAP: "Bitmap [RT_BITMAP]",
    win32con.RT_ICON: "Icon [RT_ICON]",
    win32con.RT_ANIICON: "Animated Icon [RT_ANIICON]",
    win32con.RT_MENU: "Menu [RT_MENU]",
    win32con.RT_DIALOG: "Dialog [RT_DIALOG]",
    win32con.RT_STRING: "String Table [RT_STRING]",
    win32con.RT_FONTDIR: "Font Directory [RT_FONTDIR]",
    win32con.RT_FONT: "Font [RT_FONT]",
    win32con.RT_ACCELERATOR: "Accelerator Table [RT_ACCELERATOR]",
    win32con.RT_RCDATA: "Raw Data [RT_RCDATA]",
    win32con.RT_MESSAGETABLE: "Message Table [RT_MESSAGETABLE]",
    win32con.RT_GROUP_CURSOR: "Group Cursor [RT_GROUP_CURSOR]",
    win32con.RT_GROUP_ICON: "Group Icon [RT_GROUP_ICON]",
    win32con.RT_VERSION: "Version [RT_VERSION]",
    win32con.RT_DLGINCLUDE: "Dialog Include [RT_DLGINCLUDE]",
    win32con.RT_HTML: "HTML [RT_DLGINCLUDE]",
    #win32con.RT_MANIFEST: "Manifest",
    24 : "Manifest",
    win32con.RT_VXD: "VXD",
    #win32con.PLUGPLAY: "Plug and Play resource",
    19 : "Plug and Play resource",
}

def get_resource_type(value):
    """Convert a resource type name or integer to the corresponding integer."""
    if value.isdigit():
        return int(value)
    for key, name in RESOURCE_TYPE_MAP.items():
        if name.lower() == value.lower():
            return key
    raise ValueError(f"Invalid resource type: {value}")

def get_resource_name(resource_type):
    """Return a human-readable name for the resource type."""
    return RESOURCE_TYPE_MAP.get(resource_type, f"Unknown ({resource_type})")


def list_resources_in_dll_legacy(dll_path):
    # Enumerate all resource types
    try:
        # Load the DLL as a data file
        handle = win32api.LoadLibraryEx(dll_path, 0, win32con.LOAD_LIBRARY_AS_DATAFILE)
    except Exception as e:
        print(f"Failed to load DLL: {e}")
        return
    
    print(f"Resources in {dll_path}:\n")
    print(RESOURCE_TYPE_MAP)

    try:
        # Enumerate all resource types
        resource_types = win32api.EnumResourceTypes(handle)
        for resource_type in resource_types:
            print(f"Resource Type: {RESOURCE_TYPE_MAP[resource_type] if ( isinstance(resource_type, int) and resource_type in RESOURCE_TYPE_MAP )  else ''} ({resource_type})")
            
            # Enumerate resources of this type
            resource_names = win32api.EnumResourceNames(handle, resource_type)
            for resource_name in resource_names:
                print(f"  Resource Name: {resource_name}")
    except Exception as e:
        print(f"Error enumerating resources: {e}")
    finally:
        # Free the loaded DLL
        win32api.FreeLibrary(handle)
            

def list_resources_in_dll(dll_path):
    """List resources in the specified DLL."""
    try:
        handle = win32api.LoadLibraryEx(dll_path, 0, win32con.LOAD_LIBRARY_AS_DATAFILE)
    except Exception as e:
        print(f"Failed to load DLL: {e}")
        return

    resources_dict = {}

    try:
        # Go through all known resource types and enumerate their names
        for resource_type in RESOURCE_TYPE_MAP:
            try:
                resource_names = win32api.EnumResourceNames(handle, resource_type)
                for resource_name in resource_names:
                    # Map the type to human-readable names or use the raw integer identifier
                    resource_type_name = get_resource_name(resource_type)
                    if resource_type not in resources_dict:
                        resources_dict[resource_type] = {
                            "type_name": resource_type_name,
                            "names": []
                        }
                    resources_dict[resource_type]["names"].append(resource_name)
            except Exception:
                # If a resource type has no resources or cannot be enumerated, skip it
                continue

        # Print the resources grouped by their type
        for resource_type, data in resources_dict.items():
            print(f"\nType: {data['type_name']} ({resource_type})")
            for resource_name in data['names']:
                print(f"  Name: {resource_name}")

    except Exception as e:
        print(f"Error enumerating resources: {e}")
    finally:
        win32api.FreeLibrary(handle)

def extract_resource(dll_path, resource_type, resource_name, output_path):
    """Extract a specific resource and save it to a file."""
    try:
        handle = win32api.LoadLibraryEx(dll_path, 0, win32con.LOAD_LIBRARY_AS_DATAFILE)
        resource_data = win32api.LoadResource(handle, resource_type, resource_name)
        win32api.FreeLibrary(handle)

        # Save the resource to the output file
        with open(output_path, "wb") as file:
            file.write(resource_data)
        print(f"Extracted: {output_path}")
    except Exception as e:
        print(f"Failed to extract resource {resource_name}: {e}")

def extract_all_resources_of_type(dll_path, resource_type, output_folder):
    """Extract all resources of a specific type into the specified folder."""
    try:
        handle = win32api.LoadLibraryEx(dll_path, 0, win32con.LOAD_LIBRARY_AS_DATAFILE)
        resource_names = win32api.EnumResourceNames(handle, resource_type)
        for resource_name in resource_names:
            output_path = os.path.join(output_folder, f"{resource_name}.bin")
            extract_resource(dll_path, resource_type, resource_name, output_path)
    except Exception as e:
        print(f"Error extracting resources of type {resource_type}: {e}")
    finally:
        win32api.FreeLibrary(handle)

def main():
    parser = argparse.ArgumentParser(description="List and extract resources from a DLL.")
    parser.add_argument("dll_path", type=str, help="Path to the DLL file.")
    parser.add_argument("--list", "-l", action="store_true", help="List resources in the DLL.")
    parser.add_argument("--extract", "-x", action="store_true", help="Extract resources in the DLL.")
    parser.add_argument("--type", "-t", type=str, help="Resource type (name or integer).")
    parser.add_argument("--name", "-n", type=str, help="Resource name or ID.")
    parser.add_argument("--output", "-o", type=str, help="Output file or folder path.")
    args = parser.parse_args()

    if args.list:
        list_resources_in_dll_legacy(args.dll_path)
    elif args.extract and args.type and args.output:
        resource_type = get_resource_type(args.type)
        if args.name:
            extract_resource(args.dll_path, resource_type, args.name, args.output)
        else:
            if not os.path.exists(args.output):
                os.makedirs(args.output)
            extract_all_resources_of_type(args.dll_path, resource_type, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
