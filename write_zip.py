import zipfile
import os.path
""" Archive the selected files by the user into a zip file """
def write(matchingfiles, path, filename = "log_files.zip", ):
    # if there is more than 1 file
    if len(matchingfiles) > 0:
        zipname = os.path.join(path, filename)
        zf = zipfile.ZipFile(zipname, mode = 'w')
        try:
            # write each file into the zip file
            for myfile in matchingfiles:
                zf.write(file[0], arcname = myfile[1])
        finally:
            zf.close()

        print "writing zip to - " + zipname
