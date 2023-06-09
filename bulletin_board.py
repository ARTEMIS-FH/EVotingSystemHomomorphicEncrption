
import os

def get_all_vote_id():
    
    id_list = []
    file = open("encrypted_vote.txt", "r")
    for x in file:
       id_list.append(x.strip().split(" ")[1])
    return id_list

if __name__ == "__main__":
    
    if not os.path.isfile('encrypted_vote.txt'):
        print("No vote found! The election might haven't started!")
    else:
        id_list = get_all_vote_id()
        print("Election Bulletin Board! Check to see if your vote has been submitted to the system!")
        vote = input("Enter your vote id: ").strip()
        if vote in id_list:
            print("Vote id found! Your vote has been submitted to the system!")
        else:
            print("Vote id failed to find! You might have entered the wrong vote id or your vote hasn't been submitted to the system! Please contact election organizer!")
        print("Program is closing!")