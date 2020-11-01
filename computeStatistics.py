import pandas as pd 
import os
import json 

class DirectGraph : 
  def __init__(self) :
    self.graph_data = {}
    
  def update_graph(self,EdgeList) : 
    for edge in edgeList : 
            if edge[0] not in self.graph_data : 
                self.graph_data[edge[0]] = {edge[1] : 0}
            else : 
                if not edge[1] in self.graph_data[edge[0]] : 
                    self.graph_data[edge[0]][edge[1]] = 0 
            graph_data[edge[0]][edge[1]] +=1 
  
class ReviewGraph(DirectGraph) : 
    def __init__(self) : 
        self.__init__()

class CommentsGraph(DirectGraph) : 
    def __init__(self) : 
        self.__init__()

class VotingGraph(DirectGraph) : 
    def __init__(self) : 
        self.__init__()
    
    def update(self,edgeList) : 
        for edge in edgeList : 
            if edge[0] not in self.graph_data : 
                self.graph_data[edge[0]] = {edge[1] : {"-2" : 0, "-1" : 0 , "+1" : 0 , "+2" : 0 }}
            else :
                if not edge[1] in self.graph_data[edge[0]] : 
                    self.graph_data[edge[0]][edge[1]] = {"-2" : 0, "-1" : 0 , "+1" : 0 , "+2" : 0 } 
            self.graph_data[edge[0]][edge[1]][edge[2]] += 1 

class PersonsChangesGraph(DirectGraph) : 
    def __init__(self) : 
        self.__init__()
    def update_graph(self,EdgeList) : 
         for edge in edgeList : 
            if edge[0] not in self.graph_data : 
                self.graph_data[edge[0]] = {'Own' : [] , 'Review' : [] }
            else :
                self.graph_data[edge[0]][edge[1]].append(edge[2])

class ChangeStatistics: 
  def __init__(self,change,files_path) : 
  
    self.change_id = change['change_id']
    self.full_id = change['id']
    self.branch = change["branch"] 
    self.project = change["project"]
    self.messages = change["messages"]
    
    
    if  not change['owner'] : 
      self.authorAccountId = ''
    else : 
      self.authorAccountId = change['owner']['_account_id'] 
    
    
    self.currentRevisionsNumber = 0 
    if 'revisions' in change.keys() :
      self.currentRevisionsNumber = len(change['revisions'].keys())
    
    
    
    
    #compute comments metrics 
    self.total_inline_comments = 0 
    if 'total_comment_count' in change : 
        self.total_inline_comments = change['total_comment_count']
    self.unsolved_comments = 0 
    if 'unresolved_comment_count' in change : 
        self.unsolved_comments = change['unresolved_comment_count']
        
    #compute product metrics 
    self.files_data = self.read_files_data(path)
    self.AddedLines = int(self.change['insertions'])
    self.DeletedLines = int(self.change_data['deletions'])
    self.ComputeFilesMetrics()
    
 
  def read_files_data(self,path) : 
    return json.load(open(os.path.join(path,self.project,self.change_id+".json")))
   
  def TotalChrun(self) : 
    return self.AddedLines - self.DeletedLines
    
  def ComputeFilesMetrics(self) : 
    self.files_count = len(self.files_data)
    self.total_complexity = 0
    self.total_size_before = 0 
    self.total_size_after = 0 
    self.total_modified_methods = 0 
    
    self.added_files_number = 0
    self.deleted_files_number = 0 
    self.renamed_files_number=0 
    self.modified_files_number = 0 
    
    for file_data in self.files_data : 
        self.total_complexity += float(file_data["complexity"])
        self.total_size_after += int(file_data["loc"])
        self.total_modifed_methods += int(file_data['changed_methods_count'])
        if file_data["change_type"] == "Added" : 
            self.added_files_number +=1 
        if file_data["change_type"] == "Deleted" : 
            self.deleted_files_number +=1
        if file_data["change_type"] == "Renamed" :
            self.renamed_files_number += 1 
        if file_data["change_type"] == "Modified" :
            self.modified_files_number +=1 
        
    self.total_size_before =  self.total_size_after - self.AddedLines + self.DeletedLines
    