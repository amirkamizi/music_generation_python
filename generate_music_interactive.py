print("Hello! Welcome to Music Generation Assistant.")
end_file_name = input("Please choose a name for the final file\n")
print("preparing the file ...")
import re
f = open(end_file_name+".csv","a")
#write the header of file
current_layer='1'
wanna_continue = 1
f.write(
    "0, 0, Header, 1, 4, 960 \n"
    )
while wanna_continue:  
    f.write(
    current_layer+", 0, Start_track \n"
    +current_layer+", 0, Tempo, 500000 \n"
        )
    #write the music
    current_time = 0
    print("loading the music basics")
    #initialize the basics of the Music
    #C C# D D# E F F# G G# A A# B
    music_notes = [0,1,2,3,4,5,6,7,8,9,10,11]
    major_progression = [0,2,4,5,7,9,11,12]
    harmonic_minor_progression = [0,2,3,5,7,8,11,12]
    melodic_minor_progression = [0,2,3,5,7,9,11,12]
    types = []
    types.append(major_progression)
    types.append(harmonic_minor_progression)
    types.append(melodic_minor_progression)
    #to get the scale notes of major,minor of a note
    
    # =============================================================================
    # #choose your note
    # =============================================================================
    print("0:C 1:C# 2:D 3:D# 4:E 5:F 6:F# 7:G 8:G# 9:A 10:A# 11:B")
    user_note = input("Please choose the number of the key note\n")
    note=music_notes[int(user_note)]
    # =============================================================================
    # #choose your type
    # =============================================================================
    #0 major 1 harmonic minor 2 melodic minor
    print("0:major 1:harmonic minor 2:melodic minor")
    user_type = input("Please choose the number of the type of your key\n")
    my_type = int(user_type)
    print("loading the scale for this key ...")
    note_scale = []
    for i in range(8):
        note_scale.append((types[my_type][i]+note))
    
    print("loading the chords on each note of this key ...")
    #chords made on the notes of this
    #minor chord is 0 3 7
    #major chord i 0 4 7
    #dim Chord is 0 3 6
    chord_notes=[]
    if my_type==0:
        #major
        for j in range(0,8):
            if j == 0 or j ==3 or j==4:
                #major chords
                chord_notes.append([note_scale[j] + 0,note_scale[j] + 4,note_scale[j] + 7])
            elif j==1 or j==2 or j==5:
                #minor chords
                chord_notes.append([note_scale[j] + 0,note_scale[j] + 3,note_scale[j] + 7])
            elif j==6:
                #dim chords
                chord_notes.append([note_scale[j] + 0,note_scale[j] + 3,note_scale[j] + 6])
    elif my_type==1 or my_type==2:
        #minor
        for j in range(0,8):
            if j == 0 or j ==3 or j==4:
                #minor chords
                chord_notes.append([note_scale[j] + 0,note_scale[j] + 3,note_scale[j] + 7])
            elif j==6 or j==2 or j==5:
                #major chords
                chord_notes.append([note_scale[j] + 0,note_scale[j] + 4,note_scale[j] + 7])
            elif j==1:
                #dim chords
                chord_notes.append([note_scale[j] + 0,note_scale[j] + 3,note_scale[j] + 6])
        
    # =============================================================================
    # #choose your chord progression
    # =============================================================================
    user_chord_progression = input("Please write your chord progression seperated by comma\nExample:1,4,5,1\n")
    my_chord_progression = re.split(",",user_chord_progression)
    my_chord_progression = [int(n) for n in my_chord_progression]
    #my_chord_progression=[1,4,5,1]    
    
    # =============================================================================
    # #choose a pattern
    # #have a pattern(later you can generate them)
    # =============================================================================
    user_pattern = input("Please write your rhythm pattern seperated by comma (write 0 for silence) \nExample:1,3,2,3\n")
    pattern_rhythem = re.split(",",user_pattern)
    pattern_rhythem = [int(n) for n in pattern_rhythem]
    #pattern_rhythem = [1,3,2,3,2,3,1,2]
    user_pattern_repetition= input("Please write how many times each pattern should be repeated in a chord?(default is 4)\n")
    pattern_repetition = int(user_pattern_repetition)
    #choose note duration
    note_duration = input("How long is each note?\n1:quarter note(very short)\n2:half note(short)\n3:dotted half note(almost long)\n4:whole note(long)\n")
    note_duration = int(note_duration)
    user_octav = input("And finally choose the octave.\n")
    user_octav = int(user_octav)
    # =============================================================================
    # some notes:
    # 4 below means it reapeats the pattern 4 times
    # you can change that if you want
    # =============================================================================
    print("making the music ready ... ")
    final_music_notes=[]
    for y in range(len(my_chord_progression)):
        for b in range(pattern_repetition):
            for z in range(len(pattern_rhythem)):
                if pattern_rhythem[z] == 0:
                    final_music_notes.append(127)
                else:
                    final_music_notes.append(chord_notes[my_chord_progression[y]-1][pattern_rhythem[z]-1])
    
    # =============================================================================
    # if you want shorter or longer notes change the 48 to more or less:
    # make sure it's dividable by 24
    # =============================================================================
    for x in final_music_notes:
        if x != 127:
            f.write(current_layer+", "+ str(current_time) + ", Note_on_c, 0, "+str(x+(user_octav*12)+12)+", 127 \n")
        current_time = current_time + (480 * note_duration)
        if x != 127:
            f.write(current_layer+", "+ str(current_time) + ", Note_off_c, 0, "+str(x+(user_octav*12)+12)+", 90 \n")
    
    #write the footer of the file
    #1536 should be changed to the last part of your file + 1
    
    f.write(
    current_layer+", "+str(current_time)+", End_track \n"
    )
    end_or_not = input("Would you like to add another layer to your music?\n1 for YES,0 for NO\n")
    if int(end_or_not) == 0:
        wanna_continue = 0
    else:
        current_layer = str(int(current_layer) + 1)
f.write(    
"0, 0, End_of_file"
    )
f.close()

import os
import sys
os.popen('csvmidi "'+end_file_name+'.csv" "'+end_file_name+'.mid"','r')

bye = input("Your file is ready. Please press enter to exit")
os.remove(end_file_name+'.csv')

sys.exit()




