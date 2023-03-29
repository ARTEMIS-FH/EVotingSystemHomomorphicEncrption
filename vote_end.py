

def end():
   
    file = open("vote_status.txt", "w")
    file.write("1")
    file.close()
    print("Voting process has been ended!")

if __name__ == "__main__":
    end()