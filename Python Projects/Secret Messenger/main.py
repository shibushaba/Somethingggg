print("Welcom To Secrete Messenger")
print("Enter decode/encode/exit")

def encode(text,shift):
    encrypted =""
    for char in text:
        if char.isalpha():
            new_char = chr(((ord(char.lower())-97 + shift) %26)+97)
            encrypted += new_char
        else:
            encrypted += char

        return encrypted      
    


    def decode(text, shift):
        return encode(text, -shift)
    
    