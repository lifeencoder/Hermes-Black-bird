import gdrive_fsspec

try:
    fs = gdrive_fsspec.GoogleDriveFileSystem(token="cache")
    print("GoogleDriveFileSystem connected!")
    files = fs.ls("/")
    print("Drive root files:", files)
    try:
        models = fs.ls("/hf_models")
        print("/hf_models:", models)
    except Exception as e:
        print("No /hf_models:", e)
except Exception as e:
    print("Error connecting to drive:", e)
