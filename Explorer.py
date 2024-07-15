import os
import pickle
import time
import threading

class Explorer:
    def __init__(self):
        self.count = 0
        self.list_of_files_found = []
        self.filename_to_list_of_absolute_paths_mapping = {}
        self.root_folder = "C:\\"
        self.mapping_storage_file = "filename_to_list_of_absolute_paths_mapping.bin"

    def create_filename_absolute_path_mapping(self, root_folder):
        try:
            folders_and_files_inside  = os.listdir(root_folder)
            folders_and_files_inside = [os.path.join(root_folder, folder_or_file_name) for folder_or_file_name in folders_and_files_inside]
        except PermissionError:
            print("No Permission to access this file, PermissionError occured!!!")
            # print("Hello")
            return
        print("Permission present!!!")
        threads_to_execute = []
        for folder_or_file in folders_and_files_inside:
            try:
                is_file = os.path.isfile(folder_or_file)
                if (is_file):
                    file_name = os.path.basename(folder_or_file)
                    if (file_name not in self.filename_to_list_of_absolute_paths_mapping):
                        self.filename_to_list_of_absolute_paths_mapping[file_name.upper()] = [folder_or_file]#folder_or_file is the absolute path
                    else:
                        self.filename_to_list_of_absolute_paths_mapping[file_name.upper()].append(folder_or_file)
                else: #is folder
                    if os.path.isdir(folder_or_file): 
                        my_thread = threading.Thread(target = self.create_filename_absolute_path_mapping, args = (folder_or_file,))
                        # my_thread.start()
                        threads_to_execute.append(my_thread)
                        # self.create_filename_absolute_path_mapping(folder_or_file)
                        # print(folder_or_file)
            except PermissionError:
                continue
            
            while threads_to_execute != []:
                current_thread = threads_to_execute.pop()
                current_thread.start()
            # for thread_to_execute in threads_to_execute:
            #     thread_to_execute.start()


    def write_mapping_to_file(self):
        with open(self.mapping_storage_file, 'wb') as fp:
            pickle.dump(self.filename_to_list_of_absolute_paths_mapping, fp)
            print('mapping saved successfully to file')
    
    def initial_explorer_setup(self):
        set_up_start_time = time.time()
        self.create_filename_absolute_path_mapping(self.root_folder)
        self.write_mapping_to_file()
        set_up_end_time = time.time()
        time_taken_for_set_up = set_up_end_time - set_up_start_time
        print(f"Explorer setup finished!!!\n Time taken = {time_taken_for_set_up} seconds")

    def read_mapping_file(self):
        start_time = time.time()
        with open(self.mapping_storage_file, 'rb') as f:
            data = pickle.load(f)
            print("data loaded")
            # print(data)
        # for file_name in data:
        #     try:
        #         print(f"{file_name} : {data[file_name]}")
        #     except UnicodeEncodeError:
        #         print("UnicodeEncodeError Occured!!!")
        self.filename_to_list_of_absolute_paths_mapping = data
        # print(self.filename_to_list_of_absolute_paths_mapping)
        end_time = time.time()
        time_taken_to_read_file = end_time - start_time
        print(f"Time taken to read file is : {time_taken_to_read_file}")
        return data

    def find_files_quickly(self, file):
        if self.filename_to_list_of_absolute_paths_mapping == {}:
            self.read_mapping_file()
        if file.upper() not in self.filename_to_list_of_absolute_paths_mapping:
            # print("File dosent exist !!!")
            return []
        else:#file exists
            return self.filename_to_list_of_absolute_paths_mapping[file.upper()]
    
    def find_prefix(self, search_file):
        start_time = time.time() 
        if self.filename_to_list_of_absolute_paths_mapping == {}:
            self.read_mapping_file()
        for existing_file in self.filename_to_list_of_absolute_paths_mapping:
            if len(existing_file) < len(search_file):
                continue
            else:
                if existing_file[:len(search_file)] == search_file.upper()[::]:
                    print(self.filename_to_list_of_absolute_paths_mapping[existing_file])
        time_taken_for_prefix_search = time.time() - start_time
        print(f"Time taken for prefix search is : {time_taken_for_prefix_search}")
    
    def find_suffix(self, search_file):
        start_time = time.time() 
        if self.filename_to_list_of_absolute_paths_mapping == {}:
            self.read_mapping_file()
        for existing_file in self.filename_to_list_of_absolute_paths_mapping:
            if len(existing_file) < len(search_file):
                continue
            else:
                if existing_file[len(search_file):] == search_file.upper()[::]:
                    print(self.filename_to_list_of_absolute_paths_mapping[existing_file])
        time_taken_for_suffix_search = time.time() - start_time
        print(f"Time taken for suffix search is : {time_taken_for_suffix_search}")


    def find_file_inside_folder(self, root_folder, file):
        folders_and_files_inside  = os.listdir(root_folder)
        folders_and_files_inside = [os.path.join(root_folder, folder_or_file_name) for folder_or_file_name in folders_and_files_inside]
        
        for folder_or_file in folders_and_files_inside:
            try:
                is_file = os.path.isfile(folder_or_file)
                if (is_file):
                    if os.path.basename(folder_or_file) == file[::]:
                        print("found", folder_or_file)
                        self.count += 1
                        print("count = ", self.count)
                        self.list_of_files_found.append(folder_or_file)
                else: #is folder
                    if os.path.isdir(folder_or_file): 
                        self.find_file_inside_folder(folder_or_file, file)
                        # print(folder_or_file)
            except PermissionError:
                # print(folder_or_file)
                continue

if __name__ == "__main__":
    my_explorer = Explorer()
    my_explorer.initial_explorer_setup()
    # my_explorer.read_mapping_file()
    # data = my_explorer.filename_to_list_of_absolute_paths_mapping
    # print(data)
    # my_explorer.find_suffix(".txt")
    # my_explorer.find_suffix("lite3")
    # paths = my_explorer.find_files_quickly("Main.java")
    # print(paths)
    # for mapping in data:
        # print(data)
    # print(my_explorer.filename_to_list_of_absolute_paths_mapping)
    #added version control git
    