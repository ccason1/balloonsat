import os, zlib, base64


def main():
    # open--> creats file with name, mode
    f = open("afile.txt", "w+")
    # loop writes to file i times
    for i in range(18):
        f.write("This is a line %d\r\n" % (i + 1))

    f.close()
    # printing the file size
    file_size = os.path.getsize('afile.txt')
    print("file size is:", file_size, "bytes")

def compress_file():
    # method compresses a selected file by compressing actual data in file
    # and writing it to a new "zip" file
    # opens un compressed file
    file1 = open('afile.txt','r')
    # reads and closes file storing contents in 'text'
    text = file1.read()
    file1.close

    # takes the encoded text and stores it into anoher file called "compressed"
    code = base64.b64encode(zlib.compress(text.encode('utf-8'),9))
    code = code.decode('utf-8')
    fz = open('compressed.txt','w')
    fz.write(code)
    fz.close()

    #prints the file size
    zip_size = os.path.getsize('compressed.txt')
    print("compressed file size is:", zip_size, "bytes")


   # afile_zip = zipfile.Zipfile('afile.zip', 'w')
   # afile_zip.write('afilezip.txt', compress_type=zipfile.z)
    #afile_zip.close()
   # zip_size = os.path.getsize('afilezip.zip')
    #print("zip file size is:", zip_size, "bytes") #

if __name__ == "__main__":
    main()
    compress_file()
