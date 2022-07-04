# Written with <3 by Julien Romero
import random
import hashlib
from sys import argv
import sys
import itertools
from random import randint
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode


#NAME = "koch".lower()
NAME = "dupond".lower()

# This is the correct location on the moodle
#ENCFILE = "../passwords2020/" + NAME + ".enc"
# If you run the script on your computer: uncomment and fill the following
# line. Do not forget to comment this line again when you submit your code
# on the moodle.

#ENCFILE = "koch.enc"
ENCFILE = "dupond.enc"



class Crack:
    """Crack The general method used to crack the passwords"""

    def __init__(self, filename, name):
        """__init__
        Initialize the cracking session
        :param filename: The file with the encrypted passwords
        :param name: Your name
        :return: Nothing
        """
        self.name = name.lower()
        self.passwords = get_passwords(filename)



#    def check_password(self, password):
#        """check_password
#        Checks if the password is correct
#        !! This method should not be modified !!
#        :param password: A string representing the password
#        :return: Whether the password is correct or not
#        """
#        password = str(password)
#        cond = False
#        if (sys.version_info > (3, 0)):
#            cond = hashlib.md5(bytes(password, "utf-8")).hexdigest() in \
#                self.passwords
#        else:
#            cond = hashlib.md5(bytearray(password)).hexdigest() in \
#                self.passwords
#        if cond:
#            args = {"name": self.name,
#                    "password": password}
#            args = urlencode(args, "utf-8")
#            page = urlopen('http://137.194.211.71:5000/' +
#                                          'submit?' + args)
#            if b'True' in page.read():
#                print("You found the password: " + password)
#                return True
#        return False

    def check_password(self, password):
        """check_password
        Checks if the password is correct
        !! This method should not be modified !!
        :param password: A string representing the password
        :return: Whether the password is correct or not
        """
        password = str(password)
        cond = False
        
        if (sys.version_info > (3, 0)):
            cond = hashlib.md5(bytes(password, "utf-8")).hexdigest() in \
                self.passwords
        else:
            cond = hashlib.md5(bytearray(password)).hexdigest() in \
                self.passwords
        if cond:
            print("You found the password: " + password)
            return True
        return False

    
    #################################### Start Utils function ####################################
        
    def password_to_leet(self, password):
        """
        DESCRIPTION:
            the function converts a password into a password that compliant with the leet format 
        ARGS: 
            password = raw password from the dictionary of password
        RETURNS:
            return a compliant leet password format to leet format
        """
        password_leet = ""
        
        for elm in password:
            if elm == 'e':
                password_leet += '3'
            elif elm == 'l':
                password_leet += '1'
            elif elm == 'a':
                password_leet += '@'
            elif elm == 'o':
                password_leet += '0'
            else:
                password_leet += elm
                
        return password_leet
    
    def password_to_diacritics(self, password):
            password_diacritics = ""
            
            diacritics_list = ["é", "è", "à", "ç", "ù"]
            
            for elm in password:
                if elm not in diacritics_list:
                    password_diacritics += elm
                    
                else:
                    if elm == 'é':
                        random_int = random.randint(0,1)
                        if random_int == 1:
                            password_diacritics += 'e'
                        else:
                            password_diacritics += elm
                        
                    elif elm == 'è':
                        random_int = random.randint(0,1)
                        if random_int == 1:
                            password_diacritics += 'e'
                        else:
                            password_diacritics += elm
    
                    elif elm == 'à':
                        random_int = random.randint(0,1)
                        if random_int == 1:
                            password_diacritics += 'a'
                        else:
                            password_diacritics += elm
    
                    elif elm == 'ç':
                        random_int = random.randint(0,1)
                        if random_int == 1:
                            password_diacritics += 'c'
                        else:
                            password_diacritics += elm
    
                    elif elm == 'ù':
                        random_int = random.randint(0,1)
                        if random_int == 1:
                            password_diacritics += 'u'
                        else:
                            password_diacritics += elm
    
            return password_diacritics        
    #################################### End Utils function ####################################

    def crack(self):
        """crack
        Cracks the passwords. YOUR CODE GOES BELOW.

        We suggest you use one function per question. Once a password is found,
        it is memorized by the server, thus you can comment the call to the
        corresponding function once you find all the corresponding passwords.
        """
        #self.bruteforce_digits() #ok
        #self.bruteforce_letters() #ok

        #self.dictionary_passwords() #ok
        #self.dictionary_passwords_leet() #ok
        #self.dictionary_words_hyphen() #ok
        self.dictionary_words_digits() # non ok
        #self.dictionary_words_diacritics() # partialy ok
        #self.dictionary_city_diceware() # ok

        #self.social_google() 
        #self.social_jdoe() # non ok
        #self.paste()

    def bruteforce_digits(self):
        """
        Intuitivement, on tendance à dire que plus le mot de passe est long, plus ce dernier est difficile à deviner
        Cela est vrai en pratique plus le mot de passe est le plus il est nécessaire de tester plus de combinaisons de caractères possibles
        Dans notre cas, si le mot de passe contient uniquement pas plus de 9 chiffres, le nombre totale de combinaisons a tester pour pouvoir
        espérer trouver le mot de passe est de 9^10. 
        En génélarisant on obtient la formule suivante :
            Pour un mot de au maximum 9 caractères (ici des chiffres) avec 10 possibilités de caractères
            9^10 = 3 486 784 401 combinaisons
        Or remarque donc que lorsque le mot de passe de grand le temps de calcul s'allonge de plus en plus.
        C'est pourquoi, il généralement recommandé de choisir un mot de passe avec au minimum 8 chiffres'
        """
        
        print("#### Testing bruteforce_digits strategy ####")
        
        counter_password = 0
        
        # Init list of 10 digits from 0 to 9
        digit_list  = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        
        # test all possible combinations from 1 digits to 9 digits
        for i in range(1, len(digit_list)):
            for k in itertools.product(digit_list, repeat = i):
                password_digits = ''.join(k)
                # Check if a password is found
                self.check_password(password_digits)
                if self.check_password(password_digits) == True:
                    counter_password = counter_password + 1
                    print(counter_password)
                if counter_password == 4:
                    return
        return

    def bruteforce_letters(self):
        """
        De manière analogue à la précédente question, plus le mot de passe est long, plus le mot de passe contient de caractères différents 
        plus il est nécessaire de tenter des combinaisons différentes et plus le temps de calcul se rallonge
        """
        print("#### Testing bruteforce_letters strategy ####")
        
        counter_password = 0
        
        # Init lower case letter list
        lower_case_letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        # Init upper case letter list
        upper_case_letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        
        # concatenate the two list of mixed care letter
        letter_list = lower_case_letter + upper_case_letter
        
        # test all possible combinations from 1 mixed case letter to 5 mixed case letters
        for i in range(1, 6):
            for k in itertools.product(letter_list, repeat = i):
                password_letter = ''.join(k)
                # Check if a password is found
                self.check_password(password_letter)
                if self.check_password(password_letter) == True:
                    counter_password = counter_password + 1
                    print(counter_password)
                if counter_password == 4:
                    return
        return


    def dictionary_passwords(self):
        # Lien du dictionnaire "10k most common password"
        # https://gitlab.com/kalilinux/packages/seclists/-/blob/kali/master/Passwords/Common-Credentials/10k-most-common.txt
        
        print("#### Testing dictionary_passwords strategy ####")
        
        counter_password = 0
        
        # Opening the file in reader only
        file_10k = open('10k_common_password.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_10k.readlines()
        
        # Closing the file
        file_10k.close()
        
        # Browsing the lines of the file stored in the variable lines 
        for password in lines:
            # Removing the white spaces if it exists 
            password = password.strip()
            
            # Check if a password is found
            self.check_password(password)
            if self.check_password(password) == True:
                counter_password = counter_password + 1
                print(counter_password)
            if counter_password == 4:
                return
            
            

    def dictionary_passwords_leet(self):
        # Lien du dictionnaire "10k most common password"
        # https://gitlab.com/kalilinux/packages/seclists/-/blob/kali/master/Passwords/Common-Credentials/10k-most-common.txt
        
        print("#### Testing dictionary_passwords_leet strategy ####")
        
        counter_password = 0
        
        # Opening the file in reader only
        file_10k = open('10k_common_password.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_10k.readlines()
        
        # Closing the file
        file_10k.close()
        
        # Browsing the lines of the file stored in the variable lines 
        for password in lines:
            # Removing the white spaces if it exists 
            password = password.strip()
            # Convert password to leet password
            leet_password = self.password_to_leet(password)
            
            # Check if a password is found
            self.check_password(leet_password)        
            if self.check_password(leet_password) == True:
                counter_password = counter_password + 1
                print(counter_password)
            if counter_password == 4:
                return


    def dictionary_words_hyphen(self):
        # Lien du dictionnaire "20k most common password"
        # https://github.com/first20hours/google-10000-english/blob/master/20k.txt
        
        print("#### Testing dictionary_words_hyphen strategy ####")
        
        counter_password = 0
        
        # Opening the file in reader only
        file_20k = open('20k_common_password.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_20k.readlines()
        
        # Closing the file
        file_20k.close()
        
        # Browsing the lines of the file stored in the variable lines 
        for password in lines:
            
            # Init/Reset the password list hyphen at each new line of the dictionnary
            password_list_hypen = list()
            
            # Removing the white spaces if it exists 
            password = password.strip()
            
            # Test all combination for the insertion of the 1st hyphen 
            for i in range(len(password)):
                password_hypen1 = password[:i] + "-" + password[i:]
                password_list_hypen.append(password_hypen1)
                
                # Test all combination for the insertion of the 2dn hyphen
                for k in range(len(password_hypen1)):
                    password_hypen2 = password_hypen1[:k] + "-" + password_hypen1[k:]
                    password_list_hypen.append(password_hypen2)
                    
                    # Test all combination for the insertion of the 3rd hyphen
                    for l in range(len(password_hypen2)):
                        password_hypen3 = password_hypen2[:l] + "-" + password_hypen2[l:]
                        password_list_hypen.append(password_hypen3)
        
            # drop duplicated password
            password_list_hypen = list(dict.fromkeys(password_list_hypen))
            
            # Check if a password is found
            for password in password_list_hypen:
                self.check_password(password)        
                if self.check_password(password) == True:
                    counter_password = counter_password + 1
                    print(counter_password)
                if counter_password == 4:
                    return
            

    def dictionary_words_digits(self):
        # Lien du dictionnaire "20k most common password"
        # https://github.com/first20hours/google-10000-english/blob/master/20k.txt
        
        print("#### Testing dictionary_words_digits strategy ####")
        
        counter_password = 0
        
        # Opening the file in reader only
        file_20k = open('google-10000-english.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_20k.readlines()
        
        # Closing the file
        file_20k.close()
        
        digit_list = ['0','1','2','3','4','5','6','7','8','9']
        
        # Browsing the lines of the file stored in the variable lines 
        
        list_password_20k = list()
        for elm in lines:
            password_cleaned = elm.split("\n")[0]
            list_password_20k.append(password_cleaned)
            
        #print(list_password_20k)
        list_password_up_19 = list()
        
        for i in range(1, 100):
            for j in range(1, 100):
                password_temp = list_password_20k[i] + list_password_20k[j]
                #print(password_temp)
                if len(password_temp) >= 19:
                    list_password_up_19.append(password_temp)
                    print(password_temp)
                    
        print(list_password_up_19)
        
        for password in list_password_up_19:
            # Removing the white spaces if it exists 
            password = password.strip()
            # Test all combinatation of 1 to 2 digits
            for i in range(1,3):
                for k in itertools.product(digit_list, repeat = i):
                    password_words_digits = "".join(str(password) + str("".join(k)))
                    # Check if a password is found
                    #self.check_password(password_words_digits)
                    print(password_words_digits)
        
        #for i in range(1, len(list_password_20k)):
            #for j in itertools.product(list_password_20k, repeat = i):
                #password = "".join(j)
                #print(password)
        
        #for password in lines:
                        
            # Removing the white spaces if it exists 
            #password = password.strip()
            
            # Take all the password from the dicationnary which have at least 7 letters
            #if len(password) > 6:
            
            #list_password_up_19= list()
            #for i in range(1,2):
                #for j in itertools.product(digit_list, repeat = i):
                
            # Test all combinatation of 1 to 2 digits
            #for i in range(1,3):
                #for k in itertools.product(digit_list, repeat = i):
                    #password_words_digits = "".join(str(password) + str("".join(k)))
                    # Check if a password is found
                    #self.check_password(password_words_digits)
                    #print(password_words_digits)
                    #if self.check_password(password_words_digits) == True:
                        #counter_password = counter_password + 1
                        #print(counter_password)
                    #if counter_password == 4:
                        #return
                                                   

    def dictionary_words_diacritics(self):
        # A voir
        print("#### Testing dictionary_words_diacritics strategy ####")
        
        counter_password = 0
        
        # Opening the file in reader only
        file_10k_french = open('10k_french_common_password.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_10k_french.readlines()
        
        # Closing the file
        file_10k_french.close()
        
        # Browsing the lines of the file stored in the variable lines 
        for password in lines:
            # Removing the white spaces if it exists 
            password = password.strip()
            password = password.split("\t")[0]
            # Convert password to leet password
            diacritics_password = self.password_to_diacritics(password)
            # Check if a password is found
            #print(diacritics_password)
            self.check_password(diacritics_password)        
            if self.check_password(diacritics_password) == True:
                counter_password = counter_password + 1
                print(counter_password)
            if counter_password == 4:
                return


    def dictionary_city_diceware(self):
        # Lien du dictionnaire "african_capitals.txt"
        # https://www.nationsonline.org/oneworld/capitals_africa.htm
        
        print("#### Testing dictionary_city_diceware strategy ####")
        
        counter_password = 0
        
        # Opening the file in reader only
        file_african_capitals = open('african_capitals.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_african_capitals.readlines()
        
        # Closing the file
        file_african_capitals.close()
        
        african_capitals_list = list()
                
        # Browsing the lines of the file stored in the variable lines 
        for password in lines:
                        
            # Removing the white spaces if it exists 
            password = password.strip()
            
            # Join the two string if the name of capital city is composed of more than two words
            # put transform output in lower case 
            password = ''.join(password.split()).lower()
            african_capitals_list.append(password)
            
        for capital in african_capitals_list:
            # Test all possible combinations from 1 to 4 characters
            for i in range(1,5):
                for k in itertools.product(african_capitals_list, repeat = i):
                        # Check if a password is found
                        password_captial_city = "-".join(k)
                        self.check_password(password_captial_city)        
                        if self.check_password(password_captial_city) == True:
                            counter_password = counter_password + 1
                            print(counter_password)
                        if counter_password == 4:
                            return
                

    def social_google(self):
        
        print("#### Testing social_google strategy ####")
        
        counter_password = 0
        
        original_password = "Prom3theus"
        original_password_lower_case = original_password.lower()
        # ['Prom3theus', 'prom3theus']
        list_original_password = [original_password, original_password_lower_case]
        
        # 1ST STRATEGY : Leet words transformation
        print("------ Starting Strategy 1 ------")

        list_leet_passwords = ["prom3th3us", "prom3theus", "pr0m3th3us", "pr0metheus", "pr0m3theus", "pr0meth3us", "Prom3th3us", "Prom3theus", "Pr0m3th3us", "Pr0metheus", "Pr0m3theus", "Pr0meth3us"]
        
        for password in list_leet_passwords:
            # Removing the white spaces if it exists 
            password = password.strip()
            # Check if a password is found
            self.check_password(password)
            if self.check_password(password) == True:
                counter_password = counter_password + 1
                print(counter_password)
            if counter_password == 4:
                return
        
        print("")
        print("------ Finish Strategy 1 ------")
        print("")

        
        # 2ND STRATEGY : Concatenate 2 digits number with the orignial password
        print("------ Starting Strategy 2 ------")
        
        # Init digit list number
        digit_list = ['0','1','2','3','4','5','6','7','8','9']

        # Init words digits passwords list
        list_password_words_digits = list()


        for password in list_original_password:
            password = password.strip()
            # Test all combinatation of 1 to 2 digits
            for i in range(1,3):
                for k in itertools.product(digit_list, repeat = i):
                    password_words_digits = "".join(str(password) + str("".join(k)))
                    list_password_words_digits.append(password_words_digits)

        for password in list_password_words_digits:           
            # Check if a password is found
            self.check_password(password)
            if self.check_password(password) == True:
                counter_password = counter_password + 1
                print(counter_password)
            if counter_password == 4:
                return
        
        print("")
        print("------ Finish Strategy 2 ------")
        print("")
        
        # 3RD STRATEGY : Add hyphen randomly 
        print("------ Starting Strategy 3 ------")
        for password in list_original_password:
            # Init/Reset the password list hyphen at each new line of the dictionnary
            password_list_hypen = list()
                
            # Removing the white spaces if it exists 
            password = password.strip()
                
            # Test all combination for the insertion of the 1st hyphen 
            for i in range(len(password)):
                password_hypen1 = password[:i] + "-" + password[i:]
                password_list_hypen.append(password_hypen1)
                    
                # Test all combination for the insertion of the 2dn hyphen
                for k in range(len(password_hypen1)):
                    password_hypen2 = password_hypen1[:k] + "-" + password_hypen1[k:]
                    password_list_hypen.append(password_hypen2)
                        
                    # Test all combination for the insertion of the 3rd hyphen
                    for l in range(len(password_hypen2)):
                        password_hypen3 = password_hypen2[:l] + "-" + password_hypen2[l:]
                        password_list_hypen.append(password_hypen3)
        
            # drop duplicated password
            password_list_hypen = list(dict.fromkeys(password_list_hypen))
            
            # Check if a password is found
            for password in password_list_hypen:
                self.check_password(password)
                if self.check_password(password) == True:
                    counter_password = counter_password + 1
                    print(counter_password)
                if counter_password == 4:
                    return
        
        print("")
        print("------ Finish Strategy 3 ------")
        print("")
        
        # 4TH STRATEGY : Combinining 1st and 2nd strategy
        print("------ Starting Strategy 4 ------")
        
        list_password_strategy4 = list()
        
        for password in list_leet_passwords:
            password = password.strip()
            # Test all combinatation of 1 to 2 digits
            for i in range(1,3):
                for k in itertools.product(digit_list, repeat = i):
                    password_words_digits_bis = "".join(str(password) + str("".join(k)))
                    list_password_strategy4.append(password_words_digits_bis)

        for password in list_password_strategy4:           
            # Check if a password is found
            self.check_password(password)
            if self.check_password(password) == True:
                counter_password = counter_password + 1
                print(counter_password)
            if counter_password == 4:
                return
            
        print("")
        print("------ Finish Strategy 4 ------")
        print("")
        
        # 5TH STRATEGY : Combinining 1st and 3rd strategy
        print("------ Starting Strategy 5 ------")
                
        for password in list_leet_passwords:
            # Init/Reset the password list hyphen at each new line of the dictionnary
            password_list_hypen_bis = list()
                
            # Removing the white spaces if it exists 
            password = password.strip()
                
            # Test all combination for the insertion of the 1st hyphen 
            for i in range(len(password)):
                password_hypen1 = password[:i] + "-" + password[i:]
                password_list_hypen_bis.append(password_hypen1)
                    
                # Test all combination for the insertion of the 2dn hyphen
                for k in range(len(password_hypen1)):
                    password_hypen2 = password_hypen1[:k] + "-" + password_hypen1[k:]
                    password_list_hypen_bis.append(password_hypen2)
                        
                    # Test all combination for the insertion of the 3rd hyphen
                    for l in range(len(password_hypen2)):
                        password_hypen3 = password_hypen2[:l] + "-" + password_hypen2[l:]
                        password_list_hypen_bis.append(password_hypen3)
        
            # drop duplicated password
            password_list_hypen_bis = list(dict.fromkeys(password_list_hypen_bis))
            
            # Check if a password is found
            for password in password_list_hypen_bis:
                self.check_password(password)
                if self.check_password(password) == True:
                    counter_password = counter_password + 1
                    print(counter_password)
                if counter_password == 4:
                    return
        
        print("")
        print("------ Finish Strategy 5 ------")
        print("")
        
        # 6TH STRATEGY : Combinining 2nd and 3rd strategy
        print("------ Starting Strategy 6 ------")
                
        for password in list_password_words_digits:
            # Init/Reset the password list hyphen at each new line of the dictionnary
            password_list_hypen_bis_bis = list()
                
            # Removing the white spaces if it exists 
            password = password.strip()
                
            # Test all combination for the insertion of the 1st hyphen 
            for i in range(len(password)):
                password_hypen1 = password[:i] + "-" + password[i:]
                password_list_hypen_bis_bis.append(password_hypen1)
                    
                # Test all combination for the insertion of the 2dn hyphen
                for k in range(len(password_hypen1)):
                    password_hypen2 = password_hypen1[:k] + "-" + password_hypen1[k:]
                    password_list_hypen_bis_bis.append(password_hypen2)
                        
                    # Test all combination for the insertion of the 3rd hyphen
                    for l in range(len(password_hypen2)):
                        password_hypen3 = password_hypen2[:l] + "-" + password_hypen2[l:]
                        password_list_hypen_bis_bis.append(password_hypen3)
        
            # drop duplicated password
            password_list_hypen_bis_bis = list(dict.fromkeys(password_list_hypen_bis_bis))
            
            # Check if a password is found
            for password in password_list_hypen_bis_bis:
                self.check_password(password)
                if self.check_password(password) == True:
                    counter_password = counter_password + 1
                    print(counter_password)
                if counter_password == 4:
                    return
                
        print("")
        print("------ Finish Strategy 6 ------")
        print("")
        

    def social_jdoe(self):
        print("#### Testing social_jdoe strategy ####")
        
        counter_password = 0
        
        # List of all possible subset of John's password
        jonh_info_upper_case = ['John', 'Doe', 'April', '25', '1978', '04251978', 'Shakespeare', 'Shaker', 'Heights', 'Ohio', 'New', 'York', 'New York', 'Cleveland', 'Indians', 'Sunday']
        
        jonh_info_lower_case = list()
        
        # convert John's info to lower case
        for info in jonh_info_upper_case:
            info_lower_case = info.lower()
            jonh_info_lower_case.append(info_lower_case)
            
        # concatenate the two list of John's info
        jonh_info = jonh_info_upper_case + jonh_info_lower_case
        
        # drop duplicated elements
        jonh_info = list(dict.fromkeys(jonh_info))
        # then iterate to test all the possible combinations 
        for i in range(1,len(jonh_info)):
            for k in itertools.product(jonh_info, repeat = i):
                john_password = "".join(k).strip()
                print(john_password)
                # Check if a password is found
                self.check_password(john_password)        
                if self.check_password(john_password) == True:
                    counter_password = counter_password + 1
                    print(counter_password)
                if counter_password == 4:
                    return
      
    def paste(self):
        """
        the password of the following email can be found on the web at the following url:
            https://throwbin.io/RvokH9z
        """
        
        password_leaked = "Riseagainst1"
        # Check if a password is found
        self.check_password(password_leaked)        



def get_passwords(filename):
    """get_passwords
    Get the passwords from a file
    :param filename: The name of the file which stores the passwords
    :return: The set of passwords
    """
    passwords = set()
    with open(filename, "r") as f:
        for line in f:
            passwords.add(line.strip())
    return passwords


# First argument is the password file, the second your name
crack = Crack(ENCFILE, NAME)


if __name__ == "__main__":
    crack.crack()