import os
if __name__=="__main__":
    
    satie=[
        #-----------------------------------------
           ["solO2d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #-----------------------------------------
           ["reO2d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #-----------------------------------------
           ["solO2d1"],
           ["siO2d2","reO3d2","faDO3d2"],
        #-----------------------------------------
           ["reO2d1"],
           ["laO2d2","doDO3d2","faDO3d2"],
        #-----------------------------------------
           ["solO2d1"],
           ["siO2d1","reO3d1","faDO3d1","faDO4d1"],
           ["siO2d1","reO3d1","faDO3d1","laO4d1"],
        #-----------------------------------------
           ["reO2d1","solO4d1"],
           ["laO2d1","doDO3d1","faDO3d1","faDO4d1"],
           ["laO2d1","doDO3d1","faDO3d1","doDO4d1"],
        #-----------------------------------------
           ["solO2d1","siO3d1"],
           ["siO2d1","reO3d1","faDO3d1","doDO4d1"],
           ["siO2d1","reO3d1","faDO3d1","reO4d1"],
           ["laO3d2","solO2d2"]
        #-----------------------------------------
          ]
    # lecture
    for notes in satie:
        notename=''
        for note  in notes:
            notename+=note
        notenamefile=notename+".wav"
        print(notenamefile)
        os.system("mplayer "+notenamefile+" > /dev/null 2>&1")    
