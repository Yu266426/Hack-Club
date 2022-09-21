with open("Hack Club Members.txt") as file:
    names = []
    for line in file.readlines():
        split_line = line.split(" ")
        first = split_line[0]
        last = split_line[1][:-1]
        
        names.append((first, last))

emails = []
for name in names:
    emails.append(f"{name[0].lower()}.{name[1].lower()}@smus.ca")
    
    
with open("Hack Club Emails.txt", "w+") as file:
    for email in emails:
        file.write(f"{email}\n")
