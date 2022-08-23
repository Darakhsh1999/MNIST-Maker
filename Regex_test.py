import re



test_strings = {"Area bss":True, # 1
                "Awds_adwa32":True, # 2
                "__aaa__":False, # 3
                "2312ad":True, # 4
                "A23231c":True, # 5
                " adwa":False, # 6
                "adwwa  ":False, # 7
                "$$_adwad":False, # 8
                "~~ADdw_":False, # 9
                "Adwdw$$dwa3":False, # 10
                "Adwadw_adWW_232":True, # 11
                "Swew,.-32":False, # 12
                "Dwae@@@dwa":False, # 13
                "Adaw dwamo32low":True, # 14
                "A(32)_32":False, # 15
                "All--oow32ed":True, # 16
                "Are//be":False, # 17
                "32ref\\e":False, # 18
                "Aplo{42a}d":False, # 19
                "awdw[32]daw32":False, # 20
                "aewa\eww":False, # 21
                "dawdw32\\":False, # 22
                "Arash Mnist digits-2032p":True, # 23
                "Loaded_MNIST_320p--HD":True, # 24
                "360p-pixel_MNIST-images":True, # 25
                "CON":False, # 26
                "AUX":False, # 27
                "LPT10":True, # 28
                "NUL1":True, # 29
                "CON23":True, # 30
                "LPT3":False, # 31
                "COM23":True, # 32
                "COM4":False, # 33
                "COM_3":True, # 34
                "CON2":True, # 35
                "LPT01":True # 36
                } 


regex = re.compile('^CON|(^[a-zA-Z0-9]+[^<>:"/|?*~%#+$!@,.();{}\[\]\\\]+[a-zA-Z0-9]$)') # want to be not None
reserved_names = re.compile("(^CON$|^PRN$|^AUX$|^NUL$|^COM\d{1}$|^LPT\d{1}$)") # want to be None

word_idx = 0
test_good = 0
for test_str,target in test_strings.items():

    regex_match = regex.search(test_str)
    reserve_name = reserved_names.search(test_str)
    print(word_idx+1,":",regex_match)
    if ((target and (regex_match is not None)) and reserve_name is None) or (not target and ((regex_match is None) or (reserve_name is not None))):
        print("Test successful")
        test_good += 1
    else:
        print("Test failed")
    word_idx += 1


print("#####################")
if word_idx == test_good:
    print("All tests succeeded")
else:
    print(word_idx-test_good,"tests failed")