import os
import datetime
import shutil
import stat



def sync_files(sour_folder, dest_folder):

    filenames = [f for f in os.listdir(dest_folder) if os.path.isfile(os.path.join(dest_folder, f))]
    for filename in filenames:
        dest_file = os.path.join(dest_folder, filename)
        os.chmod(dest_file, stat.S_IWRITE)
        os.remove(dest_file)

    filenames = [f for f in os.listdir(sour_folder) if os.path.isfile(os.path.join(sour_folder, f))]
    for filename in filenames:
        print(filename)
        sour_file = os.path.join(sour_folder, filename)
        # print(sour_file)
        dest_file = os.path.join(dest_folder, filename)
        # print(dest_file)
        shutil.copyfile(sour_file, dest_file)
        os.chmod(dest_file, stat.S_IREAD)
    print(str(len(filenames)) + ' files synchronized\n')



def backup_files(sour_folder, sub_folder ='History', with_datefolder=True):

    dest_folder = os.path.join(sour_folder, sub_folder)
    if with_datefolder:
        date_folder = datetime.datetime.today().strftime('%Y%m%d')
        dest_folder = os.path.join(dest_folder, date_folder)
        try:
            os.mkdir(dest_folder)
        except OSError:
            print("Creation of the directory %s failed" % dest_folder)
        else:
            print("Successfully created the directory %s" % dest_folder)
    print('-' * 30)

    filenames = [f for f in os.listdir(sour_folder) if os.path.isfile(os.path.join(sour_folder, f))]
    for filename in filenames:
        print(filename)
        sour_file = os.path.join(sour_folder, filename)
        # print(sour_file)
        dest_file = os.path.join(dest_folder, filename)
        # print(dest_file)
        if os.path.exists(dest_file):
            os.chmod(dest_file, stat.S_IWRITE)
        shutil.copyfile(sour_file, dest_file)
        os.chmod(dest_file, stat.S_IREAD)
    print(str(len(filenames)) + ' files backuped\n')



if __name__ == '__main__':

    sour_folder2022 = r'C:\Users\zjin6\Documents\1 WORK\1 TVM Data Analysis\2 Weekly Report\2022 Weekly Report'
    dest_folder2022 = r"C:\Users\zjin6\OneDrive - azureford\0 Weekly Status Report\2022 TVM Weekly Report"
    sour_folder_MP = r"C:\Users\zjin6\Documents\1 WORK\3 Weekly MP Meeting"
    dest_folder_MP = r"C:\Users\zjin6\OneDrive - azureford\3 Weekly MP Meeting"
    sync_files(sour_folder2022, dest_folder2022)
    sync_files(sour_folder_MP, dest_folder_MP)

    sour_folder2022_C = r'C:\Users\zjin6\Documents\1 WORK\1 TVM Data Analysis\2 Weekly Report\2022 Weekly Report'
    sour_folder2022_W = r"C:\Users\zjin6\OneDrive - azureford\0 Weekly Status Report\2022 TVM Weekly Report"
    sour_folder_MP_azure = r"C:\Users\zjin6\OneDrive - azureford\3 Weekly MP Meeting"
    backup_files(sour_folder2022_C)
    backup_files(sour_folder2022_W)
    backup_files(sour_folder_MP_azure)

    print('Mission Completed.')   
else:
    print('module loaded ... ' + __name__ + '\n')
    # print('function ... sync_files(), backup_files')

    
    
    
    
    


















