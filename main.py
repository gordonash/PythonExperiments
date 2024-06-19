def main():
    try:
        booklist=[]
        print("hello wold")
        infile=open("thebooklist","r")
        line=infile.readline
        while line:
            booklist.append(line.rstrip("\n").split(","))
            line=infile.readline()
        infile.close
    except:
        print("error")
        
    choice=0
    while choice !=4:
        print("1)")
        choice=int(input())
        if choice==1:
            print("Adding")

    outfile=open("thebooklist.txt","w")
    for book in booklist:
        outfile.write(",".join(book)+"\n")
        
    outfile.close
    
    
    
    
    
if __name__=="__main__":
    main()