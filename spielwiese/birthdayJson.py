import json

infoAboutMe = {
    "name": "Sophia Hollander",
    "birthday": "22.11.1979"
}

# write file
with open("birthdayInfo.json", "w") as f:
    json.dump(infoAboutMe, f)

# read file
with open("birthdayInfo.json", "r") as f:
    name = json.load(f)

print(name)
