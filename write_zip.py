import zipfile
import os.path

def write(matchingfiles, path, filename = "log_files.zip", ):
    if len(matchingfiles) > 0:
        zipname = os.path.join(path, filename)
        zf = zipfile.ZipFile(zipname, mode = 'w')
        try:
            for myfile in matchingfiles:
                zf.write(file[0], arcname = myfile[1])
        finally:
            print 'closing'
            zf.close()

        print "writing zip to - " + zipname
