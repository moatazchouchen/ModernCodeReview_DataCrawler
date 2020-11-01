from pydriller import RepositoryMining
import re
import json
import os
import pandas as pd


def load_metadata_from_raw_data(data_path,statuses) :
  index_dataframe = pd.DataFrame(columns=["index","ID","status","CreationDate","UpdateDate"])
  for status in statuses : 
    print("loading data for status : ",status)
    for file_name in os.listdir(os.path.join(data_path,status,'data')) : 
      index = int(file_name.split("_")[0])
      changes = json.load(open(os.path.join(data_path,status,'data',file_name)))
      if status == 'merged' : 
        changes=changes[0]
      for local_index,change in enumerate(changes) : 
        try : 
          row = {}
          row["index"] = index + local_index
          row["status"] = status
          row["ID"] = change["id"]
          row["CreationDate"] = change["created"]
          row["UpdateDate"] = change["updated"]
          index_dataframe = index_dataframe.append(row,ignore_index=True)
        except : 
          print(changes)
          break
  #converting dates to datetime 
  index_dataframe["CreationDate"] = pd.to_datetime( index_dataframe["CreationDate"])
  index_dataframe["UpdateDate"] = pd.to_datetime( index_dataframe["UpdateDate"])
  return index_dataframe
  
def preprocess_metadata(metadata) : 
    #removing duplicates
    metadata = metadata.drop_duplicates(subset=['ID'])
    #sorting data according to update date
    sorted_metadata = metadata.sort_values(by=['UpdateDate'])
    return sorted_metadata
def save_metadata(metadata) :
    metadata.to_excel("meta_data.xlsx",index=False)

def load_metadata(path) : 
    return pd.read_excel(os.path.join(path,"meta_data.xlsx"))
    
def extract_commits_data(repo_path,results_path) : 
    #making results path
    os.mkdirs(results_path,exists_ok=True)
    for commit in RepositoryMining(repo_path).traverse_commits() : 
        if ('Change-Id' in commit.msg) :
          id = re.findall("Change-Id: [A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9][A-Za-z0-9]",commit.msg)
          change_id = id[0]
          all_data = []
         
          for modification in commit.modifications : 
            data = {}
            data['changed_methods_count'] = len(modification.changed_methods)
            data['added_lines'] = modification.added
            data["removed_lines"] = modification.removed
            data["loc"] = modification.nloc
            data["complexity"] = modification.complexity
            data["change_type"] = modification.change_type
            data["old_path"] = modification.old_path
            data["new_path"] = modification.new_path 
            file_name = modification.filename 
            if data["old_path"] == None : 
                data["old_path"] = ''
            if data["new_path"] == None : 
                data["new_path"] = ''
                file_path = data["old_path"]
            all_data.append(data)
          json.dump(all_data,open(os.path.join(results_path,id+".json")))


