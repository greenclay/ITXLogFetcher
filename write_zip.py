import zipfile
import os.path


def write(matchingfiles, path, filename = "log_files.zip", ):
    if len(matchingfiles) > 0:
        zipname = os.path.join(path, filename)
        zf = zipfile.ZipFile(zipname, mode = 'w')
        try:
            for file in matchingfiles:
                zf.write(file[0], arcname = file[1])
        finally:
            print 'closing'
            zf.close()

        print "writing zip to - " + zipname
