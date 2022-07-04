"""The goal of this lab is to crack passwords with different standard methods. 
Each student has their own set of passwords waiting to be cracked. 

1) Put your name (as it appears in the password file name) in the variable NAME below.
2) Implement the functions at the bottom of this template,
   calling check_password(.) with each possible password.

The deadline is today at the end of the lab!
"""

import hashlib
from urllib.request import urlopen
from urllib.parse import urlencode
import itertools


# TODO: write your last name here (must match the name of the password file)
NAME = "michel".lower()

# This file contains original passwords but encrypted.
# It is used for validating passwords your cracked locally.
# If there is a match, this match is sent to the server.
ENCFILE = "INF344_2021_2022_enc/" + NAME + ".enc"

# Leaderboard address
SERVER_ADD = 'http://137.194.211.123/' # DO NOT CHANGE THIS VALUE!!!


class Crack:
    """Password Cracking"""

    def __init__(self, filename, name):
        """
        -------------------
        This method should not be modified !!
        ------------------

        Initialize the cracking session
        :param filename: The file with the encrypted passwords
        :param name: Your name
        :return: Nothing
        """
        self.name = name.lower()

        # load the encrypted passwords
        self.passwords = self.get_passwords(filename)

    def get_passwords(self, filename):
        """
        -------------------
        This method should not be modified !!
        ------------------

        Get the passwords from a file
        :param filename: The name of the file which stores the passwords
        :return: The set of passwords
        """
        passwords = set()
        with open(filename, "r") as f:
            for line in f:
                passwords.add(line.strip())
        return passwords

    def check_password(self, password):
        """
        -------------------
        This method should not be modified !!
        ------------------

        Checks if the password you give is correct
        :param password: A string representing the password
        :return: Whether the password is correct or not
        """
        password = str(password)
        cond = hashlib.md5(bytes(password, "utf-8")).hexdigest() in \
               self.passwords
        if cond:
            args = {"name": self.name,
                    "password": password}
            args = urlencode(args, "utf-8")
            page = urlopen(SERVER_ADD + 'submit?' + args)
            if b'True' in page.read():
                print("You found the password: " + password)
                return True
        return False

    def evaluate(self):
        """
        -------------------
        This method should not be modified !!
        ------------------

        Retrieve the grade from the server,
        """
        args = {"name": NAME}
        args = urlencode(args, "utf-8")
        page = urlopen(SERVER_ADD + 'evaluate?' + args)
        print("Grade :=>> " + page.read().decode('ascii').strip())


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
            elif elm == 'i':
                password_leet += '1'
            elif elm == 'o':
                password_leet += '0'
            else:
                password_leet += elm
                
        return password_leet
    
    #################################### End Utils function ####################################





    def crack(self):
        """
        -------------------
        This method should be modified carefully !!
        ------------------

        Cracks the passwords. YOUR CODE GOES IN THE METHODS BELOW.

        We suggest you use one function per question. Once a password is found,
        it is memorized by the server, thus YOU CAN COMMENT THE CALL to the
        corresponding function once you find all the corresponding passwords.
        """
        #self.bruteforce_digits()
        #self.bruteforce_letters()
        #self.dictionary_passwords()
        #self.dictionary_passwords_leet()
        #self.dictionary_words_hyphen()
        self.dictionary_words_digits()

    # You code goes here.
    # Call the function check_password(.) with all possible passwords
    def bruteforce_digits(self):
        # Via brute-force, find passwords with *up to* 9 digits (max is 999,999,999)
        # [4 passwords / 1 point]
        # TODO: Your code here
        
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
        # Via brute-force, find passwords with *up to* 5 letters in upper or lower case, e.g, zPLsD
        # [4 passwords / 1 point]
        # TODO: Your code here
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
        # Use the list of the 1k most common passwords and try all of them (lowercase)
        # [1k most common passwords]
        # [2 passwords / 1 point]
        # TODO: Your code here
        print("#### Testing dictionary_passwords strategy ####")
        
        counter_password = 0
        
        # Opening the file in reader only
        file_1k = open('1000-most-common-passwords.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_1k.readlines()
        
        # Closing the file
        file_1k.close()
        
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
        # Reuse the 1k most common passwords, and apply the transformations e -> 3, l -> 1, a -> @, i -> 1, o -> 0 -- to all possible combinations of possible positions
        # [1k most common passwords]
        # [3 passwords / 1 point]
        # TODO: Your code here
        print("#### Testing dictionary_passwords_leet strategy ####")
        
        counter_password = 0
        
        # Opening the file in reader only
        file_1k = open('1000-most-common-passwords.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_1k.readlines()
        
        # Closing the file
        file_1k.close()
        
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
        # Use the 10k most common English words (lowercase) with up to 3 randomly added hyphens inside the word, as in h-e-ll-o
        # Passwords CANNOT begin or end with '-', and there CANNOT be two '-' in a row
        # [10k most common English words]
        # [3 passwords / 1 point]
        # TODO: Your code here
        print("#### Testing dictionary_words_hyphen strategy ####")
        
        counter_password = 0
        
        # Opening the file in reader only
        file_10k = open('google-10000-english.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_10k.readlines()
        
        # Closing the file
        file_10k.close()
        
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
        # Concatenate the 10k most common English words (lowercase) to a minimum length of 19, plus a two-digit number
        # [10k most common English words]
        # e.g., computers + democrates + 01 -> computersdemocrates01
        # len(computersdemocrates) >= 19
        # [4 passwords / 1 point]
        # TODO: Your code here
        print("#### Testing dictionary_words_digits strategy ####")
                
        # Opening the file in reader only
        file_10k = open('google-10000-english.txt', "r", encoding='utf-8')
        
        # Read each line of the file
        lines = file_10k.readlines()
        
        # Closing the file
        file_10k.close()
        
        digit_list = ['0','1','2','3','4','5','6','7','8','9']
        
        # Browsing the lines of the file stored in the variable lines 
        
        list_password_10k = list()
        for elm in lines:
            password_cleaned = elm.split("\n")[0]
            list_password_10k.append(password_cleaned)
            
        #print(list_password_10k)
        list_password_up_19 = list()
        
        for i in range(1, len(list_password_10k)):
            for j in range(1, len(list_password_10k)):
                password_temp = list_password_10k[i] + list_password_10k[j]
                #print(password_temp)
                if len(password_temp) >= 19:
                    list_password_up_19.append(password_temp)
                    #print(password_temp)
                    
        #print(list_password_up_19)
        
        for password in list_password_up_19:
            # Removing the white spaces if it exists 
            password = password.strip()
            # Test all combinatation of 1 to 2 digits
            for i in range(1,3):
                for k in itertools.product(digit_list, repeat = i):
                    password_words_digits = "".join(str(password) + str("".join(k)))
                    # Check if a password is found
                    self.check_password(password_words_digits)
                    #print(password_words_digits)



if __name__ == "__main__":
    crack = Crack(ENCFILE, NAME)
    crack.crack()
    crack.evaluate()
