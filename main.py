import argparse
import csv
import logging
import pathlib
import re


# keys we want to access in the csv file
FNAME_COL = "Child's First Name"
LNAME_COL = "Child's Last Name"

# image file extension
IMG_EXT = ".jpg"

# a regular expression to match the student photo name where it is first name and last name separated by an underscore,
# and ends with the image extension
STUDENT_PHOTO_RE = re.compile(r"^(?P<fname>\w+)_(?P<lname>\w+)$")


def create_student_dir(student: dict, source_dir: pathlib.Path, dryrun: bool) -> None:
    """
    Create a directory for a student

    :param student: dictionary containing the student information
    :param source_dir: the source directory
    :param dryrun: perform a dry run
    """
    # create the student directory
    student_dir = source_dir / f"{student[FNAME_COL]}_{student[LNAME_COL]}"
    if not student_dir.exists():
        if not dryrun:
            student_dir.mkdir()
        logging.info(f"Created directory: {student_dir}")
    else:
        logging.warning(f"Directory already exists - skipping: {student_dir}")


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Photo Organizer - Organize photos by student")

    # add a required argument to read in a csv file
    parser.add_argument("csv_file", help="The CSV file containing the student information")

    # add a required argument to specify the source directory
    parser.add_argument("source_dir", help="The source directory to read photos from")

    # add an optional boolean argument to performa dryrun that defaults to False
    parser.add_argument("--dryrun", help="Perform a dry run", action="store_true")

    # parse the arguments
    args = parser.parse_args()

    # ensure the csv file exists
    csv_path = pathlib.Path(args.csv_file)
    if not csv_path.exists():
        logging.error(f"File not found: {args.csv_file}")
        return

    # ensure the source directory exists and is a directory
    source_dir = pathlib.Path(args.source_dir)
    if not source_dir.exists() or not source_dir.is_dir():
        logging.error(f"Directory not found: {args.source_dir}")
        return

    if args.dryrun:
        logging.warning("Dry run enabled - no changes to the file system will occur!")

    # read the csv file - the first line contains the headers
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # create a directory for each student
            create_student_dir(row, source_dir, args.dryrun)

    # find all photos in the source directory using the pathlib module, sorted by creation time
    photos = sorted(source_dir.glob(f"*{IMG_EXT}"), key=lambda x: x.stat().st_ctime)
    student_dir = None
    for photo in photos:
        # the list of photos will contains 1 image that is named after the student first name and last name, and every
        #  following photo will be moved to the student directory until we hit the next photo named after the student

        # check if the photo name matches the regular expression
        match = STUDENT_PHOTO_RE.match(photo.stem)
        if match:
            # create the student directory
            student_dir = source_dir / pathlib.Path(match.group("fname") + "_" + match.group("lname"))
            logging.info("Processing student: " + student_dir.name)
            if not args.dryrun:
                if not student_dir.exists() or not student_dir.is_dir():
                    logging.warning(f"Student directory not found: {student_dir}")
                    student_dir = None
            continue  # we skip the photo that matches the student name
        else:
            # move the photo to the student directory
            if not args.dryrun:
                if student_dir:
                    photo.rename(student_dir / photo.name)
                    logging.info(f"Moved photo: {photo} to {student_dir}")
                else:
                    logging.warning(f"Photo not moved - no student directory found: {photo}")
            else:
                logging.info(f"Would have moved photo: {photo} to {student_dir}")
    logging.info("Photo organization complete!")


if __name__ == "__main__":
    main()
