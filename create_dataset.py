
import argparse

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Clean and save Gutenberg data set to XML files.")

    # Argument
    parser.add_argument("--dataset", type=str, help="Gutenberg dataset directory", default=".")
    parser.add_argument("--output", type=str, help="Output dataset directory", default=".")
    args = parser.parse_args()

    # For each file


# end if