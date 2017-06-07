
import argparse
import os
import core.cleaning as cl

######################################################
#
# Functions
#
######################################################

######################################################
#
# Main
#
######################################################

if __name__ == "__main__":

    # Argument parser
    parser = argparse.ArgumentParser(description="SFgram - Clean and save Gutenberg data set to XML files.")

    # Argument
    parser.add_argument("--dataset", type=str, help="Gutenberg dataset directory", default=".")
    parser.add_argument("--output", type=str, help="Output dataset directory", default=".")
    args = parser.parse_args()

    # gutenbergSF path
    gutenberg_sf_path = os.path.join(args.dataset, "Gutenberg SF")

    # For each file
    for filename in os.listdir(gutenberg_sf_path):
        # File
        sf_file = os.path.join(gutenberg_sf_path, filename)

        # Cleaner
        cleaner = cl.SFGCleaner()

        # File or directory
        if os.path.isdir(sf_file):
            cleaner = cl.SFGDirectoryCleaner()
        else:
            if os.path.splitext(sf_file)[1] == ".pdf":
                cleaner = cl.SFGPdfCleaner()
            elif os.path.splitext(sf_file)[1] == ".rtf":
                cleaner = cl.SFGRTFCleaner()
            elif os.path.splitext(sf_file)[1] == ".html" or os.path.splitext(sf_file)[1] == ".htm":
                cleaner = cl.SFGHTMLCleaner()
            elif os.path.splitext(sf_file)[1] == ".txt":
                cleaner = cl.SFGFileCleaner()
            elif os.path.splitext(sf_file)[1] == ".lit":
                cleaner = cl.SFGLitCleaner()
            elif os.path.splitext(sf_file)[1] == ".tei":
                cleaner = cl.SFGXmlCleaner()
            else:
                print("WARNING : " + sf_file)
            # end if
        # end if

        # Get cleaned text and info
        text = cleaner(sf_file)
    # end for

# end if