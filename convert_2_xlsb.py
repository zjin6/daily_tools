# Created by: Ross Gibson
import win32com.client as win32
import os
import functools
import datetime


# decorator for checking time comsumption
def print_runtime(func):
    """Print run time for running func."""
    @functools.wraps(func)
    def wrapper(*arg, **kwarg):
        start = datetime.datetime.now()
        result = func(*arg, **kwarg)
        end = datetime.datetime.now()
        print('\n' + 'runtime = ' + str(end - start).split('.')[0])
        return result   
    return wrapper


# define original formats to convert to .xlsb
original_formats = ['.xls', '.xlsx', '.xlsm', '.csv']


def getFiles(directory):
    """Given a directory, will return list of all files in given directory."""
    print('search all files in this directory:')
    fileList = []  # place holder used for accumulation
    
    if directory[-1] != '\\':  # check if path doesn't end with a back slash
        directory = directory + '\\'  # add backslash to path
    for item in os.scandir(directory):  # loop through each item
        if item.is_file():  # check if item is a file
            print('find ... ', item)
            fileList.append(directory + item.name)  # append path and file name to accumulator list
    return fileList  # return accumulated list


def convertFiles(fileList):
    """Given a list of file paths, will save .xls, .xlsx, .xlsm, or .csv files as .xlsb in same directory."""    
    print('replace ', original_formats, ' to .xlsb')
    
    for file in fileList:  # loop through each file in provided list
        if os.path.splitext(file)[1] in original_formats:  # check if excel or csv file
            tgtPath = os.path.splitext(file)[0] + '.xlsb'  # sets target path as .xlsb file extension
            xlApp = win32.Dispatch('Excel.Application')  # create Excel object
            xlApp.Visible = True  # unhide Excel window
            xlApp.ScreenUpdating = True  # update Excel window (no window flashes)
            xlApp.DisplayAlerts = True  # display alerts like updating links
            try:
                wb = xlApp.Workbooks.Open(Filename=file, ReadOnly=True)  # try opening the file in read-only mode
            except:
                print(f'Could not open {file}')  # print file if cannot be opened
                continue
            wb.SaveAs(Filename=tgtPath, FileFormat=50)  # save file as xlsb file format
            wb.Close(False)  # closes Excel workbook without saving
            xlApp.Quit()  # kill Excel process
            print(f'saved ... {tgtPath}')  # print confirmation


@print_runtime
def get_convert(directory):
    """Given a windows formatted folder path, will convert all .xls, .xlsx, .xlsm, and .csv files in that directory to .xlsb format."""
    fileList = getFiles(directory)  # get list of files in provided directory
    convertFiles(fileList)  # convert Excel/CSV files in file list



directory = input('input directory: ')
get_convert(directory)













    
    
