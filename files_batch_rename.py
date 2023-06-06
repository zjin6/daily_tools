import glob, os


# rename files with specified suffix in a folder
def batch_rename(source_folder, suffix='*'):
    source_paths = source_folder + '\\*.' + suffix
    print('Target: .' + suffix)
    path_list = glob.glob(source_paths)
    file_qty = len(path_list)
    # print(path_list)
    
    for old_path in path_list:
        file_num = old_path.split()[-1].split('.')[0]
        file_name = old_path.split('\\')[-1]
        # print(file_name)
        
        if file_num.isnumeric():
            if len(file_num) == 1:
                file_num = '00' + file_num
            elif len(file_num) == 2:
                file_num = '0' + file_num
            else:
                file_num = '' + file_num
        else:
            file_num = '000'
        # print(file_num)           
        
        new_path = source_folder + '\\' + file_num + ' ' + file_name
        # print(new_path)
        os.rename(old_path, new_path)
    print('Batch rename done ... ' + str(file_qty) + ' files.')
  



def get_allfolders(source_folder): 
    allfolders = []
    
    for root, directories, files in os.walk(source_folder):
       for directory in directories:
          allfolders.append(os.path.join(root, directory))
    
    print('get folders:')
    for folder in allfolders:
        print(folder)
        
    return allfolders




if __name__ == '__main__':
    path = input('Folder: ')
    allfolders = get_allfolders(path)
    for folder in allfolders:
        batch_rename(folder)

