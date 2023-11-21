import os,sys, requests, re

def download_ts_files(url, output_filename):
    # Initialize variables
    segment_number = 1
    failed_attempts = 0
    failed = False

    # Split URL into segments to separate the changing 7th segment
    segments = url.split("/")
    changing_segment = segments[7]

    # First digit of the changing_segment changes
    pattern = r"\d+"

    print(f"Initiating download of {output_filename}")

    # Open output file in append mode
    with open(output_filename, 'ab') as output_file:
        while True:
            # Modify the URL path for the changing segment
            modified_segment = re.sub(pattern, str(segment_number), changing_segment, count=1)
            segments[7] = modified_segment
            modified_url = "/".join(segments)

            # Download the segment
            try:
                response = requests.get(modified_url, stream=True)
            except requests.exceptions.RequestException as e:
                print(f"Failed to download segment {segment_number}: {e}")
                failed_attempts += 1
                failed = True
                if failed_attempts >= 10:
                    print("Reached maximum failed attempts, stopping download.")
                    break

            # Check for successful download
            if response.status_code != 200:
                print(f"Failed to download segment {segment_number}: HTTP {response.status_code}")
                failed_attempts += 1
                failed = True
                if failed_attempts >= 10:
                    print("Reached maximum failed attempts, stopping download.")
                    break

            if not failed:
                # Write segment to output file
                for chunk in response.iter_content(chunk_size=1024):
                    output_file.write(chunk)

                # Print progress and recurse
                print(f"\rDownloaded segment {segment_number}", end="")
                failed_attempts = 0

            # Modify for next segment
            segment_number += 1

        # Close output file
        output_file.close()


if __name__ == "__main__":
    # Get URL from command line argument or take it as input
    url = sys.argv[1] if len(sys.argv) > 1 else input("Enter the URL of the video: ")

    # Extract output filename from URL
    output_filename = url.split("/")[6]

    # Download TS files and save as MP4
    download_ts_files(url, output_filename)

    # End program execution
    print("Download completed...")
    sys.exit(0)
