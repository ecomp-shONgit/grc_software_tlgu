#!/usr/bin/python3
# -*- coding: utf-8 -*-

#**************************************************
# 2021 Python3 script to run tlgu (ancient history 
# edition) over PHI7, Prof. Charlotte Schubert Alte 
# Geschichte, Leipzig
#**************************************************

'''
GPLv3 copyrigth
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http:#www.gnu.org/licenses/>.

'''


# TLGU USAGE
#IDT
#./tlgu -r PATHTO/PHI7/INS0010.IDT gINS0010.IDT
#TXT
# Latin: ./tlgu -b -p -v -w -x -y -z -r -W PATHTO/PHI7/INS0040.TXT gINS0040-xxx.TXT
# Greek: ./tlgu -b -p -v -w -x -y -z -W PATHTO/PHI7/INS0040.TXT gINS0040-xxx.TXT


import os, sys, io, shutil, textnorm, time

# THINGS REMEMBERING tlgu, python scripting related
#ausrufe
#"!" "."
#"!2" ".."
#"!3" "..."
#"!4" "...."
#"!5" "....."
#"!6" "......"
#"!7" "......."
#"!8" "........"
#"!9" "........."
# noch mehr
#? Unterpunkt - done
#Schlange macht er nicht über e o - done
#ℎ 	Σ  vor o oder a ist Behauchung [χσυμμαχία καὶ ℎόρ]κ̣ο̣[ς] Ἀ̣[θ]ε̣ν̣α̣[ίον κα]ὶ Ἐγεσταί[ον].    [χσυμμαχία καὶ Σόρ]κ?ο?[ς] Ἀ?[θ]ε?ν?α?[ίον κα]ὶ Ἐγεσταί[ον]. - Behauchung ausgeschrieben - 

thisIDTinfo = []
IDTraw = ""

def delsome( ar ):
    ar[1] = ar[1].replace("\n", "").replace("\x1e", "").replace("\x11","").replace("\x02", "").replace("\x04", "").replace("\x10","").replace("\x1d", "").replace("\x11", "").replace("\x1b", "").replace("\x03", "").replace("\x17", "").replace("\x06", "").replace("\x05", "").replace("\x14", "").replace("\x1f", "").replace("\x1c", "").replace("\x0b", "").replace("\x13", "").replace("\x0e", "").replace("\x07", "").replace("\x16", "").replace("\x01","").replace("\x08","").replace("\x12","").replace("\t","").replace("\x0c","").replace("\x08","").replace("\x10","").replace("\x0f","").replace("\x15","").replace("\x18","").replace("\x19","").replace("\x03", "")
    ar[0] = ar[0].replace("\n","").replace("\x1e", "").replace("\x11","").replace("\x02", "").replace("\x04", "").replace("\x1d", "").replace("\x10","").replace("\x11", "").replace("\x1b", "").replace("\x1f", "").replace("\x03", "").replace("\x06", "").replace("\x05", "").replace("\x17", "").replace("\x14", "").replace("\x1a", "").replace("\x1c", "").replace("\x0b", "").replace("\x13", "").replace("\x0e", "").replace("\x07", "").replace("\x16", "").replace("\x01","").replace("\x08","").replace("\x12","").replace("\t","").replace("\x0c","").replace("\x08","").replace("\x10","").replace("\x0f","").replace("\x15","").replace("\x18","").replace("\x19","")
    return ar

def processIDTtlguoutput(fna, od):
    global thisIDTinfo
    global IDTraw
    thisIDTinfo = []
    with open( fna,'r',encoding='utf-8' ) as f:
            text =  textnorm.normatext( f.read().replace("\u0332", "").replace("\u0305", ""), textnorm.analysisNormalform )
            li = text.split("\x10\x01")
            
            IDTraw = li
            for ll in li:
                ll = ll.strip()
                if(ll == ""):
                    continue
                
                
                lp = ll.split( "\x03" )
                ind = 0
                if(lp[ind] == ""):
                    ind = 1
                spl = "\x08"
                if( not spl in lp[ind] ):
                    spl = "\x11"
                lg = lp[ind].split( spl )
                #print(lg)
                
                if(len(lg) >= 2):
                    u = delsome([lg[len(lg)-2], lg[len(lg)-1]])
                    if( u[0] != "" and u[1] != ""):
                        thisIDTinfo.append( u )
                else:
                    print("e lll: ", ll, lg, lp) 
                                
                        
    if( len(thisIDTinfo) == 0):
        print("Error extract info", li)
        raise ValueError("Some thing went wrong with the split.")
        

def processTLGUoutp( fna, od ):
    
    A = None
    B = None
    C = None
    D = None
    w = None
    v = None
    x = None
    y = None
    z = None
    num = None
    
    count = 1
    lcount = 1
    pcount = 0
    try:
        with open( fna,'r',encoding='utf-8' ) as f:
            text =  textnorm.normatext( f.read().replace("?", "\u0323").replace("\u0332", "").replace("\u0305", ""), textnorm.analysisNormalform )
            li = text.split("\n")
            stacklines = [];
            stackparts = [];
            
            for l in range(len(li)):
                #
                if "" in li[l]:
                    
                    pi = li[l].split("]]")
                    Ao = pi[0].split("[[")[1].replace( "/", "\\" ).strip()
                    Bo = pi[1].split("[[")[1].replace( "/", "\\" ).strip()
                    Co = pi[2].split("[[")[1].replace( "/", "\\" ).strip()
                    Do = pi[3].split("[[")[1].replace( "/", "\\" ).strip()
                    
                    if( A != Ao or B != Bo or C != Co or D != Do ):
                        if( A != None ):
                            #print("Major Ref changed + written", A, B, C, D, thisIDTinfo[pcount][0])
                            print("Major Ref changed + written", A, B, C, D )
                            fnout = od+"/"+str(A)+"_"+str(D)+"_"+str(B)+"_"+str(C)+".xml"
                            #fdout = "<div db='PHI7' type='"+thisIDTinfo[pcount][1]+"' edition='"+thisIDTinfo[pcount][0]+"'>\n"+"\n".join( stackparts )+"\n</div>"
                            fdout = "<div db='PHI7' >\n"+"\n".join( stackparts )+"\n</div>"
                            with open( fnout, 'w', encoding='utf-8') as f_out:
                                f_out.write( fdout )
                            pcount += 1
                            count = 1
                            stackparts = []
                        A = Ao
                        B = Bo 
                        C = Co
                        D = Do
                        
                        
                        
                else:#textline
                    if( li[l] != "" ):
                        
                        po = li[l].split("\t")
                        #if("!3" in po[1]):
                        #    print(po[1])
                        #print(po[0])
                        pi = po[0].split("----")
                        if( len(pi) < 2 ):
                            print("ERROR SOCOND SPLIT", li[l] )
                            
                            #lse = list(li[l])
                            
                            #for f in lse:
                            #    print(f, f.encode("utf-8", "strict")  )
                            
                            if( len(stacklines)-1 >= 0 ):
                                stacklines[len(stacklines)-1] += li[l]
                            continue
                        
                        ref = pi[1].split(".")
                        
                        wo = ref[0].strip().split("__")
                        vo = ref[1].strip().split("__")
                        xo = ref[2].strip().split("__")
                        yo = ref[3].strip().split("__")
                        zo = ref[4].strip().split("__")
                        
                        R = pi[0].split("_")
                        
                        numo = R[13].replace( "/", "\\" )
                    
                        if( len(zo) != 2 ):
                            print("Error",wo, vo, xo, yo, zo, l)
                            if( len(stacklines)-1 >= 0 ):
                                stacklines[len(stacklines)-1] += li[l]
                            continue
                        if( z != None ):
                            if( num != numo ):
                                fdirout = od+"/"+str(A)+"_"+str(D)+"_"+str(B)+"_"+str(C) 
                                if( not os.path.exists( fdirout ) ):
                                    os.mkdir( fdirout ) 
                                #print("thisIDTinfo", thisIDTinfo, len(thisIDTinfo), pcount)
                                fnout = fdirout+"/"+str(num)+".xml"
                                #fdata = textnorm.normatext( "<div type='"+thisIDTinfo[pcount][1]+"' edition='"+thisIDTinfo[pcount][0]+"' lA='"+str(A)+"' lB='"+str(B)+"' lC='"+str(C)+"' lD='"+str(D)+"'>\n<ab lA='"+str(A)+"' lB='"+str(B)+"' lC='"+str(C)+"' lD='"+str(D)+"' lE='"+str(num)+"'>\n"+"</lb>\n".join(stacklines)+"</lb>\n</ab>\n</div>", textnorm.dispnormalform )   
                                fdata = textnorm.normatext( "<div lA='"+str(A)+"' lB='"+str(B)+"' lC='"+str(C)+"' lD='"+str(D)+"'>\n<ab lA='"+str(A)+"' lB='"+str(B)+"' lC='"+str(C)+"' lD='"+str(D)+"' lE='"+str(num)+"'>\n"+"</lb>\n".join(stacklines)+"</lb>\n</ab>\n</div>", textnorm.dispnormalform )                 
                                #write Inscription level
                                with open( fnout, 'w', encoding='utf-8') as f_out:
                                    f_out.write( fdata )
                                
                                stackparts.append(fdata)
                                stacklines = []
                                count += 1
                                lcount = 1
                                stacklines.append( "<lb n="+str(lcount)+" t='"+str(num)+"' p='"+str(count)+"'/>"+po[1]  )
                            else:
                                lcount += 1
                                stacklines.append( "<lb n="+str(lcount)+" t='"+str(num)+"' p='"+str(count)+"'/>"+po[1] )
                                
                        else:
                            print("zo is none: Start process")
                        w = wo
                        v = vo
                        x = xo
                        y = yo
                        z = zo
                        num = numo
                        
    except Exception as e:
        print("!! ", e )
        pass
        #raise ValueError("Some thing went wrong")
        
    
if __name__ == "__main__":
    phipath = "PATHTO/PHI/PHI7"
    phiextdir = "PHI7extract"
    phixmldir = "PHI7XML"
    if( os.path.exists( phixmldir ) ):
        shutil.rmtree( phixmldir )
        shutil.rmtree( phiextdir )
        os.mkdir( phixmldir ) 
        os.mkdir( phiextdir ) 
    else:
        os.mkdir( phixmldir )
        os.mkdir( phiextdir ) 

    lof = sorted( filter( lambda x: os.path.isfile(os.path.join(phipath, x)), os.listdir(phipath) ) )

    for i in range(len(lof)):
    
        n = lof[i]
        print(n)
        if( ".TXT" in n ):
            print("Do extract text to XML: ", phipath+"/"+n)
            os.system( "./tlgu -p -a -b -c -d -v -w -x -y -z "+phipath+"/"+n+" "+phiextdir+"/"+n )
            processTLGUoutp( phiextdir+"/"+n, phixmldir )
        #elif( ".IDT" in n ):
        #    os.system( "./tlgu -r "+phipath+"/"+n+" "+phiextdir+"/"+n )
        #    processIDTtlguoutput( phiextdir+"/"+n, phixmldir )
        else:
            print("Don't ", n)


    
    

#eof
