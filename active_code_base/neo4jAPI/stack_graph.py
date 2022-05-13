# a useful periodic commit
CALL apoc.periodic.commit(
  "MATCH (n:Realtor_Search_URL) where n.stacked = False 
  WITH n
  ORDER BY n.url ASC
  WITH collect(n) as urls, n as n 
  with urls[0] as tail, n as n
  merge (tail) - [:TO_PROCESS] -> (stack:Stack {UID: apoc.create.uuid(),type: 'realtor_stack', date_created: localdatetime(),  last_id_processed: -1, last_index_processed: -1, in_progress: False})
  set n.stacked = True",
  {limit:1000});
#CALL apoc.nodes.link(urls, 'test_stack_1')
#RETURN urls



match n:(Realtor_Search_URL) where n.processed = false and stacked = False 
with n 

FOR EACH 

from typing import no_type_check_decorator


create a worker id and user
create a node with the worker name 

1 worker per state....__annotations__

hmm.  create stacks per state...  of batch size 100
each 100 is a unit of work to assign a worker to

match n:(Realtor_Search_URL) where n.processed = false and stacked = False



stacks --> stack_uid -> 100 random url's of the state...

def crawl_graph():
    search for 1 node of type
    search for 100 nodes of type realtor url where n.state = state and processed = False
        for each node process:(the hard part)
            set each node to processed = True

            disconnect from to_process


    #find all ancestors and descendents
    MATCH (n:Node2)
    WITH n, [(n)<-[:Child*]-(x) | x] as ancestors,  [(x)<-[:Child*]-(n) | x] as descendants

    #find 1 parent and 1 child
    MATCH (n:Node2)
    WITH n, [(n)<-[:Child]-(x) | x][0] as parent,  [(x)<-[:Child]-(n) | x] as children
    RETURN n, parent, children 
    RETURN n, ancestors, descendants 

    #set state all descendents of root 
    match (n:Realtor_Search_URL) where (n.is_root = True and n.sprouted = True and n.processed = False) return n limit 100
    match n [:IS_STATE_OF] -> (state)
    pull 100 url's at a time by state

    n:Realtor_Search_URL where n.processed = false  
    match n -{'is_state_of'} ->[]

    n:Realtor_Search_URL related to to_process


// Set for all descendants
match (n:Realtor_Search_URL) where (n.is_root = True and n.sprouted = True and n.processed = False) 
match ((n) -[:IS_STATE_OF] -> (state))
with [(x)<-[:IS_CHILD*]-(n) | x] as descendants, state.code as state_name
FOREACH (d IN descendants | SET d.state_code = state_name)
return descendants
    #create or stack??/ or just do it randomly?  