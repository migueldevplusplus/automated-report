from pathlib import Path
import zipfile


def create_report_zip(
    output_dir: Path,
    excel_data_path: Path,
    excel_report_path: Path,
    zip_path: Path,
    compression: int = zipfile.ZIP_DEFLATED
) -> Path:
    """
    Creates a ZIP archive containing the two main Excel reports:
    - Weekly_Data.xlsx (processed data and KPIs)
    - Weekly_Report.xlsx (the second report, if it exists)

    Args:
        output_dir: Output directory (used for optional cleanup of old zip files)
        excel_data_path: Full path to Weekly_Data.xlsx
        excel_report_path: Full path to Weekly_Report.xlsx
        zip_path: Path where the .zip file will be created
        compression: Compression method (default: ZIP_DEFLATED)

    Returns:
        Path: Path to the created ZIP file
    """


    # Optional: remove previous Weekly_Sales_Report_*.zip files to prevent accumulation
    for old_zip in output_dir.glob("Weekly_Sales_Report_*.zip"):
        try:
            old_zip.unlink()
            print(f"Deleted previous ZIP: {old_zip.name}")
        except Exception:
            pass  # silently skip if deletion fails

    files_to_zip = [
        excel_data_path,      # Weekly_Data.xlsx - should always exist (just created)
        excel_report_path     # Weekly_Report.xlsx - may or may not exist
    ]

    added_count = 0

    with zipfile.ZipFile(zip_path, 'w', compression=compression) as zipf:
        for file_path in files_to_zip:
            if file_path.exists():
                arcname = file_path.name
                zipf.write(file_path, arcname)
                print(f"Added to ZIP: {arcname}")
                added_count += 1
            else:
                print(f"Warning: File not found, skipped → {file_path.name}")

    if added_count == 0:
        print("WARNING: ZIP file created but contains NO files!")
    elif added_count == 1:
        print(f"ZIP created successfully: {zip_path.name} (only 1 file included)")
    else:
        print(f"ZIP created successfully: {zip_path.name} ({added_count} files included)")

    return zip_path
