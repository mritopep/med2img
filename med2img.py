import  os
import  sys
import  argparse

from    med2img.util       import *
from    argparse            import RawTextHelpFormatter
from    argparse            import ArgumentParser
from    pfmisc._colors      import Colors
import  pudb


str_version = "2.2.10"
str_desc    = Colors.CYAN + """
                        _  _____  _
                       | |/ __  \(_)
     _ __ ___   ___  __| |`' / /' _ _ __ ___   __ _  __ _  ___
    | '_ ` _ \ / _ \/ _` |  / /  | | '_ ` _ \ / _` |/ _` |/ _ \\
    | | | | | |  __/ (_| |./ /___| | | | | | | (_| | (_| |  __/
    |_| |_| |_|\___|\__,_|\_____/|_|_| |_| |_|\__,_|\__, |\___|
                                                 __/ |
                                                |___/
                        med(ical image)2image
            Converts typical medical image formats to jpg/png
                    -- version """ + \
           Colors.YELLOW + str_version + Colors.CYAN + """ --
    'med2image' converts image files from standard medical formats
    such as DICOM and NIfTI to more web-friendly formats such as
    png and jpg.
""" + Colors.NO_COLOUR


def synopsis(ab_shortOnly=False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis = '''
    NAME
	    med2image.py - convert medical images to jpg/png/etc.
    SYNOPSIS
            %s                                       \\
                    [-i|--input <inputFile>]                \\
                    [--inputFileSubStr <substr>]            \\
                    [-I|--inputDir <inputDir>]              \\
                    [-d|--outputDir <outputDir>]            \\
                     -o|--output <outputFileStem>           \\
                    [-t|--outputFileType <outputFileType>]  \\
                    [-s|--sliceToConvert <sliceToConvert>]  \\
                    [--convertOnlySingleDICOM]              \\
                    [-f|--frameToConvert <frameToConvert>]  \\
                    [--showSlices]                          \\
                    [--func <functionName>]                 \\
                    [--reslice]                             \\
                    [-x|--man]                              \\
                    [-y|--synopsis]
    BRIEF EXAMPLE
	    med2image.py -i slice.dcm -o slice.jpg
    ''' % scriptName

    description = '''
    DESCRIPTION
        `%s' converts input medical image formatted data to a more
        display friendly format, such as jpg or png.
        Currently understands NIfTI and DICOM input formats.
    ARGS
        [-i|--inputFile <inputFile>]
        Input file to convert. Typically a DICOM file or a nifti volume.
        [--inputFileSubStr <substr>]
        As a convenience, the input file can be determined via a substring
        search of all the files in the <inputDir> using this flag. The first
        filename hit that contains the <substr> will be assigned the
        <inputFile>.
        This flag is useful is input names are long and cumbersome, but
        a short substring search would identify the file. For example, an
        input file of
           0043-1.3.12.2.1107.5.2.19.45152.2013030808110149471485951.dcm
        can be specified using ``--inputFileSubStr 0043-``
        [-I|--inputDir <inputDir>]
        If specified, a directory containing the <inputFile>. In this case
        <inputFile> should be specified as relative to <inputDir>.
        [-d|--outputDir <outputDir>]
        The directory to contain the converted output image files.
        -o|--outputFileStem <outputFileStem>
        The output file stem to store conversion. If this is specified
        with an extension, this extension will be used to specify the
        output file type.
        SPECIAL CASES:
        For DICOM data, the <outputFileStem> can be set to the value of
        an internal DICOM tag. The tag is specified by preceding the tag
        name with a percent character '%%', so
            -o %%ProtocolName
        will use the DICOM 'ProtocolName' to name the output file. Note
        that special characters (like spaces) in the DICOM value are
        replaced by underscores '_'.
        Multiple tags can be specified, for example
            -o %%PatientName%%PatientID%%ProtocolName
        and the output filename will have each DICOM tag string as
        specified in order, connected with dashes.
        [--convertOnlySingleDICOM]
        If specified, will only convert the single DICOM specified by the
        '--inputFile' flag. This is useful for the case when an input
        directory has many DICOMS but you specifially only want to convert
        the named file. By default the script assumes that multiple DICOMS
        should be converted en mass otherwise.
        [-t|--outputFileType <outputFileType>]
        The output file type. If different to <outputFileStem> extension,
        will override extension in favour of <outputFileType>.
        [-s|--sliceToConvert <sliceToConvert>]
        In the case of volume files, the slice (z) index to convert. Ignored
        for 2D input data. If a '-1' is sent, then convert *all* the slices.
        If an 'm' is specified, only convert the middle slice in an input
        volume.
        [-f|--frameToConvert <sliceToConvert>]
        In the case of 4D volume files, the volume (V) containing the
        slice (z) index to convert. Ignored for 3D input data. If a '-1' is
        sent, then convert *all* the frames. If an 'm' is specified, only
        convert the middle frame in the 4D input stack.
        [--showSlices]
        If specified, render/show image slices as they are created.
        [--func <functionName>]
        Apply the specified transformation function before saving. Currently
        support functions:
            * invertIntensities
              Inverts the contrast intensity of the source image.
        [--reslice]
        For 3D data only. Assuming [i,j,k] coordinates, the default is to save
        along the 'k' direction. By passing a --reslice image data in the 'i' and
        'j' directions are also saved. Furthermore, the <outputDir> is subdivided into
        'slice' (k), 'row' (i), and 'col' (j) subdirectories.
        [-x|--man]
        Show full help.
        [-y|--synopsis]
        Show brief help.
    EXAMPLES
    NIfTI
    o Convert each slice in a NIfTI volume 'vol.nii' to a jpg called
      'image-sliceXXX.jpg' and store results in a directory called 'out':
    		med2image -i vol.nii -d out -o image.jpg -s -1
    o Convert only the middle slice in an input volume and store in current
      directory:
    		med2image -i vol.nii -o image.jpg -s m
    o Convert a specific slice, i.e. slice 20
    		med2image -i vol.nii -o image.jpg -s 20
    DICOM
    o Simply convert a DICOM file called 'slice.dcm' to a jpg called 'slice.jpg':
    		med2image -i slice.dcm -o slice.jpg
    o Convert all DICOMs in a directory. Note that is assumes all DICOM files
      in the directory containing the passed file belong to the same series.
      Conversion will fail if multiple series are interspersed in the same dir.
            med2image -i slice.dcm -o slice.jpg -s -1
    GITHUB
        o See https://github.com/FNNDSC/med2image for more help and source.
    ''' % (scriptName)
    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description


#define script arguments

parser  = ArgumentParser(description = str_desc, formatter_class = RawTextHelpFormatter)

parser.add_argument("-i", "--inputFile",
                    help    = "input file",
                    dest    = 'inputFile',
                    default = '')
parser.add_argument("--inputFileSubStr",
                    help    = "input file substring",
                    dest    = 'inputFileSubStr',
                    default = '')
parser.add_argument("-I", "--inputDir",
                    help    = "input directory",
                    dest    = 'inputDir',
                    default = '')
parser.add_argument("-o", "--outputFileStem",
                    help    = "output file",
                    default = "output.jpg",
                    dest    = 'outputFileStem')
parser.add_argument("-d", "--outputDir",
                    help    = "output image directory",
                    dest    = 'outputDir',
                    default = '.')
parser.add_argument("-t", "--outputFileType",
                    help    = "output image type",
                    dest    = 'outputFileType',
                    default = '')
parser.add_argument("--convertOnlySingleDICOM",
                    help    = "if specified, only convert the specific input DICOM",
                    dest    = 'convertOnlySingleDICOM',
                    action  = 'store_true',
                    default = False)
parser.add_argument("-s", "--sliceToConvert",
                    help="slice to convert (for 3D data)",
                    dest='sliceToConvert',
                    default='-1')
parser.add_argument("-f", "--frameToConvert",
                    help    = "frame to convert (for 4D data)",
                    dest    = 'frameToConvert',
                    default = '-1')
parser.add_argument("--printElapsedTime",
                    help    = "print program run time",
                    dest    = 'printElapsedTime',
                    action  = 'store_true',
                    default = False)
parser.add_argument('-r', '--reslice',
                    help    = "save images along i,j,k directions -- 3D input only",
                    dest    = 'reslice',
                    action  = 'store_true',
                    default = False)
parser.add_argument('--showSlices',
                    help    = "show slices that are converted",
                    dest    = 'showSlices',
                    action  = 'store_true',
                    default = False)
parser.add_argument('--func',
                    help    = "apply transformation function before saving",
                    dest    = 'func',
                    default = "")
parser.add_argument("-x", "--man",
                    help    = "man",
                    dest    = 'man',
                    action  = 'store_true',
                    default = False)
parser.add_argument("-y", "--synopsis",
                    help    = "short synopsis",
                    dest    = 'synopsis',
                    action  = 'store_true',
                    default = False)
parser.add_argument('-v', '--version',
                    help    = 'if specified, print version number',
                    dest    = 'b_version',
                    action  = 'store_true',
                    default = False)


# parse passed arguments
args = parser.parse_args()

# Do some minor CLI checks
if args.b_version:
    print("Version: %s" % str_version)
    sys.exit(1)

if args.man or args.synopsis:
    print(str_desc)
    if args.man:
        str_help = synopsis(False)
    else:
        str_help = synopsis(True)
    print(str_help)
    sys.exit(1)


def convert(input_file, output_folder):
    args.inputFile = input_file
    args.outputFileStem = output_folder
    imgConverter = object_factoryCreate(args).C_convert
    imgConverter.tic()
    imgConverter.run()
    print("Elapsed time = %f seconds" % imgConverter.toc())


if __name__ == "__main__":
    convert("./sample/filtered_adni_11/002_S_4262_7/mri.nii", "./outputs/y.png")