input_string =  input("enter the string to be translated")
removablestrings = ["<p>","</p>","<br>"]
for i in removablestrings:
    input_string = input_string.replace(i,"")
print(input_string)