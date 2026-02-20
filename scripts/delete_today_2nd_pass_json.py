import os
import glob
import datetime

def main():
    target_dir = os.path.join("json", "2nd_pass_json")
    if not os.path.exists(target_dir):
        print(f"Directory not found: {target_dir}")
        return

    today = datetime.date.today()
    print(f"Deleting files in {target_dir} modified on {today}...")

    deleted_count = 0
    files = glob.glob(os.path.join(target_dir, "*.json"))

    for file_path in files:
        try:
            mtime = os.path.getmtime(file_path)
            file_date = datetime.date.fromtimestamp(mtime)

            if file_date == today:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
                deleted_count += 1
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Total files deleted: {deleted_count}")

if __name__ == "__main__":
    main()
